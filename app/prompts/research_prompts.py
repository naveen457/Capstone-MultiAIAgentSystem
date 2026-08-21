from langchain_core.prompts import PromptTemplate
from app.parsers.output_parsers import research_plan_parser


research_planner_prompt = PromptTemplate(
    template="""You are a research planning agent.

Your task is to convert the user's research question into a clear research plan.

Before planning, decide the best source order based on the query:
1. Use the dates tool first only if the user asks for the current date or time.
2. Prefer arXiv first for academic or paper-based questions.
3. If arXiv results are not enough, use the dedicated web-search subgraph next.
4. Do not use web search if the question can be answered fully from papers.

Determine:
1. What concepts need to be investigated.
2. What types of papers should be searched.
3. What evidence should be extracted.
4. What comparisons should be made.

Do not perform the research yourself.
Only create the research plan.

Research question:
{query}

{format_instructions}
""",
    input_variables=["query"],
    partial_variables={
        "format_instructions": research_plan_parser.get_format_instructions()
    },
)
