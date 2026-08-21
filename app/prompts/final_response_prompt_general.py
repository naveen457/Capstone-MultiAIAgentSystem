from langchain_core.prompts import PromptTemplate

final_response_prompt_general = PromptTemplate(
    template="""You are a helpful assistant.

Use the previous conversation when it is relevant to the user's current question.

Previous conversation:
{messages}

Current user query:
{query}

Write a clear, natural chat-style response.
""",
    input_variables=["messages", "query"],
)
