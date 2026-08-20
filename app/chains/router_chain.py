from app.models.llm import model
from app.parsers.output_parsers import route_decision_parser
from app.prompts.router_prompt import router_prompt


router_chain = router_prompt | model | route_decision_parser


def route_query(query: str) -> str:

    decision = router_chain.invoke({"query": query})

    return decision.route