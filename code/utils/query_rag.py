from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from utils.get_embedding_function import get_embedding_function

# Load environment variables
load_dotenv()


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
   
    # Query the RAG system with the given text
   
    try:
        # Prepare the DB
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Search the DB
        results = db.similarity_search_with_score(query_text, k=5)
        
        if not results:
            return {
                "success": False,
                "message": "No relevant documents found in the database.",
                "response": "No relevant information found.",
                "sources": []
            }
        
        # Prepare context and prompt
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        
        # Initialize OpenAI Chat model
        model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Get response from model
        response_text = model.invoke(prompt)
        
        # Extract content from response
        if hasattr(response_text, 'content'):
            response_content = response_text.content
        else:
            response_content = str(response_text)
        
        # Get sources
        sources = [doc.metadata.get("id", "Unknown") for doc, _score in results]
        
        return {
            "success": True,
            "response": response_content,
            "sources": sources,
            "num_sources": len(sources)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error querying the model: {str(e)}",
            "response": "",
            "sources": []
        }

