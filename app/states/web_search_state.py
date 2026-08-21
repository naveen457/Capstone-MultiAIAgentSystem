from typing import TypedDict


class WebSearchState(TypedDict):
    query: str
    web_findings: list[str]