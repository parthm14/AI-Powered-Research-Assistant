# AI-Powered-Research-Assistant

A powerful, interactive Streamlit web app that helps researchers, students, and professionals find and summarize academic papers on any topic. Built using Retrieval-Augmented Generation (RAG), this app fetches papers from ArXiv, Semantic Scholar, and CORE, generates concise summaries using LLMs, and allows PDF uploads and downloads.


## Features

- **Search Academic Papers**  
  Retrieve papers from multiple sources (ArXiv, Semantic Scholar, CORE) based on any research topic.

- **LLM Summarization**  
  Auto-generates concise summaries using Gemini Pro or any preferred local LLM.

- **Download Full PDFs**  
  Download and store full papers from public sources.

- **Upload Your Own PDFs**  
  Upload custom research papers for future indexing and summarization.

- **Multi-tab Interface**  
  Includes Search, Paper List, Bibliography (coming soon), and PDF Upload tabs.

- **Async Paper Fetching**  
  Speeds up performance using `asyncio` for parallel paper retrieval and summarization.

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-Research-Assistant.git
cd AI-Powered-Research-Assistant
```
**2. Create and activate a virtual environment**
```
python3 -m venv .venv
source .venv/bin/activate
On Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Run the app**
```
streamlit run app.py
```
---

## Project Structure

```text
AI-Powered-Research-Assistant/
├── app.py                   # Main Streamlit interface
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
│
├── app/
│   ├── config.py            # Configurations (API keys, paths)
│   ├── schema.py            # ResearchPaper model
│   ├── paper_fetcher.py     # Multi-source async fetcher
│   ├── summarizer.py        # LLM summarizer logic
│   ├── paper_downloader.py  # Download PDFs
│   └── utils.py             # Utility functions
```
---

**Example Use Case**
- Go to the Search Papers tab.
- Enter a query like Applications of AI in finance.
- Click Fetch & Summarize.
- Browse papers in the Papers List tab.
- Download PDFs or upload your own.

---

**Contributing**

Contributions are welcome! Feel free to:
	•	Open issues for bugs or feature requests
	•	Submit pull requests with improvements

---

 **Acknowledgements**
      	•	ArXiv API
	•	Semantic Scholar API
	•	CORE API
	•	Google Generative AI (Gemini)
	•	Streamlit

