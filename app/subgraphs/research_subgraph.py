from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from app.states.research_state import ResearchState
from app.models.llm import model

from app.tools.arxiv import arxiv_tool
from app.tools.dates import dates

from app.chains.research_chain import create_research_plan
from app.chains.final_response_chain import format_final_response_web_research
from app.chains.synthesis_chain import synthesize_research

from app.subgraphs.web_search_subgraph import web_search_graph

tools = [
    arxiv_tool,
    dates,
]

# Bind tools to the model
model_with_tools = model.bind_tools(tools)

# LangGraph ToolNode executes the requested tools
tool_node = ToolNode(tools)


def planner_node(state: ResearchState) -> ResearchState:
    """
    Create a research plan from the user's query.
    """

    plan = create_research_plan(state["query"])

    return {"plan": plan.search_queries}


def research_node(state: ResearchState):
    system_message = SystemMessage(content="""
You are a research agent.

Your job is to investigate the user's research question using
the available research tools.

Available tools:

1. arXiv
   - Use this for academic papers, research papers,
     scientific literature, and paper-related questions.

2. dates
   - Use this only when the question requires the
     current date or time.

Rules:

- Prefer arXiv for academic and research questions.
- Use dates only when date/time information is required.
- Do not invent research findings.
- Use tools only when necessary.
- Keep tool usage minimal.
- After obtaining sufficient information, stop using tools
  and provide a concise research response.
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
    """
    Extract research findings from tool results.
    """

    messages = state.get("messages", [])

    paper_findings = []
    web_findings = []

    for message in messages:

        # We are primarily interested in ToolMessage results
        if isinstance(message, ToolMessage):

            content = str(message.content)

            tool_name = str(getattr(message, "name", "")).lower()

            # arXiv results
            if "arxiv" in tool_name or "paper" in tool_name:

                paper_findings.append(content)

            # Date results are not research findings
            elif "date" in tool_name:

                continue

            # Other search-related results
            elif "tavily" in tool_name or "web" in tool_name or "search" in tool_name:

                web_findings.append(content)

    return {
        "paper_findings": paper_findings,
        "web_findings": web_findings,
    }


def needs_web_search(state: ResearchState) -> bool:
    """
    Decide whether the research requires web search.
    """

    query = state["query"].lower()

    paper_findings = state.get("paper_findings", [])

    # No paper findings → use web search
    if not paper_findings:
        return True

    # Queries requiring fresh information
    current_terms = [
        "latest",
        "current",
        "recent",
        "today",
        "news",
        "update",
    ]

    if any(term in query for term in current_terms):
        return True

    # Check whether paper information
    # is substantial enough
    combined_papers = " ".join(paper_findings).strip()

    if len(combined_papers) < 400:
        return True

    return False


def web_search_node(state: ResearchState):
    """
    Run the independent web-search subgraph.
    """

    result = web_search_graph.invoke(
        {
            "query": state["query"],
            "web_findings": [],
        }
    )

    return {"web_findings": result.get("web_findings", [])}


def synthesizer_node(state: ResearchState):
    """
    Combine paper findings and web findings
    into the final answer.
    """

    paper_findings = state.get("paper_findings", [])

    web_findings = state.get("web_findings", [])

    if web_findings:

        web_text = "\n".join(f"- {item}" for item in web_findings)

    else:

        web_text = "No direct web results were returned."

    if not paper_findings:

        return {
            "final_answer": format_final_response_web_research(
                query=state["query"],
                paper_report="",
                web_results=web_text,
            )
        }

    report = synthesize_research(
        query=state["query"],
        findings=paper_findings,
    )

    paper_report_text = (
        f"Summary: {report.summary}\n\n"
        f"Key findings:\n"
        + "\n".join(f"- {item}" for item in report.key_findings)
        + "\n\n"
        f"Comparison: {report.comparison}\n\n"
        f"Limitations:\n"
        + "\n".join(f"- {item}" for item in report.limitations)
        + "\n\n"
        f"Conclusion: {report.conclusion}"
    )

    return {
        "final_answer": format_final_response_web_research(
            query=state["query"],
            paper_report=paper_report_text,
            web_results=web_text,
        )
    }


builder = StateGraph(ResearchState)


builder.add_node(
    "planner",
    planner_node,
)

builder.add_node(
    "research",
    research_node,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_node(
    "analyzer",
    analyzer_node,
)

builder.add_node(
    "web_search",
    web_search_node,
)

builder.add_node(
    "synthesizer",
    synthesizer_node,
)


builder.add_edge(
    START,
    "planner",
)

builder.add_edge(
    "planner",
    "research",
)


builder.add_conditional_edges(
    "research",
    tools_condition,
    {
        "tools": "tools",
        END: "analyzer",
    },
)


builder.add_edge(
    "tools",
    "research",
)

builder.add_conditional_edges(
    "analyzer",
    needs_web_search,
    {
        True: "web_search",
        False: "synthesizer",
    },
)

builder.add_edge(
    "web_search",
    "synthesizer",
)


builder.add_edge(
    "synthesizer",
    END,
)


research_graph = builder.compile()
