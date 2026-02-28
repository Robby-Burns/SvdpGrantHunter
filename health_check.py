import sys
import os
from dotenv import load_dotenv

load_dotenv()

def run_health_check():
    """
    Performs a basic check of system dependencies and connectivity.
    Exits with 0 if healthy, non-zero otherwise.
    """
    print("--- SVdP Grant Agent Health Check ---")
    
    # 1. Check Python Version
    print(f"Python Version: {sys.version}")
    
    # 2. Check Core Imports (Ensures environment is set up)
    try:
        import streamlit
        import langchain
        from SvdpGrantAgent.factories.db_factory import get_db_connection
        print("✅ Core dependencies imported successfully.")
    except ImportError as e:
        print(f"❌ Dependency Error: {e}")
        sys.exit(1)
        
    # 3. Check Database Connectivity
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        print("✅ Database connection established.")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        # We don't exit here necessarily if the DB isn't strictly required for boot,
        # but for this agent it is.
        sys.exit(1)

    print("--- Status: HEALTHY ---")
    sys.exit(0)

if __name__ == "__main__":
    run_health_check()
