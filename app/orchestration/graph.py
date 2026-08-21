from langgraph.graph import StateGraph, START, END
from app.chains.router_chain import route_query
from app.chains.final_response_chain import (
    format_final_response_web_research,
    format_final_response_general,
)
from app.states.global_state import GlobalState
from app.states.research_state import ResearchState
from app.subgraphs.research_subgraph import research_graph
from app.subgraphs.web_search_subgraph import web_search_graph
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


def web_search_entry(state: GlobalState):

    result = web_search_graph.invoke({"query": state["query"], "web_findings": []})

    web_results = "\n".join(f"- {item}" for item in result.get("web_findings", []))

    return {
        "final_answer": format_final_response_web_research(
            query=state["query"],
            web_results=web_results,
        )
    }


def direct_response_entry(state: GlobalState):

    return {
        "final_answer": format_final_response_general(
            query=state["query"],
        )
    }


builder = StateGraph(GlobalState)

builder.add_node("route", route_node)

builder.add_node("research", research_entry)

builder.add_node("web_search", web_search_entry)

builder.add_node("direct_response", direct_response_entry)

builder.add_edge(START, "route")

builder.add_conditional_edges(
    "route",
    lambda state: state["route"],
    {
        "research": "research",
        "websearch": "web_search",
        "qa": "direct_response",
        "summarize": "direct_response",
        "planning": "direct_response",
    },
)

builder.add_edge("research", END)

builder.add_edge("web_search", END)

builder.add_edge("direct_response", END)

graph = builder.compile()
