from langgraph.graph import StateGraph, END, START
from state import AgentState
from agents import (
    supervisor_node, 
    billing_node, 
    tech_node, 
    general_node, 
    qa_node
)

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("billing", billing_node)
workflow.add_node("technical", tech_node)
workflow.add_node("general", general_node)
workflow.add_node("qa", qa_node)

# Add edges
workflow.add_edge(START, "supervisor")

# Conditional edge from supervisor
def route_supervisor(state: AgentState):
    return state["next_step"]

workflow.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)

# Edges from agents to QA
workflow.add_edge("billing", "qa")
workflow.add_edge("technical", "qa")
workflow.add_edge("general", "qa")

# Conditional edge from QA
def route_qa(state: AgentState):
    return state["next_step"]

workflow.add_conditional_edges(
    "qa",
    route_qa,
    {
        "END": END,
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)

# Compile
app = workflow.compile()
