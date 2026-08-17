from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.states.research_state import ResearchState
from app.models.llm import model

from app.tools.arxiv import arxiv_tool
from app.tools.web_search import web_search_tool

from app.chains.research_chain import create_research_plan
from langchain_core.messages import SystemMessage

tools = [arxiv_tool, web_search_tool]

model_with_tools = model.bind_tools(tools)

tool_node = ToolNode(tools)


def planner_node(state: ResearchState) -> ResearchState:
    plan = create_research_plan(state["query"])
    return {"plan": plan.search_queries}


def research_node(state: ResearchState):

    messages = [
        SystemMessage(content="""
You are a research agent.

Use the available research tools to investigate
the user's research question.

Prefer arXiv for academic papers.
Use web search only when additional information
is required.
"""),
        {
            "role": "user",
            "content": f"""
Research question:
{state["query"]}

Research plan:
{state.get("plan", [])}
""",
        },
    ]

    response = model_with_tools.invoke(messages)

    return {"messages": [response]}


def analyzer_node(state: ResearchState):

    messages = state.get("messages", [])

    findings = []

    for message in messages:
        if hasattr(message, "content"):
            findings.append(str(message.content))

    return {"findings": findings}


from app.chains.synthesis_chain import synthesize_research


def synthesizer_node(state: ResearchState):

    report = synthesize_research(
        query=state["query"], findings=state.get("findings", [])
    )

    return {"final_answer": report.model_dump_json(indent=2)}


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
