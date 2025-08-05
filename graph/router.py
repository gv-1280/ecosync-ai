from typing import Dict

def router_node(state: Dict) -> str:
    """
    Decides which agent to route to based on presence of image or keywords.
    Returns the agent node name as a string.
    """
    user_input = state.get("input", "")
    image = state.get("image")

    if image:
        # Use input text to determine marine or land animal
        if "marine" in user_input.lower() or "ocean" in user_input.lower():
            return "marine_health_agent"

        elif "land" in user_input.lower() or "animal" in user_input.lower():
            return "land_health_agent"

        else:
            return "marine_health_agent"  # Default to marine if ambiguous
    elif user_input:
        return "eco_chatbot_agent"

    return "eco_chatbot_agent"  # Final fallback
