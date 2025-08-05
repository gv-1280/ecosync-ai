from typing import Dict
from langgraph.graph import StateGraph
from utils.openrouter import call_openrouter_text_model

# Define the node function
def eco_chatbot_node(state: Dict) -> Dict:
    """
    Handles eco chatbot queries (e.g., coral bleaching, SDGs, eco-awareness).
    Uses Google Gemini 2.5 Flash Lite from OpenRouter.
    """
    user_input = state.get("input", "")

    if not user_input:
        response = "I didn't receive any input to process. Please provide a question or message."
    else:
        response = call_openrouter_text_model(user_input, model="mistralai/mistral-small-3.2-24b-instruct:free")

    # Update state with output
    return {"output": response}
