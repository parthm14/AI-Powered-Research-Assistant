# app/models.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import OpenSearchVectorSearch
from app.config import OPENSEARCH_URL, OPENSEARCH_INDEX

def get_embedding_model():
    """
    Loads the HuggingFace embeddings model.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vectorstore(embedding_model):
    """
    Initializes the OpenSearch vector store using the given embedding model.
    """
    return OpenSearchVectorSearch(
        index_name=OPENSEARCH_INDEX,
        embedding_function=embedding_model,
        opensearch_url=OPENSEARCH_URL,
        use_ssl=False,
        verify_certs=False
    )