# agents/land_health_agent.py
import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
TEXT_MODEL = "tiiuae/falcon-rw-1b"
IMAGE_MODEL = "openai/clip-vit-base-patch32"

def land_health_node(state):
    if "image" in state:
        image_bytes = state["image"]
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}",
            headers=headers,
            files={"inputs": image_bytes}
        )
        result = response.json()
        output = result[0]["label"] if isinstance(result, list) else "Could not classify image."
        return {"response": f"🖼️ Detected issue: {output}"}
    
    elif "input" in state:
        text = state["input"]
        prompt = f"A user described a land animal with this issue: {text}. Suggest the likely cause and treatment."
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        payload = {"inputs": prompt}
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{TEXT_MODEL}",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
            answer = result[0]["generated_text"]
        else:
            answer = "⚠️ Sorry, I couldn't analyze the issue right now."
        return {"response": answer}
    
    else:
        return {"response": "Please describe the land animal issue or upload an image."}
