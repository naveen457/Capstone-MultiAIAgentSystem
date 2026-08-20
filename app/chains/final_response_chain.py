from app.models.llm import model
from app.prompts.final_response_prompt import final_response_prompt

final_response_chain = final_response_prompt | model


def format_final_response(
    query: str, paper_report: str = "", web_results: str = ""
) -> str:
    response = final_response_chain.invoke(
        {
            "query": query,
            "paper_report": paper_report,
            "web_results": web_results,
        }
    )

    return response.content
