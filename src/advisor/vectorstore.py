"""FAISS vector store management for Canadian accessibility documents."""

from __future__ import annotations

from typing import Iterable, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from advisor.config import (
    MODEL_CONFIG,
    VECTORSTORE_CONFIG,
    docs_dir,
    index_dir,
    index_path,
    project_root,
)

JURISDICTION_MAP = {
    "federal": "federal",
    "ontario": "provincial",
    "wcag": "standards",
    "provinces": "provincial",
}


def _load_documents() -> List:
    documents = []
    root = project_root()

    for subdir in docs_dir().iterdir():
        if not subdir.is_dir():
            continue

        jurisdiction = JURISDICTION_MAP.get(subdir.name, "unknown")

        for doc_file in subdir.glob("*.txt"):
            loader = TextLoader(str(doc_file))
            docs = loader.load()

            for doc in docs:
                doc.metadata.update(
                    {
                        "source": doc_file.stem,
                        "jurisdiction": jurisdiction,
                        "file_path": str(doc_file.relative_to(root)),
                    }
                )

            documents.extend(docs)

    if not documents:
        raise ValueError(f"No documents found in {docs_dir()}")

    return documents


def _split_documents(documents: Iterable) -> List:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=VECTORSTORE_CONFIG.chunk_size,
        chunk_overlap=VECTORSTORE_CONFIG.chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(list(documents))


def _embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=MODEL_CONFIG.embedding_model)


def build_accessibility_vectorstore() -> FAISS:
    """Load documents from docs/ and build or load the FAISS index."""

    if index_path().exists():
        return FAISS.load_local(
            str(index_path()),
            _embeddings(),
            allow_dangerous_deserialization=True,
        )

    documents = _load_documents()
    splits = _split_documents(documents)

    vectorstore = FAISS.from_documents(splits, _embeddings())

    index_dir().mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_path()))

    return vectorstore
