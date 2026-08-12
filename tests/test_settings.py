# command to run these test file
# pytest tests/test_settings.py

import pytest

from app.config.settings import Settings


def test_settings_loads_configuration():
    settings = Settings()

    assert settings.APP_ENV is not None
    assert settings.LLM_PROVIDER is not None
    assert settings.LLM_MODEL is not None
    assert settings.LANGCHAIN_PROJECT is not None
    assert settings.HUGGINGFACEHUB_API_KEY is not None


def test_settings_types():
    settings = Settings()

    assert isinstance(settings.APP_ENV, str)
    assert isinstance(settings.DEBUG, bool)
    assert isinstance(settings.LLM_PROVIDER, str)
    assert isinstance(settings.LLM_MODEL, str)
    assert isinstance(settings.LANGCHAIN_TRACING_V2, bool)


def test_settings_values():
    settings = Settings()

    assert settings.APP_ENV == "development"
    assert settings.LLM_PROVIDER == "huggingface"
    assert settings.LLM_MODEL == "meta-llama/Llama-3.1-405B-Instruct"
    assert settings.LANGCHAIN_PROJECT == "agentic-ai-Capstone"
