from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.documents import Document


class ResearchState(TypedDict):
    query: str
    plan: list[str]
    papers: list[Document]
    paper_findings: list[str]
    web_findings: list[str]
    analysis: str
    final_answer: str
    messages: Annotated[list, add_messages]
