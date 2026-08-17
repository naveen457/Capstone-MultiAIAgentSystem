from typing import TypedDict
from langchain_core.documents import Document


class ResearchState(TypedDict):
    query: str
    plan: list[str]
    papers: list[Document]
    findings: list[str]
    analysis: str
    final_answer: str
    messages: list
