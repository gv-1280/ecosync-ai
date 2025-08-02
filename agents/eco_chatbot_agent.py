def eco_chatbot_node(state):
    user_input = state.get("input", "").lower()
    
    if "ocean" in user_input:
        answer = "🌊 The ocean covers over 70% of the Earth's surface and supports incredible biodiversity."
    elif "forest" in user_input:
        answer = "🌳 Forests are home to over 80% of terrestrial species and play a critical role in climate regulation."
    elif "pollution" in user_input:
        answer = "♻️ Pollution affects marine and land ecosystems alike. Reducing plastic use and promoting clean-up drives are effective actions."
    else:
        answer = "❓ I can help with questions about marine life, forests, biodiversity, or pollution. Try asking something related!"

    return {"response": answer}

if __name__ == "__main__":
    result = eco_chatbot_node({"input": "Tell me about oceans"})
    print(result)
