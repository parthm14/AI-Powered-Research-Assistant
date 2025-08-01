import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import HuggingFaceEmbeddings
from app.config import OPENSEARCH_URL, OPENSEARCH_INDEX


def load_documents_from_directory(directory):
    documents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            continue
        documents.extend(loader.load())
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def index_documents():
    print("Loading and chunking documents...")
    docs = load_documents_from_directory("data")
    chunks = split_documents(docs)

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Indexing documents into OpenSearch...")
    vector_store = OpenSearchVectorSearch(
        index_name=OPENSEARCH_INDEX,
        opensearch_url=OPENSEARCH_URL,
        embedding_function=embeddings,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    vector_store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks into OpenSearch.")


if __name__ == "__main__":
    index_documents()