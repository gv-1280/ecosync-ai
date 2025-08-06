from langgraph.graph import StateGraph, END
from graph.schema import EcosyncState
from graph.router import enhanced_router_node
from agents.eco_chatbot_agent import enhanced_eco_chatbot_agent
from agents.marine_health_agent import enhanced_marine_health_agent
from agents.land_health_agent import enhanced_land_health_agent

def create_enhanced_ecosync_flow():
    """Create and configure the enhanced Ecosync AI multi-agent flow with health integration"""
    
    # Create the state graph
    workflow = StateGraph(EcosyncState)
    
    # Add nodes
    workflow.add_node("enhanced_router", enhanced_router_node)
    workflow.add_node("eco_chatbot_agent", enhanced_eco_chatbot_agent)
    workflow.add_node("marine_health_agent", enhanced_marine_health_agent)
    workflow.add_node("land_health_agent", enhanced_land_health_agent)
    
    # Set entry point
    workflow.set_entry_point("enhanced_router")
    
    # Add conditional routing from router to agents
    def route_to_agent(state: EcosyncState) -> str:
        """Route to the appropriate agent based on enhanced router decision"""
        agent_decision = state.get("agent_decision")
        if agent_decision in ["eco_chatbot_agent", "marine_health_agent", "land_health_agent"]:
            return agent_decision
        else:
            # Fallback to eco chatbot
            return "eco_chatbot_agent"
    
    workflow.add_conditional_edges(
        "enhanced_router",
        route_to_agent,
        {
            "eco_chatbot_agent": "eco_chatbot_agent",
            "marine_health_agent": "marine_health_agent", 
            "land_health_agent": "land_health_agent"
        }
    )
    
    # All agents end the flow
    workflow.add_edge("eco_chatbot_agent", END)
    workflow.add_edge("marine_health_agent", END)
    workflow.add_edge("land_health_agent", END)
    
    # Compile the graph
    app = workflow.compile()
    return app

# Create the enhanced app instance
enhanced_app_flow = create_enhanced_ecosync_flow()

# For backward compatibility
app_flow = enhanced_app_flow