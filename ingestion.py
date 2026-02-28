import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .factories.db_factory import get_vector_store
from .guardrails import Guardrails
from dotenv import load_dotenv

load_dotenv()

def ingest_documents(file_paths: List[str]):
    """
    Parses documents, scrubs PII, and stores them in pgvector.
    """
    documents = []
    for file_path in file_paths:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        loaded_docs = loader.load()
        # Apply PII scrubbing guardrail
        for doc in loaded_docs:
            doc.page_content = Guardrails.scrub_pii(doc.page_content)
        
        documents.extend(loaded_docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)

    vectorstore = get_vector_store()
    
    vectorstore.add_documents(documents=splits)
    
    print(f"Ingested {len(splits)} chunks into the vector database after PII scrubbing.")

if __name__ == "__main__":
    # Example usage: ingest all files in a 'docs' directory
    docs_dir = "./docs"
    if os.path.exists(docs_dir):
        files = [os.path.join(docs_dir, f) for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
        ingest_documents(files)
    else:
        print(f"Directory {docs_dir} not found. Please create it and add SVdP documents.")

