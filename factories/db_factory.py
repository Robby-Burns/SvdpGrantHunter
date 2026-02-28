import os
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

def get_vector_store(collection_name: str = "svdp_knowledge_base"):
    """
    Creates a vector store instance based on environment configuration.
    """
    # For this project, we primarily use PGVector as per AgentSpec
    connection_string = os.getenv("DATABASE_URL", "postgresql+psycopg2://localhost/svdp_grants")
    embeddings = OpenAIEmbeddings()
    
    return PGVector(
        connection_string=connection_string,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

def get_db_connection():
    """
    Returns a raw psycopg2 connection for standard SQL operations.
    """
    import psycopg2
    connection_string = os.getenv("DATABASE_URL", "postgresql+psycopg2://localhost/svdp_grants")
    # psycopg2 expects 'postgresql://' not 'postgresql+psycopg2://'
    if "+psycopg2" in connection_string:
        connection_string = connection_string.replace("+psycopg2", "")
    
    return psycopg2.connect(connection_string)
