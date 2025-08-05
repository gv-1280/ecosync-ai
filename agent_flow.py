from langgraph.graph import StateGraph
from graph.schema import AgentState
from agents.eco_chatbot_agent import eco_chatbot_node
from agents.marine_health_agent import marine_health_agent_node
from agents.land_health_agent import land_health_agent_node
from graph.router import router_node

# Initialize the graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("eco", eco_chatbot_node)
builder.add_node("marine", marine_health_agent_node)
builder.add_node("land", land_health_agent_node)
builder.add_node("router", router_node)

# Set entry point
builder.set_entry_point("router")

# Define edges
builder.add_edge("router", "eco")
builder.add_edge("router", "marine")
builder.add_edge("router", "land")

# Set finish conditions
builder.set_finish_point("eco")
builder.set_finish_point("marine")
builder.set_finish_point("land")

# Compile graph
app_flow = builder.compile()
