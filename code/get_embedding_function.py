from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_embedding_function():
    """
    Returns OpenAI embeddings function using text-embedding-3-small model.
    
    Make sure to set your OpenAI API key as an environment variable:
    export OPENAI_API_KEY='your-api-key-here'
    
    Or create a .env file with:
    OPENAI_API_KEY=your-api-key-here
    """
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    
    # Use text-embedding-3-small - it's cost-effective and performs well
    # Alternative: text-embedding-3-large for higher performance but higher cost
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
    
    return embeddings