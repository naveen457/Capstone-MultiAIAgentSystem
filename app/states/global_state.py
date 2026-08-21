from typing import Literal, TypedDict


class GlobalState(TypedDict, total=False):
    query: str
    route: Literal["research", "websearch", "qa", "summarize", "planning"]
    final_answer: str