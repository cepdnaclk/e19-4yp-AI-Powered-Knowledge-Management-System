import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from get_embedding_function import get_embedding_function

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5) # Limit to top 5 results 
    
    if not results:
        print("No relevant documents found in the database.")
        return "No relevant information found."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Uncomment the line below to see the full prompt being sent
    # print("DEBUG - Prompt being sent:")
    # print(prompt)
    # print("\n" + "="*50 + "\n")

    # Initialize OpenAI Chat model
    model = ChatOpenAI(
        model="gpt-3.5-turbo",  
        temperature=0,  # Lower temperature for more consistent responses
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        response_text = model.invoke(prompt)
        
        # Extract the content from the response
        if hasattr(response_text, 'content'):
            response_content = response_text.content
        else:
            response_content = str(response_text)
        
        sources = [doc.metadata.get("id", None) for doc, _score in results]
        
        # Format and display the response
        formatted_response = f"Response: {response_content}\n\nSources: {sources}"
        print(formatted_response)
        
        return response_content
        
    except Exception as e:
        error_msg = f"Error querying the model: {str(e)}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    main()