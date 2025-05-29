---
layout: home
permalink: index.html

# Please update this with your repository name and title
repository-name: e19-4yp-AI-Powered-Knowledge-Management-System
title: AI powered knowledge management system
---

[comment]: # "This is the standard layout for the project, but you can clean this and use your own template"

# AI Powered Knowledge Management System

#### Team

- E/19/004, R.B.ABEYSINGHE, [email](mailto:e19004@eng.pdn.ac.lk)
- E/19/096, E.M.C.Y.B.EKANAYAKE, [email](mailto:e19096@eng.pdn.ac.lk)
- E/19/100, E.P.S.G.ELLAWALA, [email](mailto:e19100@eng.pdn.ac.lk)

#### Supervisors

- Dr. Asitha Bandaranayake, [email](mailto:asithab@eng.pdn.ac.lk)
- Prof Roshan Ragel, [email](mailto:roshanr@eng.pdn.ac.lk)

#### Table of content

1. [Abstract](#abstract)
2. [Related works](#related-works)
3. [Methodology](#methodology)
4. [Experiment Setup and Implementation](#experiment-setup-and-implementation)
5. [Results and Analysis](#results-and-analysis)
6. [Conclusion](#conclusion)
7. [Publications](#publications)
8. [Links](#links)

---

## Abstract

### Leveraging AI-Powered Knowledge Management Systems to Enhance Operational Efficiency

National Research and Education Networks (NRENs) play a crucial role in supporting academic and research communities
by providing advanced technological infrastructure and services. As these organizations grow in complexity, there is an
increasing need for efficient knowledge management systems to support their operations.

This research project aims to explore the potential of AI-powered knowledge management systems in enhancing the operational efficiency of NRENs, with a focus on managing:

- Institutional knowledge
- Training materials
- Administrative guidelines

## Related works

## Methodology

### Research Objectives

- **Primary Goal**: Develop an AI-powered knowledge management system tailored for NREN operations
- **Focus Areas**: Institutional knowledge preservation, training material organization, administrative guideline accessibility
- **Target Outcome**: Enhanced operational efficiency through intelligent information retrieval and management

## Experiment Setup and Implementation

### Technical Architecture

#### RAG (Retrieval-Augmented Generation) System

Our approach leverages RAG architecture to combine the benefits of large language models with domain-specific knowledge retrieval:

![ARG ARCHITECTURE](images/arg_arch.png)

#### Core Components

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

## Results and Analysis

### Current Progress

- **RAG Architecture Study**: Comprehensive analysis of Retrieval-Augmented Generation systems
- **Vector Embeddings Research**: Deep dive into semantic search and similarity matching techniques
- **Prototype Development**: Created small-scale chatbots for concept validation
- **Component Integration**: Successfully tested retrieval and generation workflows

## Conclusion

This research demonstrates the viability and advantages of AI-powered knowledge management systems in supporting the evolving needs of NRENs. By automating and enhancing knowledge retrieval and accessibility, such systems can significantly boost operational efficiency.

## Publications

[//]: # "Note: Uncomment each once you uploaded the files to the repository"

<!-- 1. [Semester 7 report](./) -->
<!-- 2. [Semester 7 slides](./) -->
<!-- 3. [Semester 8 report](./) -->
<!-- 4. [Semester 8 slides](./) -->
<!-- 5. Author 1, Author 2 and Author 3 'Research paper title' (2021). [PDF](./). -->

## Links

- [Project Repository](https://github.com/cepdnaclk/e19-4yp-AI-Powered-Knowledge-Management-System)
- [Project Page](https://cepdnaclk.github.io/e19-4yp-AI-Powered-Knowledge-Management-System)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)

---

## Technology Stack

### Language Models

- **Primary Requirement**: GPT-3.5 Turbo or GPT-4
- **Use Cases**:
  - Text generation and summarization
  - Query understanding and response synthesis
  - Context-aware information retrieval

### Vector Processing

- **Embedding Models**: OpenAI text-embedding-ada-002 or similar
- **Vector Database**: Pinecone, Weaviate, or Chroma
- **Similarity Search**: Cosine similarity, semantic matching

### Development Framework

```python
- Python 3.8+
- LangChain for LLM orchestration
- OpenAI API for language models
- Vector database (Pinecone/Weaviate)
- FastAPI for backend services
- React/Next.js for frontend interface
```
