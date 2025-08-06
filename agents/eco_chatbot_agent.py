from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_text_model

def eco_chatbot_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Eco Chatbot Agent - handles general environmental Q&A.
    MUST return a dictionary to update the state.
    """
    input_text = state.get("input", "")
    
    # Prepare the prompt
    system_prompt = """You are an environmental expert chatbot. 
    Answer questions about environmental conservation, climate change, 
    sustainability, and ecological issues. Provide accurate, helpful information 
    to promote environmental awareness."""
    
    try:
        # Call the model
        response = call_text_model(
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            system_prompt=system_prompt,
            user_prompt=input_text
        )
        
        # CRITICAL: Must return a dictionary
        return {
            "response": response,
            "metadata": {
                "agent_used": "eco_chatbot_agent",
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
            "metadata": {
                "agent_used": "eco_chatbot_agent",
                "success": False,
                "error": str(e)
            }
        }