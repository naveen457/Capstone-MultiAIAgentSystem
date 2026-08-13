from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_core.documents import Document

api_wrapper = ArxivAPIWrapper(
    top_k_results=5,
    ARXIV_MAX_QUERY_LENGTH=300,
    load_max_docs=3,
    load_all_available_meta=False,
    doc_content_chars_max=40000,
)


def ArxivQueryDocs(query: str) -> Document:
    return api_wrapper.get_summaries_as_docs(query)


tool = ArxivQueryRun(api_wrapper=api_wrapper)
