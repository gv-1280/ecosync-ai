from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load Mistral model
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct")

eco_llm = pipeline("text-generation", model=model, tokenizer=tokenizer)

def eco_chatbot_node(state):
    question = state.get("input", "").strip()

    prompt = (
        f"<s>[INST] You are an environmental chatbot. Help answer questions about marine life, forests, biodiversity, pollution, and SDG goals in simple language.\n"
        f"User: {question} [/INST]"
    )

    try:
        response = eco_llm(prompt, max_new_tokens=200, do_sample=True)[0]["generated_text"]
        response = response.split("[/INST]")[-1].strip()  # clean extra tokens
    except Exception:
        response = "🌎 Sorry, I couldn't respond right now. Try again soon."

    return {"response": response}
