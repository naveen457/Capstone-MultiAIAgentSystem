from app.models.llm import model
from app.prompts.final_response_prompt_web_research import (
    final_response_prompt_web_research,
)
from app.prompts.final_response_prompt_general import final_response_prompt_general
from app.parsers.output_parsers import final_response_parser

final_response_chain_web_research = (
    final_response_prompt_web_research | model | final_response_parser
)

final_response_chain_general = (
    final_response_prompt_general | model | final_response_parser
)


def format_final_response_web_research(
    query: str, paper_report: str = "", web_results: str = ""
) -> str:
    """Provide proper final answer based on the information provided.If any fields are empty then provide direct final answer.No need to give unnecessary outputs."""
    response = final_response_chain_web_research.invoke(
        {
            "query": query,
            "paper_report": paper_report,
            "web_results": web_results,
        }
    )

    return response


def format_final_response_general(query: str) -> str:
    """Provide direct answers based on the users question properly"""
    response = final_response_chain_general.invoke({"query": query})
    return response
