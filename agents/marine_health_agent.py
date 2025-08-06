from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_vision_model

def marine_health_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Marine Health Agent - analyzes images of marine life.
    MUST return a dictionary to update the state.
    """
    input_text = state.get("input", "")
    image = state.get("image")
    
    if not image:
        return {
            "response": "I need an image to analyze marine life health. Please upload an image of marine creatures or ocean environment.",
            "metadata": {
                "agent_used": "marine_health_agent",
                "success": False,
                "error": "No image provided"
            }
        }
    
    system_prompt = """You are a marine biology expert specializing in ocean health assessment. 
    Analyze the provided image for:
    - Marine species identification
    - Health indicators (signs of disease, bleaching, etc.)
    - Environmental threats (pollution, temperature stress)
    - Conservation recommendations
    
    Provide detailed, scientific analysis while being accessible to general audiences."""
    
    try:
        response = call_vision_model(
            model="moonshotai/kimi-vl-a3b-thinking:free",
            system_prompt=system_prompt,
            user_prompt=input_text or "Please analyze this marine environment image for health indicators and potential threats.",
            image_base64=image
        )
        
        return {
            "response": response,
            "metadata": {
                "agent_used": "marine_health_agent",
                "model": "moonshotai/kimi-vl-a3b-thinking:free",
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I encountered an error while analyzing the marine image: {str(e)}",
            "metadata": {
                "agent_used": "marine_health_agent",
                "success": False,
                "error": str(e)
            }
        }