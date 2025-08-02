def router_node(state):
    user_input = state.get("input", "").lower()
    
    health_keywords = [
        "symptom", "disease", "white spots", "infection", "dead", "injury", 
        "not eating", "floating", "skin problem", "fins", "marine health"
    ]
    
    if any(keyword in user_input for keyword in health_keywords):
        return {"next": "MarineHealth", "input": user_input}
    
    return {"next": "EcoChatbot", "input": user_input}
