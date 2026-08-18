from langchain_openai import ChatOpenAI

from app.config.settings import settings


def create_model():
    model = ChatOpenAI(
        model="openrouter/free",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    return model


model = create_model()

# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.config.settings import settings


# def create_model():
#     model = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=settings.GOOGLE_API_KEY,
#         temperature=0,
#     )

#     return model


# model = create_model()

# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from app.config.constants import constants
# from app.config.settings import settings


# def create_model():
#     llm = HuggingFaceEndpoint(
#         repo_id=constants.LLM_MODEL,
#         task="text-generation",
#         huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_KEY,
#     )

#     return ChatHuggingFace(llm=llm)


# model = create_model()
