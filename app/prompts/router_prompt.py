from langchain_core.prompts import PromptTemplate
from app.models.llm import model
from app.parsers.output_parsers import route_decision_parser

router_prompt = PromptTemplate(
    template="""You are the routing agent for a multi-agent assistant. 
Classify the user's request into exactly one route:
- research: Requires external information, papers, web search, current information, evidence, or comparison of sources.
- qa: General question that can be answered from the model's existing knowledge without external research.
- summarize: User wants existing content condensed or summarized.
- planning: User wants a plan, roadmap, strategy, or sequence of actions.

Choose the route that best matches the user's intent.

{formatting_instructions}

User Query: {query}""",
    input_variables=["query"],
    partial_variables={
        "formatting_instructions": route_decision_parser.get_format_instructions()
    },
)
