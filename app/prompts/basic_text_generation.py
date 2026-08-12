from langchain_core.prompts import PromptTemplate
from app.models.llm import Model


def BasicPromptTemplate():
    prompt = PromptTemplate(
        template="Generate a proper content based on the topic {topic}",
        input_variables=["topic"],
    )
    return prompt
