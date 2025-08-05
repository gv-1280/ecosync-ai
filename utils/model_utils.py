from utils.openrouter import OpenRouterClient

client = OpenRouterClient(api_key="your-api-key")

def query_openrouter(prompt: str) -> str:
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def classify_image_clip(image_bytes: bytes, domain="marine") -> str:
    # Replace with real CLIP or ResNet call later
    if b"coral" in image_bytes[:100]:
        return "Detected Coral Bleaching - Marine Health Issue"
    elif domain == "land":
        return "Detected Land Animal Health Issue"
    else:
        return "Unknown issue"
