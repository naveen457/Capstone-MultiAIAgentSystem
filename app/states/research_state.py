from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
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
    messages: Annotated[list[BaseMessage], add_messages]
