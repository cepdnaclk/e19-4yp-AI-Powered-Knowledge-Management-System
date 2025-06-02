from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from utils.get_embedding_function import get_embedding_function
from utils.query_rag import query_rag

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
    """
    Query the RAG system with the given text
    """
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

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "RAG Flask Server is running",
        "endpoints": {
            "query": "/api/query (POST)",
            "health": "/ (GET)",
            "status": "/api/status (GET)",
            "populate": "/api/populate (POST)"
        }
    })

@app.route('/api/query', methods=['POST'])
def query_endpoint():
    """
    Main query endpoint for RAG system
    Expected JSON: {"query": "your question here"}
    """
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({
                "success": False,
                "message": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        
        # Validate query parameter
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "message": "Missing 'query' parameter in request body"
            }), 400
        
        query_text = data['query'].strip()
        
        if not query_text:
            return jsonify({
                "success": False,
                "message": "Query cannot be empty"
            }), 400
        
        # Process the query
        result = query_rag(query_text)
        
        # Return appropriate status code
        status_code = 200 if result['success'] else 500
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}",
            "response": "",
            "sources": []
        }), 500

@app.route('/api/populate', methods=['POST'])
def populate_endpoint():
    """
    Populate the database with PDF documents
    Expected JSON: {"reset": true/false} (optional, defaults to false)
    """
    try:
        data = request.get_json() if request.is_json else {}
        reset = data.get('reset', False)
        
        # Process the database population
        result = populate_database(reset=reset)
        
        # Return appropriate status code
        status_code = 200 if result['success'] else 500
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500

@app.route('/api/status', methods=['GET'])
def status_endpoint():
    """
    Check if the database and embeddings are properly configured
    """
    try:
        # Check if OpenAI API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return jsonify({
                "success": False,
                "message": "OpenAI API key not configured"
            }), 500
        
        # Check if Chroma database exists
        if not os.path.exists(CHROMA_PATH):
            return jsonify({
                "success": False,
                "message": "Chroma database not found. Run populate_database.py first."
            }), 500
        
        # Try to initialize the database
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Get database stats
        collection = db.get()
        doc_count = len(collection['ids']) if collection['ids'] else 0
        
        return jsonify({
            "success": True,
            "message": "System is ready",
            "database_documents": doc_count,
            "chroma_path": CHROMA_PATH
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Configuration error: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Check environment variables on startup
    required_env_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        exit(1)
    
    # Check if database exists
    if not os.path.exists(CHROMA_PATH):
        print(f"⚠️  Warning: Chroma database not found at {CHROMA_PATH}")
        print("Run 'python populate_database.py' to create the database first")
    
    print("🚀 Starting RAG Flask Server...")
    print("📖 Available endpoints:")
    print("  GET  /              - Health check")
    print("  GET  /api/status    - System status")
    print("  POST /api/query     - Query the RAG system")
    print("  POST /api/populate  - Populate database with PDFs")
    print("\n💡 Example query:")
    print("  curl -X POST http://localhost:5000/api/query \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"query\": \"What is machine learning?\"}'")
    print("\n💡 Example populate:")
    print("  curl -X POST http://localhost:5000/api/populate \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"reset\": true}'")
    print("  (reset: true clears existing database first)")    
    app.run(debug=True, host='0.0.0.0', port=5000)