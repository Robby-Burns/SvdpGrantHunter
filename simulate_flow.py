import json
from .schema import GrantRecord, GrantStatus
from .graph import run_graph, approve_grant, graph

def simulate_full_flow():
    """
    Simulates the full agentic flow including scouting, drafting, HITL, and export.
    """
    print("=== STARTING SVDP GRANT AGENT SIMULATION ===\n")

    # 1. Create a sample grant record
    sample_grant = GrantRecord(
        grant_id="3Rivers_YouthSuccess_2026",
        grant_source_url="https://3riverscf.org/grants/youth-success",
        extracted_requirements=["Mission Statement", "Budget Breakdown"],
        status=GrantStatus.SCOUTED
    )

    print(f"Scout found a new grant: {sample_grant.grant_id}")
    
    # 2. Run the LangGraph workflow until the human review interrupt
    print("Running LangGraph workflow...")
    # Using a MagicMock for the checkpointer/memory in simulation if needed, 
    # but run_graph handles initialization.
    thread_id = "sim_thread_123"
    run_graph(sample_grant, thread_id=thread_id)
    
    # Get state to show the draft
    state = graph.get_state({"configurable": {"thread_id": thread_id}})
    print("\nStep 1: [scout_node] -> Analyzing grant mission fit...")
    print(f"Result: {state.values.get('evaluation')}\n")

    print("Step 2: [relevance_node] -> Determining ROI...")
    print(f"Result: Relevant? {state.values.get('is_relevant')}\n")

    print("Step 3: [writer_node] -> Generating drafts using RAG context...")
    for req, draft in state.values.get("draft_payload", {}).items():
        print(f"--- Draft for '{req}':")
        # In simulation without live RAG, this might be empty strings or placeholder logic
        print(f"    {draft[:100] if draft else '[MOCKED CONTENT]'}\n")

    print("--- [HUMAN-IN-THE-LOOP INTERRUPT] ---")
    print("Simulating human approval...")
    
    # 3. Resume the graph with approval
    final_state = approve_grant(thread_id)
    
    print("\nStep 4: [export_node] -> Finalizing and Exporting...")
    print(f"Export Path: {final_state.values.get('export_path')}")

    print("\n=== SIMULATION COMPLETE ===")

if __name__ == "__main__":
    simulate_full_flow()
