# app/config.py

import os
# Google Gemini API key 
GOOGLE_API_KEY = "AIzaSyDG_e_CRU7837yiDyEyO4dsLBabHuoMLFo"

# OpenSearch Configuration
OPENSEARCH_URL = "http://localhost:9200"
OPENSEARCH_INDEX = "research-papers"

# Embeddings
EMBEDDING_DIM = 384
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Directory to store downloaded papers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAPER_STORAGE_DIR = os.path.join(BASE_DIR, "downloads")

# Ensure the downloads directory exists
os.makedirs(PAPER_STORAGE_DIR, exist_ok=True)