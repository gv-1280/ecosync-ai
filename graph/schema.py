from typing import TypedDict, Optional, Any, Dict
from langgraph.graph import MessagesState

class EcosyncState(TypedDict):
    """State schema for Ecosync AI multi-agent system"""
    input: str                    # User input text
    image: Optional[str]         # Base64 encoded image (if any)
    agent_decision: Optional[str] # Which agent to use
    response: Optional[str]      # Final response from selected agent
    metadata: Optional[Dict[str, Any]]  # Additional metadata
