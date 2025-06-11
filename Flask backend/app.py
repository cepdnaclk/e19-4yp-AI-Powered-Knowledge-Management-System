from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Functions
from utils.get_embedding_function import get_embedding_function
from utils.query_rag import query_rag
from utils.populate_db import populate_database
from utils.clear_db import clear_chroma_database

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  #  CORS for React frontend

CHROMA_PATH = "chroma"


# Health check endpoint 
@app.route('/', methods=['GET']) 
def health_check():
      
    return jsonify({   # Constructs a JSON response containing
        "status": "healthy",
        "message": "RAG Flask Server is running",
        "endpoints": {
            "query": "/api/query (POST)",
            "health": "/ (GET)",
            "status": "/api/status (GET)",
            "populate": "/api/populate (POST)"
        }
    })


@app.route('/api/status', methods=['GET']) 
def status_endpoint():
     
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

#  Main query endpoint for RAG system
@app.route('/api/query', methods=['POST'])
def query_endpoint():
    
    # Expected JSON: {"query": "your question here"}
  
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
        
        # Process the query using imported query_rag function
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

# Populate database endpoint
@app.route('/api/populate', methods=['POST'])
def populate_endpoint():
    """
    Populate the database with PDF documents
    Expected JSON: {"reset": true/false} (optional, defaults to false)
    """
    try:
        data = request.get_json() if request.is_json else {}
        reset = data.get('reset', False)
        
        # Process the database population using imported function
        result = populate_database(reset=reset)
        
        # Return appropriate status code
        status_code = 200 if result['success'] else 500
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500

# Clear database endpoint
@app.route('/api/clear-db', methods=['POST'])
def clear_db():
    try:
        result = clear_chroma_database()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    
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
   
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"reset\": true}'")
    print("  (reset: true clears existing database first)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)