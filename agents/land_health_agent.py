from transformers import pipeline

land_llm = pipeline("text2text-generation", model="google/flan-t5-large")

def land_health_node(state):
    concern = state.get("input", "").strip()

    prompt = (
        "You are a wildlife vet. The user reports a health concern in a land animal.\n"
        f"Concern: {concern}\n"
        "Give the likely diagnosis and a basic remedy or recommendation."
    )

    try:
        response = land_llm(prompt, max_length=150, do_sample=True)[0]['generated_text']
    except Exception:
        response = "🦌 Sorry, I couldn’t process the land animal issue."

    return {"response": response}
