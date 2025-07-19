"""
populate_database.py  •  v3
—————————————————————————————————
Loads all PDF documents from the data/ folder.
Splits each PDF into small chunks (~800 characters).
Uses GPT-3.5-turbo to:
Classify each chunk's audience (e.g., developer, manager)
Identify topics (e.g., AI, Python)
Stores each chunk (with embeddings + metadata) in Chroma, a vector database.
Optionally clears the database if reset=True.

In here meta data is like 
{
  "source": "data/sample.pdf",
  "chunk_id": "data/sample.pdf:3:2",
  "audience": "developer,manager",
  "topics": "authentication,api"
}


"""

import os, json, re, shutil
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_openai import ChatOpenAI          # NEW
from dotenv import load_dotenv                   # NEW
from langchain_chroma import Chroma

from utils.get_embedding_function import get_embedding_function

load_dotenv()  # make sure OPENAI_API_KEY is available

CHROMA_PATH = "chroma"
DATA_PATH   = "data"


# 1.  LLM & tag vocabulary

LLM = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

ROLE_SET  = [
    "developer", "manager", "admin", "support", "customer", "researcher",
    "general"
]
TOPIC_SET = [
    "AI", "ML", "Python", "Finance", "Technical", "Security", "DevOps"
]

def classify_chunk(text: str) -> dict:
    """
    Call GPT-3.5-turbo once for the chunk and return
    {'audience': [...], 'topics': [...]}.
    Falls back to {'general', []} on any error.
    """
    # shrink long chunks to ~800 chars to save tokens
    sample = re.sub(r"\s+", " ", text)[:800]

    prompt = (
        "Identify the primary audience role(s) (choose from: "
        f"{', '.join(ROLE_SET)}) and up to three topics "
        f"(choose from: {', '.join(TOPIC_SET)}) relevant to "
        "the content below. Respond ONLY in valid JSON like "
        '{"audience":["role"],"topics":["topic"]}.\n\n'
        f"CONTENT:\n\"\"\"\n{sample}\n\"\"\""
    )

    try:
        resp   = LLM.invoke(prompt)
        parsed = json.loads(resp.content)

        audience = [r for r in parsed.get("audience", []) if r in ROLE_SET]
        topics   = [t for t in parsed.get("topics", [])   if t in TOPIC_SET]

        return {"audience": audience or ["general"], "topics": topics}
    except Exception:
        return {"audience": ["general"], "topics": []}


# 2.  ETL helpers (mostly unchanged)

def load_documents() -> List[Document]:
    return PyPDFDirectoryLoader(DATA_PATH).load()

def split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=80, length_function=len
    )
    return splitter.split_documents(docs)

def calculate_chunk_ids(chunks: List[Document]) -> List[Document]:
    last_page_id, idx = None, 0
    for c in chunks:
        src  = c.metadata.get("source")
        page = c.metadata.get("page")
        page_id = f"{src}:{page}"

        idx = idx + 1 if page_id == last_page_id else 0
        c.metadata["id"] = f"{page_id}:{idx}"
        last_page_id = page_id
    return chunks

def tag_chunks(chunks: list[Document]) -> list[Document]:
    for c in chunks:
        tags = classify_chunk(c.page_content)          # returns {'audience': [...], 'topics': [...]}

        # ----- flatten to scalars -----
        c.metadata["audience"] = ",".join(tags["audience"])   # 'developer,researcher'
        c.metadata["topics"]   = ",".join(tags["topics"])     # 'AI,Python'
    return chunks

# Stores the chunks in a Chroma vector database
# Prevents duplication by checking if chunk ID already exists.

def add_to_chroma(chunks: List[Document]) -> int:
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())

    chunks = calculate_chunk_ids(chunks)
    chunks = tag_chunks(chunks)                # ← NEW: content-based tags

    existing_ids = set(db.get(include=[])["ids"])
    new_chunks   = [c for c in chunks if c.metadata["id"] not in existing_ids]

    if not new_chunks:
        print("✅ No new documents to add")
        return 0

    print(f"👉 Adding new documents: {len(new_chunks)}")
    db.add_documents(new_chunks, ids=[c.metadata["id"] for c in new_chunks])
    print("✅ Documents added and persisted automatically")
    return len(new_chunks)


# 3.  CLI wrapper (unchanged API)

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

def populate_database(reset: bool = False):
    try:
        if reset:
            print("✨ Clearing Database")
            clear_database()

        if not os.path.exists(DATA_PATH):
            return {"success": False,
                    "message": f"Data directory '{DATA_PATH}' not found."}

        docs = load_documents()
        if not docs:
            return {"success": False,
                    "message": "No PDF documents found in data/."}

        chunks         = split_documents(docs)
        new_docs_added = add_to_chroma(chunks)

        msg = ("Database populated successfully"
               if new_docs_added else
               "No new documents were added. All documents already exist.")

        return {
            "success": True,
            "message": msg,
            "documents_processed": len(docs),
            "chunks_created": len(chunks),
            "new_documents_added": new_docs_added,
        }

    except Exception as exc:
        return {"success": False,
                "message": f"Error populating database: {exc}"}

if __name__ == "__main__":
    print(populate_database(reset=False))
