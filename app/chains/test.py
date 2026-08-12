from app.models.llm import model
from app.prompts.basic_text_generation import BasicPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def Chain():

    model

    prompt = BasicPromptTemplate()

    parser = StrOutputParser()

    chain = prompt | model | parser
    return chain


chain = Chain()
