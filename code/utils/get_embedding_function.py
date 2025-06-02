from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embedding_function():
    # Returns OpenAI embeddings function using text-embedding-3-small model.

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    
    # Use text-embedding-3-small - it's cost-effective and performs well
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
    
    return embeddings