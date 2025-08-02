from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.eco_chatbot_agent import eco_chatbot_node
from agents.marine_health_agent import marine_health_node
from agents.land_health_agent import land_health_node
from graph.router import router_node

class EcosyncState(TypedDict):
    input: str
    response: str
    next: str

def run_agent_flow(user_input):
    graph = StateGraph(EcosyncState)

    # Add Nodes
    graph.add_node("Router", router_node)
    graph.add_node("EcoChatbot", eco_chatbot_node)
    graph.add_node("MarineHealth", marine_health_node)
    graph.add_node("LandHealth", land_health_node)

    # Set Entry Point
    graph.set_entry_point("Router")

    # Conditional Routing
    graph.add_conditional_edges(
        "Router",
        lambda state: state["next"],
        {
            "EcoChatbot": "EcoChatbot",
            "MarineHealth": "MarineHealth",
            "LandHealth": "LandHealth"
        }
    )

    # End edges
    graph.add_edge("EcoChatbot", END)
    graph.add_edge("MarineHealth", END)
    graph.add_edge("LandHealth", END)

    app = graph.compile()
    return app.invoke({"input": user_input})
