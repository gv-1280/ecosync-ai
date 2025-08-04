def router_node(state):
    user_input = state.get("input", "").lower()

    marine_keywords = [
        "fish", "turtle", "dolphin", "coral", "jellyfish", "sea", "marine", "ocean", 
        "white spots", "infection", "gills", "fin", "aquatic", "aquarium"
    ]

    land_keywords = [
        "dog", "cat", "cow", "deer", "elephant", "leopard", "forest", "zoo",
        "hoof", "fur", "tail", "injury", "limp", "domestic", "wildlife"
    ]

    health_keywords = ["symptom", "disease", "sick", "not moving", "bleeding", "spots", "infection"]

    if any(kw in user_input for kw in health_keywords):
        if any(kw in user_input for kw in marine_keywords):
            return {"next": "MarineHealth", "input": user_input}
        elif any(kw in user_input for kw in land_keywords):
            return {"next": "LandHealth", "input": user_input}

    # Default to EcoChatbot
    return {"next": "EcoChatbot", "input": user_input}
