import requests

HF_API_TOKEN = "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"  # Replace with actual token
HF_MODEL = "google/flan-t5-base"         # Use public, lightweight model

prompt = "Tell me about the ocean ecosystem."
payload = {"inputs": prompt}
headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print("✅ STATUS:", response.status_code)
    print("📦 RESPONSE:", response.text)

except Exception as e:
    print("❌ ERROR:", e)
