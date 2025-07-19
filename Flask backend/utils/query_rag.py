# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
# from utils.get_embedding_function import get_embedding_function

# # Load environment variables
# load_dotenv()


# CHROMA_PATH = "chroma"

# PROMPT_TEMPLATE = """
# Answer the question based only on the following context:

# {context}

# ---

# Answer the question based on the above context: {question}
# """

# def query_rag(query_text: str):
   
#     # Query the RAG system with the given text
   
#     try:
#         # Prepare the DB
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
#         # Search the DB
#         results = db.similarity_search_with_score(query_text, k=5)
        
#         if not results:
#             return {
#                 "success": False,
#                 "message": "No relevant documents found in the database.",
#                 "response": "No relevant information found.",
#                 "sources": []
#             }
        
#         # Prepare context and prompt
#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
#         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#         prompt = prompt_template.format(context=context_text, question=query_text)
        
#         # Initialize OpenAI Chat model
#         model = ChatOpenAI(
#             model="gpt-3.5-turbo",
#             temperature=0,
#             openai_api_key=os.getenv("OPENAI_API_KEY")
#         )
        
#         # Get response from model
#         response_text = model.invoke(prompt)
        
#         # Extract content from response
#         if hasattr(response_text, 'content'):
#             response_content = response_text.content
#         else:
#             response_content = str(response_text)
        
#         # Get sources
#         sources = [doc.metadata.get("id", "Unknown") for doc, _score in results]
        
#         return {
#             "success": True,
#             "response": response_content,
#             "sources": sources,
#             "num_sources": len(sources)
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "message": f"Error querying the model: {str(e)}",
#             "response": "",
#             "sources": []
#         }


"""
This script:

Loads the persisted Chroma vector database (chroma/)
Takes a question
Retrieves relevant document chunks using embeddings
Feeds them + the question to the OpenAI model
Returns the generated answer
"""


#personlize QA
from typing import List
from datetime import datetime
import os

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from services.profile_service import get as get_profile
from services.personalized_ranking import rank as rank_chunks
from utils.get_embedding_function import get_embedding_function

load_dotenv()
CHROMA_PATH = "chroma"

BASE_TEMPLATE = """
{system_message}

Answer the question **only** using the following context:

{context}

---

{question}
""".strip()

# Builds the final prompt using the user's role & interests from their profile.
def _build_prompt(
    profile_role: str,
    profile_interests: List[str],
    context: str,
    question: str,
) -> str:
    sys_msg = (
        "You are a helpful assistant. "
        f"The user is a {profile_role} interested in {', '.join(profile_interests) or 'varied topics'}. "
        "Frame the answer accordingly."
    )
    prompt_template = ChatPromptTemplate.from_template(BASE_TEMPLATE)
    return prompt_template.format(
        system_message=sys_msg, context=context, question=question
    )


def query_rag(query_text: str, user_id: str) -> dict:
    """
    Main entry point for Flask `/api/query`.
    """
    try:

        # Loads the profile (UserProfile) of the user by their user_id.
        # Includes their role and interests.
        profile = get_profile(user_id) 
        if not profile:
            return {
                "success": False,
                "message": f"No profile found for user_id={user_id}.",
                "response": "",
                "sources": [],
            }

        # 1) retrieval
        embedding_fn = get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embedding_fn
        )
        # Define Chroma filter
        chroma_filter = {
            "$or": [
                {"audience": {"$eq": profile.role}},
                {"topics": {"$in": profile.interests}},
            ]
        }

        # first pass – wider net
        # Retrieves top 20 similar documents based on embeddings and the filter.
        raw_results = db.similarity_search_with_score(
            query_text, k=20, filter=chroma_filter
        )  #  Returns a list of tuples: (Document, similarity_score).

        if not raw_results:
            return {
                "success": False,
                "message": "No relevant documents found.",
                "response": "",
                "sources": [],
            }

        # 2) personalized re-ranking
        #  Uses a custom logic (in rank_chunks) to re-rank based on user preferences.
        # More personalized than just cosine similarity.
        top_ranked = rank_chunks(raw_results, profile)
        
        # Merges the content of top documents into a single context for the prompt.
        context_text = "\n\n---\n\n".join(
            [doc.page_content for doc, _ in top_ranked]
        )

        # 3) prompt
        prompt = _build_prompt(
            profile.role, profile.interests, context_text, query_text
        )

        # 4) call LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.0,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        resp = llm.invoke(prompt)
        answer = resp.content if hasattr(resp, "content") else str(resp)
        
        # Gathers the document IDs (or "Unknown") from metadata to show sources used.
        sources = [doc.metadata.get("id", "Unknown") for doc, _ in top_ranked]

        return {
            "success": True,
            "response": answer,
            "sources": sources,
            "num_sources": len(sources),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as exc:
        return {
            "success": False,
            "message": f"query_rag error: {exc}",
            "response": "",
            "sources": [],
        }
