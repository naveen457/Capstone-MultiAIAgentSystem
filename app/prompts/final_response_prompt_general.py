from langchain_core.prompts import PromptTemplate

final_response_prompt_general = PromptTemplate(
    template="""You are a helpful assistant.

Write a clear chat-style response for the user.

User query:
{query}
""",
    input_variables=["query"],
)
