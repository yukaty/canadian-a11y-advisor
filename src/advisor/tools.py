"""Search tools for Canadian accessibility documents."""

from functools import lru_cache

from langchain.tools import tool

from advisor.config import VECTORSTORE_CONFIG
from advisor.vectorstore import build_accessibility_vectorstore


@lru_cache(maxsize=1)
def get_vectorstore():
    """Lazy load vector store."""
    return build_accessibility_vectorstore()


@tool
def search_accessibility_docs(query: str) -> str:
    """Search Canadian accessibility regulations and standards.

    Args:
        query: Search query about Canadian accessibility laws, regulations, or standards

    Returns:
        Formatted search results with citations
    """
    vectorstore = get_vectorstore()

    # Perform similarity search
    results = vectorstore.similarity_search(query, k=VECTORSTORE_CONFIG.k_results)

    if not results:
        return "No relevant documents found."

    # Format results with citations
    formatted_results = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        jurisdiction = doc.metadata.get("jurisdiction", "unknown")
        content = doc.page_content.strip()

        formatted_results.append(
            f"[Result {i}] Source: {source} (Jurisdiction: {jurisdiction})\n{content}\n"
        )

    return "\n".join(formatted_results)
