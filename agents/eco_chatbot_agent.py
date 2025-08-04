import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "google/flan-t5-small"  # or flan-t5-large if you're using that

def eco_chatbot_node(state):
    user_input = state.get("input", "")
    prompt = f"Answer like a helpful SDG chatbot about marine life, forests, biodiversity, and pollution: {user_input}"

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    payload = {
        "inputs": prompt
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("DETAILS:", response.text)

    if response.status_code == 200:
        result = response.json()
        answer = result[0]["generated_text"]
    else:
        answer = "⚠️ Sorry, I couldn't process that right now."

    return {"response": answer}
