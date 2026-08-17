from langchain_tavily import TavilySearch
from app.config.settings import settings

web_search_tool = TavilySearch(
    tavily_api_key=settings.TAVILY_API_KEY, max_results=5, topic="general"
)
