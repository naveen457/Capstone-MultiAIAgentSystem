from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper

api_wrapper = ArxivAPIWrapper(
    top_k_results=5,
    ARXIV_MAX_QUERY_LENGTH=300,
    load_max_docs=3,
    load_all_available_meta=False,
    doc_content_chars_max=40000,
)

arxiv_tool = ArxivQueryRun(api_wrapper=api_wrapper)
