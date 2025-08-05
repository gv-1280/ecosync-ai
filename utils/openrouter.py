import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_openrouter_text_model(prompt, model="google/gemini-2.5-flash-lite"):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=HEADERS)
    return response.json()["choices"][0]["message"]["content"]

def call_openrouter_image_model(prompt, base64_image, model="moonshotai/kimi-vl-a3b-thinking:free"):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=HEADERS)
    return response.json()["choices"][0]["message"]["content"]
