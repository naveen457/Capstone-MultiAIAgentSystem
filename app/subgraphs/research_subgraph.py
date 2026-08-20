from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.states.research_state import ResearchState
from app.models.llm import model

from app.tools.arxiv import arxiv_tool
from app.tools.dates import dates
from app.tools.web_search import web_search_tool

from app.chains.research_chain import create_research_plan
from app.chains.final_response_chain import format_final_response
from langchain_core.messages import HumanMessage, SystemMessage

tools = [arxiv_tool, dates, web_search_tool]

model_with_tools = model.bind_tools(tools)

tool_node = ToolNode(tools)


def planner_node(state: ResearchState) -> ResearchState:
    plan = create_research_plan(state["query"])
    return {"plan": plan.search_queries}


def research_node(state: ResearchState):

    system_message = SystemMessage(content="""
You are a research agent.

Use the available research tools to investigate
the user's research question.

Prefer arXiv for academic papers.
Use web search only when additional information
is required.
""")

    messages = state.get("messages", [])

    if not messages:
        messages = [HumanMessage(content=f"""
Research question:
{state["query"]}

Research plan:
{state.get("plan", [])}
""")]

    response = model_with_tools.invoke([system_message, *messages])

    return {"messages": [response]}


def analyzer_node(state: ResearchState):

    messages = state.get("messages", [])

    paper_findings = []
    web_findings = []

    for message in messages:
        if hasattr(message, "content"):
            content = str(message.content)
            tool_name = str(getattr(message, "name", "")).lower()

            if "arxiv" in tool_name or "paper" in tool_name:
                paper_findings.append(content)
            elif "tavily" in tool_name or "web" in tool_name or "search" in tool_name:
                web_findings.append(content)
            else:
                web_findings.append(content)

    return {"paper_findings": paper_findings, "web_findings": web_findings}


from app.chains.synthesis_chain import synthesize_research


def synthesizer_node(state: ResearchState):
    paper_findings = state.get("paper_findings", [])
    web_findings = state.get("web_findings", [])

    # 1. Format web findings cleanly for both code paths
    if web_findings:
        web_text = "\n".join(f"- {item}" for item in web_findings)
    else:
        web_text = "No direct web results were returned."

    # 2. Check if paper findings are completely empty
    if not paper_findings:
        return {
            "final_answer": format_final_response(
                query=state["query"],
                paper_report="",
                web_results=web_text,
            )
        }

    # 3. Process paper findings if they exist
    report = synthesize_research(query=state["query"], findings=paper_findings)

    paper_report_text = (
        f"Summary: {report.summary}\n"
        f"Key findings:\n"
        + "\n".join(f"- {item}" for item in report.key_findings)
        + "\n"
        f"Comparison: {report.comparison}\n"
        f"Limitations:\n" + "\n".join(f"- {item}" for item in report.limitations) + "\n"
        f"Conclusion: {report.conclusion}"
    )

    return {
        "final_answer": format_final_response(
            query=state["query"],
            paper_report=paper_report_text,
            web_results=web_text,
        )
    }


builder = StateGraph(ResearchState)

builder.add_node("planner", planner_node)

builder.add_node("research", research_node)

builder.add_node("tools", tool_node)

builder.add_node("analyzer", analyzer_node)

builder.add_node("synthesizer", synthesizer_node)


builder.add_edge(START, "planner")

builder.add_edge("planner", "research")

builder.add_conditional_edges(
    "research",
    tools_condition,
    {
        "tools": "tools",
        END: "analyzer",
    },
)

builder.add_edge("tools", "research")

builder.add_edge("analyzer", "synthesizer")

builder.add_edge("synthesizer", END)


research_graph = builder.compile()
