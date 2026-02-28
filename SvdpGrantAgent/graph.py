from typing import TypedDict, Annotated, Sequence, Dict, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from SvdpGrantAgent.ingestion import KnowledgeIngestionFactory
from SvdpGrantAgent.writer import WriterAgent
from SvdpGrantAgent.schema import GrantRecord, GrantStatus
from SvdpGrantAgent.exporter import DocumentExportFactory

class AgentState(TypedDict):
    current_grant: GrantRecord
    evaluation: str
    is_relevant: bool
    draft_payload: Dict[str, str]
    human_approved: Optional[bool]
    human_feedback: Optional[str]
    export_path: Optional[str]

def scout_node(state: AgentState):
    """Scouts for info about the grant and mission fit."""
    print("--- SCOUTING ---")
    # In future, this would call an LLM to evaluate alignment
    return {"evaluation": "This grant aligns with our elderly outreach mission."}

def relevance_checker_node(state: AgentState):
    """Determines if the grant is worth pursuing."""
    print("--- CHECKING RELEVANCE ---")
    return {"is_relevant": True}

def writer_node(state: AgentState):
    """Drafts the application using the WriterAgent."""
    print("--- DRAFTING ---")
    writer = WriterAgent()
    # In a real implementation, generate_full_draft would take feedback into account
    feedback = state.get("human_feedback")
    draft = writer.generate_full_draft(state["current_grant"], feedback=feedback)
    return {"draft_payload": draft, "human_feedback": None} # Clear feedback after use

def human_review_node(state: AgentState):
    """
    A node that represents a pause for human review.
    """
    print("--- PENDING HUMAN REVIEW ---")
    return state

def export_node(state: AgentState):
    """Finalizes and exports the approved draft."""
    print("--- EXPORTING ---")
    # The original `exporter = DocumentExporter()` is removed as DocumentExportFactory uses static methods.
    path = DocumentExportFactory.export_to_pdf(state["draft_payload"], state["current_grant"].grant_id)
    return {"export_path": path}

def router(state: AgentState):
    if state["is_relevant"]:
        return "writer"
    return END

def post_review_router(state: AgentState):
    if state.get("human_approved") is True:
        return "export"
    elif state.get("human_approved") is False and state.get("human_feedback"):
        return "writer"
    return END

# Initialize checkpointer for state persistence
memory = MemorySaver()

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("scout", scout_node)
workflow.add_node("relevance", relevance_checker_node)
workflow.add_node("writer", writer_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("export", export_node)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "relevance")
workflow.add_conditional_edges("relevance", router, {"writer": "writer", "end": END})
workflow.add_edge("writer", "human_review")
workflow.add_conditional_edges(
    "human_review", 
    post_review_router, 
    {"export": "export", "writer": "writer", "end": END}
)
workflow.add_edge("export", END)

# Compile with checkpointer and interrupt
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]
)

def run_graph(grant: GrantRecord, thread_id: str = "1"):
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "current_grant": grant,
        "evaluation": "",
        "is_relevant": False,
        "draft_payload": {},
        "human_approved": None,
        "human_feedback": None,
        "export_path": None
    }
    # Run until the interrupt
    return graph.invoke(initial_state, config)

def approve_grant(thread_id: str):
    """Resumes the graph after human approval."""
    config = {"configurable": {"thread_id": thread_id}}
    graph.update_state(config, {"human_approved": True})
    return graph.invoke(None, config)

def request_rewrite(thread_id: str, feedback: str):
    """Requests a rewrite based on human feedback."""
    config = {"configurable": {"thread_id": thread_id}}
    graph.update_state(config, {"human_approved": False, "human_feedback": feedback})
    return graph.invoke(None, config)
