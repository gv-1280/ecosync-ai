def marine_health_node(state):
    issue = state.get("input", "")
    return {
        "response": f"🧬 This looks like a marine health issue. We're analyzing: '{issue}'. Please consult a vet or submit more details."
    }
