import os

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # APPLICATION LEVEL
    APP_ENV: str = "development"
    DEBUG: bool = True

    # LLM
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL: str = "meta-llama/Llama-3.1-70B-Instruct:featherless-ai"

    # tavily search
    TAVILY_API_KEY: str | None = None

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str | None = None
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "agentic-ai-Capstone"

    # models api keys
    HUGGINGFACEHUB_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str) and value.lower() == "release":
            return False
        return value

    def configure_langsmith(self):
        langsmith_env = {
            "LANGCHAIN_TRACING_V2": str(self.LANGCHAIN_TRACING_V2).lower(),
            "LANGCHAIN_ENDPOINT": self.LANGCHAIN_ENDPOINT,
            "LANGCHAIN_API_KEY": self.LANGCHAIN_API_KEY,
            "LANGCHAIN_PROJECT": self.LANGCHAIN_PROJECT,
        }

        for key, value in langsmith_env.items():
            if value is not None:
                os.environ.setdefault(key, value)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
settings.configure_langsmith()
