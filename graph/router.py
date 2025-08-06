import base64
from typing import Dict, Any
from graph.schema import EcosyncState

def enhanced_router_node(state: EcosyncState) -> Dict[str, Any]:
    """
    Enhanced router that detects human health queries and routes appropriately
    """
    input_text = state.get("input", "").lower()
    image = state.get("image")
    
    # Human health keywords
    human_health_keywords = [
        # Physical symptoms
        "fever", "pain", "headache", "cough", "cold", "flu", "sick", "illness", "injury",
        "rash", "skin condition", "cut", "wound", "bleeding", "swelling", "infection",
        "chest pain", "breathing", "asthma", "allergy", "nausea", "vomiting", "diarrhea",
        
        # Medical terms
        "doctor", "clinic", "hospital", "medical", "treatment", "prescription", "medicine",
        "diagnosis", "symptoms", "health checkup", "vaccination", "emergency",
        
        # Mental health
        "stress", "anxiety", "depression", "mental health", "therapy", "counseling",
        
        # Body parts (when mentioned with health context)
        "stomach ache", "back pain", "joint pain", "muscle pain", "sore throat"
    ]
    
    # Marine health keywords
    marine_keywords = [
        "ocean", "sea", "marine", "fish", "coral", "whale", "dolphin", "shark", 
        "reef", "algae", "seaweed", "jellyfish", "turtle", "seal", "water pollution",
        "oil spill", "marine ecosystem", "aquatic", "underwater", "beach pollution"
    ]
    
    # Land/wildlife health keywords  
    land_keywords = [
        "forest", "land", "animal", "wildlife", "bird", "mammal", "tree", "plant",
        "elephant", "tiger", "lion", "deer", "monkey", "bear", "wolf", "fox",
        "deforestation", "habitat loss", "poaching", "endangered species", "conservation"
    ]
    
    # Determine health type and agent
    is_human_health = any(keyword in input_text for keyword in human_health_keywords)
    is_marine_related = any(keyword in input_text for keyword in marine_keywords)
    is_land_related = any(keyword in input_text for keyword in land_keywords)
    
    # Decision logic
    if is_human_health:
        # Human health query - check if it's environmental health related
        if is_marine_related:
            agent_decision = "marine_health_agent"  # e.g., "water pollution making me sick"
            health_type = "environmental_marine"
        elif is_land_related:
            agent_decision = "land_health_agent"    # e.g., "air pollution from deforestation"
            health_type = "environmental_land"
        else:
            # Pure human health - use eco_chatbot but flag for clinic suggestions
            agent_decision = "eco_chatbot_agent"
            health_type = "human"
    
    elif image:
        # Image analysis - determine marine vs land
        if is_marine_related:
            agent_decision = "marine_health_agent"
            health_type = "marine"
        elif is_land_related:
            agent_decision = "land_health_agent"
            health_type = "land"
        else:
            # Ambiguous image - try to determine from visual cues
            # Default to marine for water-related images, land for others
            agent_decision = "marine_health_agent"  # Can be changed based on image analysis
            health_type = "marine"
    
    else:
        # Text-only environmental query
        if is_marine_related:
            agent_decision = "marine_health_agent"
            health_type = "marine"
        elif is_land_related:
            agent_decision = "land_health_agent"
            health_type = "land"
        else:
            agent_decision = "eco_chatbot_agent"
            health_type = "environmental"
    
    # Determine if we should ask for city (for human health cases)
    needs_city = health_type in ["human", "environmental_marine", "environmental_land"]
    
    return {
        "agent_decision": agent_decision,
        "health_type": health_type,
        "metadata": {
            "routing_reason": f"Selected {agent_decision} for {health_type} health query",
            "has_image": image is not None,
            "needs_clinic_suggestions": needs_city,
            "health_keywords_detected": is_human_health
        }
    }