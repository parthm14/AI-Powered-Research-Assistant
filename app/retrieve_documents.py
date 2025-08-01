# app/retrieve_documents.py

from typing import List
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import HuggingFaceEmbeddings
from app.schema import ResearchPaper
from app.config import OPENSEARCH_URL, OPENSEARCH_INDEX
from sentence_transformers import CrossEncoder


# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load cross-encoder for reranking
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_with_cross_encoder(query: str, documents: List[str], top_k: int = 5) -> List[int]:
    """Returns indices of top_k reranked documents based on cross-encoder scores."""
    pairs = [[query, doc] for doc in documents]
    scores = cross_encoder.predict(pairs)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return ranked_indices


def retrieve_and_rerank(query: str) -> List[ResearchPaper]:
    vector_search = OpenSearchVectorSearch(
        index_name=OPENSEARCH_INDEX,
        embedding_function=embedding_model,
        opensearch_url=OPENSEARCH_URL
    )

    retrieved_docs = vector_search.similarity_search(query, k=15)
    texts = [doc.page_content for doc in retrieved_docs]
    metadatas = [doc.metadata for doc in retrieved_docs]

    top_indices = rerank_with_cross_encoder(query, texts, top_k=5)

    reranked_papers = []
    for idx in top_indices:
        metadata = metadatas[idx]
        reranked_papers.append(
            ResearchPaper(
                title=metadata.get("title", "Untitled"),
                authors=metadata.get("authors", "Unknown"),
                summary=texts[idx],
                url=metadata.get("url", ""),
                source=metadata.get("source", "VectorDB")
            )
        )
    return reranked_papers