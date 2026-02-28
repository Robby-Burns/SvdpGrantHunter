from .graph import graph, run_graph, approve_grant
from .schema import GrantRecord, GrantStatus

def run_cli_review_session():
    """
    A CLI tool to demonstrate the HITL cycle.
    """
    print("=== SVDP GRANT AGENT: CLI REVIEW SESSION ===\n")
    
    # 1. Start the process
    sample_grant = GrantRecord(
        grant_id="3Rivers_Youth_2026",
        grant_source_url="https://3riverscf.org/grants",
        extracted_requirements=["Mission Statement", "Impact"]
    )
    
    thread_id = "test_thread_001"
    print(f"Starting workflow for {sample_grant.grant_id}...")
    
    # Run until interrupt
    run_graph(sample_grant, thread_id=thread_id)
    
    state = graph.get_state({"configurable": {"thread_id": thread_id}})
    
    print("\n--- VOLUNTEER REVIEW REQUIRED ---")
    print(f"Grant: {state.values['current_grant'].grant_id}")
    print("Drafted Content:")
    for req, draft in state.values.get("draft_payload", {}).items():
        print(f"[{req}]: {draft[:100]}...")
        
    choice = input("\nAction: [A]pprove / [T]rash / [E]dit? ").strip().upper()
    
    if choice == 'A':
        print("Approving grant...")
        # In a real app, we might update state with human_approved=True
        # and then resume the graph.
        approve_grant(thread_id)
        print("Status: Approved and ready for export.")
    elif choice == 'T':
        print("Grant trashed.")
    else:
        print("Manual editing not implemented in CLI.")

if __name__ == "__main__":
    run_cli_review_session()
