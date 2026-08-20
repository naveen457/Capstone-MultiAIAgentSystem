from datetime import datetime

from langchain_core.tools import tool


@tool
def dates() -> str:
    """Return the current local date and time."""

    return datetime.now().astimezone().isoformat()