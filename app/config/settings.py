from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # APPLICATION LEVEL
    APP_ENV: str = "development"
    DEBUG: bool = True

    # LLM
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL: str = "meta-llama/Llama-3.1-405B-Instruct"

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str | None = None
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "agentic-ai-Capstone"

    # models api keys
    HUGGINGFACEHUB_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
