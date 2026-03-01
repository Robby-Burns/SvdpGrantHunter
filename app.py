import streamlit as st
import uuid
from SvdpGrantAgent.factories.orchestrator_factory import OrchestratorFactory
from SvdpGrantAgent.scout import run_scout_job
from SvdpGrantAgent.schema import GrantRecord, GrantStatus

# --- PAGE CONFIG & STYLING (GRANDMOTHER MODE) ---
st.set_page_config(page_title="SVdP Grant Assistant", layout="wide")

# Inject CUSTOM CSS for Large Fonts, High Contrast, and Massive Buttons
st.markdown("""
    <style>
    /* Global Font Scaling */
    html, body, [class*="css"] {
        font-size: 24px !important;
        font-family: 'Open Sans', sans-serif !important;
    }
    
    /* Headers */
    h1 { font-size: 48px !important; color: #008751 !important; }
    h2 { font-size: 36px !important; color: #008751 !important; }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 32px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        margin: 10px 0px;
    }
    
    /* Green Approve Button */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #008751 !important;
        color: white !important;
    }
    
    /* Rewrite Button - Less prominent / Second Brand Color or darker Green */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #064E3B !important;
        color: white !important;
    }

    /* Cards */
    .grant-card {
        background-color: #F3F4F6;
        padding: 30px;
        border-radius: 20px;
        border: 4px solid #D1D5DB;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "step" not in st.session_state:
    st.session_state.step = "scout"
if "scouted_grants" not in st.session_state:
    st.session_state.scouted_grants = []
if "current_grant" not in st.session_state:
    st.session_state.current_grant = None
if "draft_results" not in st.session_state:
    st.session_state.draft_results = {}

# --- SIDEBAR STATUS (GRANDMOTHER MODE ACCESSIBILITY) ---
with st.sidebar:
    st.markdown("## 🛡️ System Status")
    try:
        from SvdpGrantAgent.factories.db_factory import get_db_connection
        conn = get_db_connection()
        conn.close()
        st.success("✅ Database: Connected")
    except Exception:
        st.error("❌ Database: Offline")
    
    st.info("Conference: St. Pats")
    st.write("---")
    if st.button("RESET SESSION"):
        st.session_state.step = "scout"
        st.rerun()

# --- HELPER FUNCTIONS ---
def start_drafting(grant):
    st.session_state.current_grant = grant
    st.session_state.step = "drafting"
    # Initiate the LangGraph process via Factory
    OrchestratorFactory.start_process(grant, thread_id=st.session_state.thread_id)
    st.rerun()

def handle_approve():
    OrchestratorFactory.approve_step(st.session_state.thread_id)
    st.session_state.step = "finished"
    st.rerun()

def handle_rewrite(feedback):
    if not feedback:
        st.error("Please explain what you want changed before clicking Rewrite.")
        return
    OrchestratorFactory.request_rewrite(st.session_state.thread_id, feedback)
    st.rerun()

def fetch_scouted_grants():
    try:
        from SvdpGrantAgent.factories.db_factory import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT grant_id, grant_source_url, status FROM grants ORDER BY created_at DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [GrantRecord(grant_id=r[0], grant_source_url=r[1], status=GrantStatus(r[2])) for r in rows]
    except Exception as e:
        print(f"Warning: Could not fetch from DB: {e}")
        return []

# --- MAIN UI ---
st.title("👵 SVdP Grant Assistant (St. Pats)")

if st.session_state.step == "scout":
    st.header("Step 1: Find Grant Opportunities")
    
    if st.button("🔍 CHECK FOR NEW GRANTS"):
        with st.spinner("Searching foundation databases..."):
            run_scout_job()
            st.session_state.scouted_grants = fetch_scouted_grants()
    
    # Always load from DB on page load if empty
    if not st.session_state.scouted_grants:
        st.session_state.scouted_grants = fetch_scouted_grants()

    if st.session_state.scouted_grants:
        for grant in st.session_state.scouted_grants:
            with st.container():
                st.markdown(f"""
                <div class="grant-card">
                    <h3>ID: {grant.grant_id}</h3>
                    <p>Source: <a href="{grant.grant_source_url}">{grant.grant_source_url}</a></p>
                    <p>Status: <b>{grant.status}</b></p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Draft Application for {grant.grant_id}", key=grant.grant_id):
                    start_drafting(grant)

elif st.session_state.step == "drafting":
    st.header("Step 2: Review and Perfect the Draft")
    
    # Retrieve current state from LangGraph
    state = OrchestratorFactory.get_state(st.session_state.thread_id)
    draft = state.get("draft_payload", {})
    
    if not draft:
        st.warning("The AI is still drafting... please refresh in a moment.")
    else:
        st.info("Edit the text below if needed, or ask the AI to rewrite a section.")
        
        # Display each requirement as an editable text area
        updated_draft = {}
        for section, content in draft.items():
            st.subheader(f"Section: {section}")
            updated_draft[section] = st.text_area(f"Verify {section}:", value=content, height=300, key=f"edit_{section}")
        
        st.divider()
        
        # Action Buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ EVERYTHING LOOKS GOOD - APPROVE"):
                handle_approve()
        
        with col2:
            feedback = st.text_input("What should the AI change?", placeholder="e.g. 'Make it more professional' or 'Add more about our food bank impact'")
            if st.button("🔄 REQUEST AI REWRITE"):
                handle_rewrite(feedback)

elif st.session_state.step == "finished":
    st.balloons()
    st.header("🎉 Application Approved!")
    
    state = OrchestratorFactory.get_state(st.session_state.thread_id)
    path = state.get("export_path")
    
    st.success(f"Final document is ready for download.")
    if path:
        st.write(f"📁 **Location:** {path}")
    
    if st.button("GO BACK TO START"):
        st.session_state.step = "scout"
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
