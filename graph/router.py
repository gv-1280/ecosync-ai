import base64
from typing import Dict, Any
from graph.schema import EcosyncState

def router_node(state: EcosyncState) -> Dict[str, Any]:
    """
    Router node that decides which agent to use.
    MUST return a dictionary to update the state.
    """
    input_text = state.get("input", "").lower()
    image = state.get("image")
    
    # Decision logic
    if image:
        # Image is present - decide between marine or land agent
        marine_keywords = ["ocean", "sea", "marine", "fish", "coral", "whale", "dolphin", "shark"]
        land_keywords = ["forest", "land", "animal", "wildlife", "bird", "mammal", "tree"]
        
        if any(keyword in input_text for keyword in marine_keywords):
            agent_decision = "marine_health_agent"
        elif any(keyword in input_text for keyword in land_keywords):
            agent_decision = "land_health_agent"
        else:
            # Default to marine for images if ambiguous
            agent_decision = "marine_health_agent"
    else:
        # No image - use eco chatbot
        agent_decision = "eco_chatbot_agent"
    
    # CRITICAL: Must return a dictionary that updates the state
    return {
        "agent_decision": agent_decision,
        "metadata": {
            "routing_reason": f"Selected {agent_decision} based on input analysis",
            "has_image": image is not None
        }
    }