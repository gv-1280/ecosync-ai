import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def eco_chatbot_node(state):
    user_input = state.get("input", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8501"
,  # Replace with your actual domain or GitHub
        "X-Title": "Ecosync AI Chatbot"
    }

    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": [
            {"role": "user", "content": f"Answer like an eco-friendly chatbot. {user_input}"}
        ],
        "max_tokens": 1000  # ✅ Reduced token usage
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
    else:
        answer = f"⚠️ Error: {response.status_code}\n📦 Response: {response.text}"

    return {"response": answer}
