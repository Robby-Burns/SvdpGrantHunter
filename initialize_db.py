import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def initialize_database():
    """
    Initializes the Postgres database with the vector extension and necessary tables.
    """
    connection_string = os.getenv("DATABASE_URL")
    if not connection_string:
        print("Error: DATABASE_URL not found in environment.")
        return

    try:
        # Connect to the database
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cur = conn.cursor()

        print("Enabling vector extension...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        print("Creating 'grants' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS grants (
                grant_id TEXT PRIMARY KEY,
                grant_source_url TEXT NOT NULL,
                extracted_requirements JSONB DEFAULT '[]',
                draft_payload JSONB DEFAULT '{}',
                human_feedback TEXT,
                status TEXT DEFAULT 'Scouted',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("Creating 'organization_facts' table...")
        # Note: langchain's PGVector usually handles its own 'langchain_pg_collection' and 'langchain_pg_embedding' tables,
        # but we ensure our custom schema co-exists.
        print("Database initialized successfully.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error during database initialization: {e}")

if __name__ == "__main__":
    initialize_database()
