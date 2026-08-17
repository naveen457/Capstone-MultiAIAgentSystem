from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


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


research_plan_parser = PydanticOutputParser(pydantic_object=ResearchPlan)

research_report_parser = PydanticOutputParser(pydantic_object=ResearchReport)
