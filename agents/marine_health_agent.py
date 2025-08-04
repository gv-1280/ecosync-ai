from transformers import pipeline

marine_llm = pipeline("text2text-generation", model="google/flan-t5-large")

def marine_health_node(state):
    concern = state.get("input", "").strip()

    prompt = (
        "You are a marine biologist. The user describes a sea animal health issue.\n"
        f"Symptom: {concern}\n"
        "What could be the issue, and what is a safe home remedy or next step?"
    )

    try:
        response = marine_llm(prompt, max_length=150, do_sample=True)[0]['generated_text']
    except Exception:
        response = "🐟 Sorry, I couldn’t analyze the marine health issue."

    return {"response": response}
