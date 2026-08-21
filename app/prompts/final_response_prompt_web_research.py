from langchain_core.prompts import PromptTemplate

final_response_prompt_web_research = PromptTemplate(
    template="""You are a helpful assistant.

Write a clear chat-style response for the user.

Rules:
- Do not output JSON.
- Do not show code or internal fields.
- If the input contains a paper report, summarize it in natural language.
- If the input contains direct web results only, present them as concise bullet points.
- Keep the response brief, readable, and user-facing.

User query:
{query}

Paper report:
{paper_report}

Direct web results:
{web_results}
""",
    input_variables=["query", "paper_report", "web_results"],
)
