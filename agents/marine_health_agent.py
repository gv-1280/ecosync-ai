# agents/marine_health_agent.py

from typing import Dict
from utils.openrouter import call_openrouter_image_model

def marine_health_agent_node(state: Dict) -> Dict:
    image_data = state.get("image")
    prompt = state.get("input", "Analyze the marine creature's condition in this image.")

    if not image_data:
        response = "No image provided for marine health analysis."
    else:
        response = call_openrouter_image_model(
            prompt,
            image_data,
            model="moonshotai/kimi-vl-a3b-thinking:free"
        )

    return {"marine_output": response}
