from typing import List
from app.retrieve_documents import retrieve_and_rerank
from app.generate_answer import generate_response
from app.schema import ResearchPaper

# Perform full RAG workflow
def rag_query_answer(query: str) -> str:
    documents: List[ResearchPaper] = retrieve_and_rerank(query, top_k=10)
    context = "\n\n".join([f"{doc.title}\n{doc.summary}" for doc in documents])
    answer = generate_response(query, context)
    return answer