from app.models.llm import model
from app.parsers.output_parsers import research_report_parser
from app.prompts.syntesis_prompts import synthesis_prompt

chain = synthesis_prompt | model | research_report_parser


def synthesize_research(query: str, findings: list[str]):
    return chain.invoke(
        {"query": query, "findings": "\n".join(findings)},
    )
