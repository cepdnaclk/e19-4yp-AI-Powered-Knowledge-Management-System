---
# Leveraging AI-Powered Knowledge Management Systems to Enhance Operational Efficiency
---

National Research and Education Networks (NRENs) play a crucial role in supporting academic and research communities
by providing advanced technological infrastructure and services. As these organizations grow in complexity, there is an
increasing need for efficient knowledge management systems to support their operations. This research project aims to explore
the potential of AI-powered knowledge management systems in enhancing the operational efficiency of NRENs, with a
focus on managing institutional knowledge, training materials, and administrative guidelines.

This research project aims to explore the potential of AI-powered knowledge management systems in enhancing the operational efficiency of NRENs, with a focus on managing:

- Institutional knowledge
- Training materials
- Administrative guidelines

## Research Objectives

- **Primary Goal**: Develop an AI-powered knowledge management system tailored for NREN operations
- **Focus Areas**: Institutional knowledge preservation, training material organization, administrative guideline accessibility
- **Target Outcome**: Enhanced operational efficiency through intelligent information retrieval and management

## Technical Architecture

### RAG (Retrieval-Augmented Generation) System

Our approach leverages RAG architecture to combine the benefits of large language models with domain-specific knowledge retrieval:

![ARG ARCHITECTURE](docs/images/arg_arch.png)

### Core Components

1. **Document Processing Pipeline**

   - Text extraction from various formats (PDF, DOC, HTML)
   - Chunking and preprocessing
   - Vector embedding generation

2. **Vector Database**

   - Semantic search capabilities
   - Efficient similarity matching
   - Scalable storage for large document collections

3. **Language Model Integration**
   - Context-aware response generation
   - Query understanding and refinement
   - Multi-turn conversation support


## Technology Stack

### Language Models

- **Embeddings:** `text-embedding-3-small` (cost-effective)
- **Chat:** `gpt-3.5-turbo` (good balance of cost and performance)

**Use Cases**:
  - Text generation and summarization
  - Query understanding and response synthesis
  - Context-aware information retrieval

- **Vector Database:** `Chroma`
- **Similarity Search:** `Cosine similarity, semantic matching``

### Development Framework

- LangChain for LLM orchestration
- OpenAI API for language models
- Vector database (Chroma)
- Flask/Python for backend services
- React for frontend interface


## Setup Instructions

### 1. Clone this repository:
   ```bash
   git clone https://github.com/cepdnaclk/e19-4yp-AI-Powered-Knowledge-Management-System.git
   ```

### 2. Navigate to the Code Folder

```bash
cd code
```

### 3. Create Python Environment and Activate It

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Create .env File with API Key

Create a `.env` file in the project root directory:

```bash
echo. > .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 6. Populate ChromaDB with PDFs

Place your PDF files in the `data/` folder, then run:

```bash
python populate_database.py
```

**Optional:** Add more PDFs to the `data/` folder and run the command again to update the database.


### 7. Query Your Documents

Run queries against your document database:

```bash
python query_data.py "What is the main topic discussed in the documents?"
```




