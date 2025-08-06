from typing import Dict, Any
from graph.schema import EcosyncState
from utils.openrouter import call_text_model
from utils.clinic_finder import find_nearby_clinics

def enhanced_eco_chatbot_agent(state: EcosyncState) -> Dict[str, Any]:
    """
    Enhanced Eco Chatbot Agent with human health support and clinic suggestions
    """
    input_text = state.get("input", "")
    health_type = state.get("health_type", "environmental")
    user_city = state.get("user_city", "")
    
    # Adjust system prompt based on health type
    if health_type == "human":
        system_prompt = """You are an environmental and public health expert. 
        You help with health-related questions, especially those connected to environmental factors.
        
        For health queries, provide:
        - General health guidance and education
        - Environmental health connections (air quality, water safety, etc.)
        - Preventive care suggestions
        - When to seek medical attention
        
        IMPORTANT: 
        - Always recommend consulting healthcare professionals for medical concerns
        - Provide educational information only, not medical diagnosis
        - Be empathetic and supportive
        - Focus on environmental health connections where relevant
        """
    else:
        system_prompt = """You are an environmental expert chatbot. 
        Answer questions about environmental conservation, climate change, 
        sustainability, and ecological issues. Provide accurate, helpful information 
        to promote environmental awareness and connect environmental health to human wellbeing."""
    
    try:
        # Call the model
        response = call_text_model(
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            system_prompt=system_prompt,
            user_prompt=input_text
        )
        
        # Add clinic suggestions for human health queries
        clinic_suggestions = ""
        clinic_data = []
        
        if health_type == "human" and user_city:
            clinic_data = find_nearby_clinics(user_city)
            if clinic_data:
                clinic_suggestions = f"\n\n🏥 **Healthcare Facilities near {user_city}:**\n\n"
                for clinic in clinic_data[:3]:  # Show top 3
                    clinic_suggestions += f"**{clinic['name']}**\n"
                    clinic_suggestions += f"📍 {clinic['address']}\n"
                    clinic_suggestions += f"📞 {clinic.get('phone', 'Contact local directory')}\n"
                    if clinic.get('rating') != 'N/A':
                        clinic_suggestions += f"⭐ Rating: {clinic['rating']}/5\n"
                    clinic_suggestions += "---\n"
                
                clinic_suggestions += "\n*Please consult with healthcare professionals for proper medical advice.*"
        
        elif health_type == "human" and not user_city:
            clinic_suggestions = "\n\n🏥 **Need medical assistance?** Please specify your city, and I can suggest nearby healthcare facilities."
        
        full_response = response + clinic_suggestions
        
        return {
            "response": full_response,
            "clinic_data": clinic_data,
            "metadata": {
                "agent_used": "eco_chatbot_agent",
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "health_type": health_type,
                "clinic_suggestions_provided": bool(clinic_suggestions),
                "success": True
            }
        }
    
    except Exception as e:
        return {
            "response": f"I apologize, but I encountered an error: {str(e)}",
            "metadata": {
                "agent_used": "eco_chatbot_agent",
                "success": False,
                "error": str(e)
            }
        }