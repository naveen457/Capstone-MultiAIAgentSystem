import json

from langgraph.graph import StateGraph, START, END

from app.states.web_search_state import WebSearchState
from app.tools.web_search import web_search_tool


def normalize_web_results(raw_result) -> list[str]:
    if isinstance(raw_result, dict):
        results = []

        answer = raw_result.get("answer")
        if answer:
            results.append(str(answer))

        items = raw_result.get("results", [])
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    title = item.get("title")
                    url = item.get("url")
                    content = item.get("content")
                    parts = [part for part in [title, content, url] if part]
                    if parts:
                        results.append(" | ".join(str(part) for part in parts))
                else:
                    results.append(str(item))

        return results

    if isinstance(raw_result, str):
        try:
            parsed = json.loads(raw_result)
        except json.JSONDecodeError:
            return [line.strip() for line in raw_result.splitlines() if line.strip()]

        return normalize_web_results(parsed)

    if isinstance(raw_result, list):
        return [str(item) for item in raw_result]

    return [str(raw_result)]


def web_search_node(state: WebSearchState) -> WebSearchState:
    raw_result = web_search_tool.invoke(state["query"])

    return {"web_findings": normalize_web_results(raw_result)}


builder = StateGraph(WebSearchState)

builder.add_node("web_search", web_search_node)

builder.add_edge(START, "web_search")
builder.add_edge("web_search", END)

web_search_graph = builder.compile()