from typing import TypedDict, Optional, Any, Dict, List
from langgraph.graph import MessagesState

class EcosyncState(TypedDict):
    """Enhanced State schema for Ecosync AI multi-agent system with health support"""
    input: str                           # User input text
    image: Optional[str]                 # Base64 encoded image (if any)
    user_city: Optional[str]             # User's city for clinic suggestions
    agent_decision: Optional[str]        # Which agent to use
    response: Optional[str]              # Final response from selected agent
    clinic_data: Optional[List[Dict]]    # Nearby clinic information
    health_type: Optional[str]           # Type: 'human', 'marine', 'land', 'environmental'
    metadata: Optional[Dict[str, Any]]   # Additional metadata