from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class GlobalState(TypedDict, total=False):
    query: str
    route: Literal["research", "websearch", "qa", "summarize", "planning"]
    messages: Annotated[list[BaseMessage], add_messages]
    final_answer: str
