from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser


class ResearchPlan(BaseModel):
    objectives: list[str] = Field(description="Reseach Objectives.")

    search_queries: list[str] = Field(description="Queries that should be searched.")

    analysis_tasks: list[str] = Field(
        description="Tasks for the analying the retrieved papers."
    )


class ResearchReport(BaseModel):

    summary: str

    key_findings: list[str]

    comparison: str

    limitations: list[str]

    conclusion: str


class RouteDecision(BaseModel):
    route: Literal["research", "qa", "summarize", "planning"] = Field(
        description="Route the decision to one of these based on the user query."
    )


route_decision_parser = PydanticOutputParser(pydantic_object=RouteDecision)
research_plan_parser = PydanticOutputParser(pydantic_object=ResearchPlan)

research_report_parser = PydanticOutputParser(pydantic_object=ResearchReport)
final_response_parser = StrOutputParser()
