from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_vision_model
from utils.clinic_finder import find_nearby_clinics

def enhanced_land_health_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Enhanced Land Health Agent with environmental health impact analysis
    """
    input_text = state.get("input", "")
    image = state.get("image")
    health_type = state.get("health_type", "land")
    user_city = state.get("user_city", "")
    
    if not image:
        return {
            "response": "I need an image to analyze terrestrial wildlife and environmental health. Please upload an image.",
            "metadata": {"agent_used": "land_health_agent", "success": False, "error": "No image provided"}
        }
    
    # Enhanced system prompt based on health type
    if health_type == "environmental_land":
        system_prompt = """You are a terrestrial ecology and environmental health expert. 
        Analyze the land-based image for:
        
        ECOSYSTEM HEALTH:
        - Wildlife species identification and health indicators
        - Habitat quality and environmental threats
        - Air quality indicators (vegetation health, pollution signs)
        - Biodiversity assessment
        
        HUMAN HEALTH IMPACTS:
        - Air pollution sources and effects
        - Soil contamination risks
        - Vector-borne disease habitats (mosquitoes, ticks)
        - Allergen sources (pollen, mold)
        - Safe outdoor recreation assessment
        
        Connect terrestrial environmental health to human wellbeing."""
    else:
        system_prompt = """You are a wildlife and terrestrial ecology expert. 
        Analyze the provided image for:
        - Species identification and animal health indicators
        - Habitat quality and environmental pressures
        - Conservation status and threats
        - Ecosystem balance and biodiversity
        - Climate change impacts on terrestrial life
        
        Provide comprehensive analysis supporting wildlife conservation."""
    
    try:
        response = call_vision_model(
            model="moonshotai/kimi-vl-a3b-thinking:free",
            system_prompt=system_prompt,
            user_prompt=input_text or "Please analyze this terrestrial environment for health indicators and potential human health impacts.",
            image_base64=image
        )
        
        # Add clinic suggestions for environmental health concerns
        clinic_suggestions = ""
        clinic_data = []
        
        if health_type == "environmental_land" and user_city:
            # Check for health-related environmental concerns
            health_concern_keywords = ["air pollution", "contamination", "allergen", "toxic", "disease vector", "health risk"]
            if any(keyword in response.lower() for keyword in health_concern_keywords):
                clinic_data = find_nearby_clinics(user_city)
                if clinic_data:
                    clinic_suggestions = f"\n\n🌿 **Environmental Health - Healthcare Options in {user_city}:**\n\n"
                    for clinic in clinic_data[:2]:
                        clinic_suggestions += f"**{clinic['name']}** - {clinic['phone']}\n"
                    clinic_suggestions += "\n*Seek medical advice for environmental health concerns or persistent symptoms.*"
        
        full_response = response + clinic_suggestions
        
        return {
            "response": full_response,
            "clinic_data": clinic_data,
            "metadata": {
                "agent_used": "land_health_agent", 
                "model": "moonshotai/kimi-vl-a3b-thinking:free",
                "health_type": health_type,
                "environmental_health_analysis": health_type == "environmental_land",
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I encountered an error while analyzing the land-based image: {str(e)}",
            "metadata": {"agent_used": "land_health_agent", "success": False, "error": str(e)}
        }
