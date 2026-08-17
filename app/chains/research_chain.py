from app.models.llm import model
from app.prompts.research_prompts import research_planner_prompt
from app.parsers.output_parsers import research_plan_parser

chain = research_planner_prompt | model | research_plan_parser


def create_research_plan(query: str):
    return chain.invoke({"query": query})
