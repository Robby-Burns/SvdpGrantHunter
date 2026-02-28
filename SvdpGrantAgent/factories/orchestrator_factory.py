from typing import Dict, Any, Optional
from SvdpGrantAgent.graph import graph, run_graph, approve_grant
from SvdpGrantAgent.schema import GrantRecord

class OrchestratorFactory:
    """
    Factory for interacting with the LangGraph orchestrator.
    Ensures the UI remains decoupled from the specific graph implementation.
    """
    
    @staticmethod
    def get_orchestrator():
        """Returns the compiled LangGraph instance."""
        return graph

    @staticmethod
    def start_process(grant: GrantRecord, thread_id: str = "1") -> Dict[str, Any]:
        """Initiates the grant processing workflow."""
        return run_graph(grant, thread_id)

    @staticmethod
    def approve_step(thread_id: str) -> Dict[str, Any]:
        """Resumes the process after human approval."""
        return approve_grant(thread_id)

    @staticmethod
    def request_rewrite(thread_id: str, feedback: str) -> Dict[str, Any]:
        """Requests a rewrite based on human feedback."""
        from SvdpGrantAgent.graph import request_rewrite as rr
        return rr(thread_id, feedback)

    @staticmethod
    def get_state(thread_id: str) -> Dict[str, Any]:
        """Retrieves the current state of a specific thread."""
        config = {"configurable": {"thread_id": thread_id}}
        return graph.get_state(config).values
