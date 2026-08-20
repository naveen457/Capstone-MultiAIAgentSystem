from langgraph.graph import StateGraph, START, END
from app.chains.router_chain import route_query
from app.states.global_state import GlobalState
from app.states.research_state import ResearchState
from app.subgraphs.research_subgraph import research_graph
from langsmith import traceable


@traceable(name="route_node")
def route_node(state: GlobalState) -> GlobalState:

    return {"route": route_query(state["query"])}


def research_entry(state: GlobalState):

    research_state: ResearchState = {
        "query": state["query"],
        "messages": [],
    }

    result = research_graph.invoke(research_state)

    return {"final_answer": result["final_answer"]}


builder = StateGraph(GlobalState)

builder.add_node("route", route_node)

builder.add_node("research", research_entry)

builder.add_edge(START, "route")

builder.add_edge("route", "research")

builder.add_edge("research", END)

graph = builder.compile()
