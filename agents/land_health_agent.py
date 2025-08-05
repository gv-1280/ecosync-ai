from typing import Dict
from utils.openrouter import call_openrouter_image_model

def land_health_agent_node(state: Dict) -> Dict:
    image_data = state.get("image")
    prompt = state.get("input", "Analyze the land animal's condition in this image.")

    if not image_data:
        response = "No image provided for land animal analysis."
    else:
        response = call_openrouter_image_model(
            prompt,
            image_data,
            model="moonshotai/kimi-vl-a3b-thinking:free"
        )

    return {"land_output": response}
