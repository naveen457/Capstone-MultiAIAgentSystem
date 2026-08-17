from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.config.constants import constants


def create_model():
    llm = HuggingFaceEndpoint(
        repo_id=constants.LLM_MODEL,
        task="text-generation",
    )

    model = ChatHuggingFace(llm=llm)
    return model


model = create_model()
