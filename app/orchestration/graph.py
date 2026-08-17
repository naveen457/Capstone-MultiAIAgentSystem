from langgraph.graph import StateGraph, START, END
from app.states.research_state import ResearchState
from app.subgraphs.research_subgraph import research_graph


def research_entry(state: ResearchState):

    result = research_graph.invoke(state)

    return result


builder = StateGraph(ResearchState)

builder.add_node("research", research_entry)

builder.add_edge(START, "research")

builder.add_edge("research", END)

graph = builder.compile()
