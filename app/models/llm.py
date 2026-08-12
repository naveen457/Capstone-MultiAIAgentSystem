from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.config.settings import Settings

settings = Settings()


def Model():
    llm = HuggingFaceEndpoint(
        repo_id=settings.LLM_MODEL,
        task="text-generation",
    )

    model = ChatHuggingFace(llm=llm)

    return model


model = Model()
