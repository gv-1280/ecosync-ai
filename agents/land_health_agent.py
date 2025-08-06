from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_vision_model

def land_health_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Land Health Agent - analyzes images of terrestrial animals and environments.
    MUST return a dictionary to update the state.
    """
    input_text = state.get("input", "")
    image = state.get("image")
    
    if not image:
        return {
            "response": "I need an image to analyze land-based wildlife health. Please upload an image of animals or terrestrial environments.",
            "metadata": {
                "agent_used": "land_health_agent",
                "success": False,
                "error": "No image provided"
            }
        }
    
    system_prompt = """You are a wildlife and terrestrial ecology expert. 
    Analyze the provided image for:
    - Species identification
    - Animal health indicators
    - Habitat quality assessment
    - Environmental threats (deforestation, pollution, climate impact)
    - Conservation status and recommendations
    
    Provide comprehensive analysis that supports wildlife conservation efforts."""
    
    try:
        response = call_vision_model(
            model="moonshotai/kimi-vl-a3b-thinking:free",
            system_prompt=system_prompt,
            user_prompt=input_text or "Please analyze this terrestrial environment/wildlife image for health indicators and conservation insights.",
            image_base64=image
        )
        
        return {
            "response": response,
            "metadata": {
                "agent_used": "land_health_agent",
                "model": "moonshotai/kimi-vl-a3b-thinking:free",
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I encountered an error while analyzing the land-based image: {str(e)}",
            "metadata": {
                "agent_used": "land_health_agent",
                "success": False,
                "error": str(e)
            }
        }