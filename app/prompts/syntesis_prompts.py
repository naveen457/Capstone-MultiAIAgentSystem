from langchain_core.prompts import PromptTemplate
from app.parsers.output_parsers import research_report_parser

synthesis_prompt = PromptTemplate(
    template="""You are a research synthesis agent.

You will receive research findings extracted from academic papers only.

Your task is to:
1. Identify the main findings.
2. Compare approaches.
3. Identify agreements and disagreements.
4. Identify limitations.
5. Produce a coherent research summary.

Do not invent information that is not present
in the supplied research findings.

Do not include web search results in the paper synthesis.
If web search results are available, they are handled separately as direct results.

Research question:
{query}
Findings:
{findings}

{format_instructions}
""",
    input_variables=["query", "findings"],
    partial_variables={
        "format_instructions": research_report_parser.get_format_instructions()
    },
)
