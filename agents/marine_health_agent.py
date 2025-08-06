from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_vision_model
from utils.clinic_finder import find_nearby_clinics

def enhanced_marine_health_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Enhanced Marine Health Agent with human health impact analysis
    """
    input_text = state.get("input", "")
    image = state.get("image")
    health_type = state.get("health_type", "marine")
    user_city = state.get("user_city", "")
    
    if not image:
        return {
            "response": "I need an image to analyze marine life health. Please upload an image of marine creatures or ocean environment.",
            "metadata": {"agent_used": "marine_health_agent", "success": False, "error": "No image provided"}
        }
    
    # Enhanced system prompt based on health type
    if health_type == "environmental_marine":
        system_prompt = """You are a marine biology and public health expert. 
        Analyze the marine environment image for:
        
        MARINE ECOSYSTEM HEALTH:
        - Marine species identification and health indicators
        - Water quality and pollution signs
        - Coral reef health and bleaching
        - Marine biodiversity assessment
        
        HUMAN HEALTH IMPACTS:
        - Water contamination that could affect human health
        - Harmful algal blooms or toxins
        - Pollution sources affecting drinking water
        - Seafood safety concerns
        - Beach safety and water recreation risks
        
        Provide comprehensive analysis linking marine health to human wellbeing."""
    else:
        system_prompt = """You are a marine biology expert specializing in ocean health assessment. 
        Analyze the provided image for:
        - Marine species identification and health indicators
        - Environmental threats (pollution, temperature stress, overfishing)
        - Coral reef health and ecosystem balance
        - Conservation recommendations and action steps
        
        Provide detailed, scientific analysis accessible to general audiences."""
    
    try:
        response = call_vision_model(
            model="moonshotai/kimi-vl-a3b-thinking:free",
            system_prompt=system_prompt,
            user_prompt=input_text or "Please analyze this marine environment for health indicators and potential human health impacts.",
            image_base64=image
        )
        
        # Add clinic suggestions if environmental health concerns detected
        clinic_suggestions = ""
        clinic_data = []
        
        if health_type == "environmental_marine" and user_city:
            # Check if response mentions health concerns
            health_concern_keywords = ["contamination", "pollution", "toxic", "harmful", "unsafe", "health risk"]
            if any(keyword in response.lower() for keyword in health_concern_keywords):
                clinic_data = find_nearby_clinics(user_city)
                if clinic_data:
                    clinic_suggestions = f"\n\n⚠️ **Health Precaution - Healthcare Facilities in {user_city}:**\n\n"
                    for clinic in clinic_data[:2]:  # Show top 2 for environmental concerns
                        clinic_suggestions += f"**{clinic['name']}** - {clinic['phone']}\n"
                    clinic_suggestions += "\n*Consult healthcare providers if you experience symptoms related to environmental exposure.*"
        
        full_response = response + clinic_suggestions
        
        return {
            "response": full_response,
            "clinic_data": clinic_data,
            "metadata": {
                "agent_used": "marine_health_agent",
                "model": "moonshotai/kimi-vl-a3b-thinking:free",
                "health_type": health_type,
                "environmental_health_analysis": health_type == "environmental_marine",
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I encountered an error while analyzing the marine image: {str(e)}",
            "metadata": {"agent_used": "marine_health_agent", "success": False, "error": str(e)}
        }