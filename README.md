Research Assistant (RAG + LLM + Streamlit)

This project is a Research Assistant Web App that allows users to input a research topic, fetch relevant research papers, summarize them, download and index the documents, and interactively ask questions using a Retrieval-Augmented Generation (RAG) pipeline. Built with LangChain, Streamlit, Semantic Scholar API, and OpenSearch, it’s an end-to-end tool for academic research, designed to be fast, intuitive, and memory-aware.

-------------------------------------------------------------------------------------------------------------------------------------

Core Workflow Overview

1. Research Topic Input

Users begin by entering a research query in the text input box on the main interface.
	•	Example: "How are large language models used in government systems?"
	•	The query is saved in the sidebar memory for future access.

2. Paper Retrieval (Semantic Scholar API)

Once a topic is entered, the app:
	•	Fetches top N relevant academic papers via Semantic Scholar.
	•	Stores metadata (title, authors, year, URL).
	•	Displays a clickable list of titles below the input.
	•	Results are stored in st.session_state["papers"].

3. Summarization (Gemini / Gemini Pro Model)

Papers retrieved are passed to a lightweight summarizer using Google’s Gemini LLM:
	•	Only the abstract or summary is used for each paper.
	•	The summary is cleaned and optionally enhanced using keyword extraction (via KeyBERT).
	•	Results are stored in st.session_state["summaries"] and shown under the “Summaries” tab.

4. Paper Download & Indexing

When the user selects papers:
	•	PDFs are downloaded from their URLs.
	•	Files are stored in the data/papers directory.
	•	PDFs are chunked using LangChain’s RecursiveCharacterTextSplitter.
	•	Each chunk is embedded using SentenceTransformers and indexed into OpenSearch using the OpenSearchVectorSearch class.

Indexed documents are now ready for retrieval via vector similarity.

5. Chat With LLM (RAG Pipeline)

Users can ask questions like:
	•	"What are the risks of using LLMs in public policy?"

The pipeline performs:
	1.	Query Embedding
	•	User query is embedded using the same embedding model used for indexing.
	2.	Dense Vector Retrieval
	•	Top k most relevant chunks are fetched from OpenSearch.
	3.	Answer Generation
	•	Context is passed into Gemini via a custom prompt.
	•	Gemini generates a coherent, context-aware answer.
	•	Chat history is updated in session_state["chat_history"].

6. Topic Memory and UI Reset
	•	All research topics are stored in the sidebar with timestamps.
	•	Clicking a saved topic restores all session states (papers, summaries, chat history) for that query.
	•	Enables persistent memory across research sessions.

-------------------------------------------------------------------------------------------------------------------------------------

📁 Directory Structure

research-bot/
│
├── app.py                     # Main Streamlit UI
├── app/
│   ├── paper_fetcher.py       # Semantic Scholar search
│   ├── paper_downloader.py    # PDF downloader
│   ├── summarizer.py          # Gemini-powered summarizer
│   ├── generate_answer.py     # LLM answer generation
│   ├── index_documents.py     # PDF chunking + OpenSearch indexing
│   ├── rag_pipeline.py        # Query -> Retrieval -> Answer
│   ├── utils.py               # Formatting, slugging, etc.
│   └── schema.py              # Paper data model
│
├── data/
│   └── papers/               # Downloaded PDFs
│
└── requirements.txt


⸻

⚙️ Technologies Used

Component: Tool/Library
UI Framework: Streamlit
LLM & RAG: Google Gemini Pro + LangChain
Vector DB: OpenSearch
Paper Search API: Semantic Scholar (official Python SDK)
Summarizer: Gemini + KeyBERT (for keywords)
Embeddings: all-MiniLM-L6-v2 via SentenceTransformers
PDF Parsing: PyMuPDF
State Management: Streamlit st.session_state

-------------------------------------------------------------------------------------------------------------------------------------

Sample Prompts
	•	Topic Input: "Applications of generative AI in healthcare diagnostics"
	•	Questions to Ask in Chat Tab:
	•	“What datasets do most papers use?”
	•	“Are there any known risks associated with these models?”
	•	“Summarize recent advancements in real-time AI diagnostics.”

-------------------------------------------------------------------------------------------------------------------------------------

Suggested Extensions
	•	Add citations tab to export bibliographies.
	•	Enable user PDF uploads alongside Semantic Scholar results.
	•	Add filters for author, year, journal.
	•	Use reranking (CrossEncoder) for more accurate retrieval.
	•	Highlight sources used in final answer (cite as footnotes).
