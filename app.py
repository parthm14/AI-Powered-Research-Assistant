# app.py

import streamlit as st
import asyncio
from app.schema import ResearchPaper
from app.paper_fetcher import fetch_papers
from app.summarizer import summarize_text
from app.paper_downloader import download_pdf
from app.utils import generate_citation, display_pdf_text

st.set_page_config(page_title="ResearchBot", layout="wide")

# Session state
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "query" not in st.session_state:
    st.session_state.query = ""

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Search Papers",
    "Papers List",
    "Citations & Bibliography",
    "Upload PDF"
])

# -------------------- 🔍 Search Papers Tab --------------------
with tab1:
    st.title("Search Research Papers")
    st.markdown("Search and summarize research papers from ArXiv, Semantic Scholar, and CORE.")

    query = st.text_input(
        "Enter your research topic:",
        value=st.session_state.query,
        placeholder="e.g. Applications of AI in finance and banking"
    )

    async def summarize_all(papers: list[ResearchPaper]) -> list[str]:
        tasks = [summarize_text(paper.summary or paper.title or "No content") for paper in papers]
        return await asyncio.gather(*tasks)

    if st.button("Fetch & Summarize"):
        st.session_state.query = query
        with st.spinner("Fetching research papers..."):
            papers = asyncio.run(fetch_papers(query))

        if not papers:
            st.warning("No papers found. Try a different topic.")
        else:
            with st.spinner("Summarizing papers..."):
                summaries = asyncio.run(summarize_all(papers))

            st.session_state.papers = papers
            st.session_state.summaries = summaries
            st.success("Papers and summaries updated.")

# -------------------- 📄 Papers List Tab --------------------
with tab2:
    st.title("Retrieved Papers")

    if not st.session_state.papers:
        st.info("No papers to display yet. Please run a search in the first tab.")
    else:
        for paper, summary in zip(st.session_state.papers, st.session_state.summaries):
            with st.expander(paper.title or "Untitled"):
                st.markdown(f"**Authors:** {paper.authors or 'Unknown'}")
                st.markdown(f"**Source:** {paper.source or 'N/A'}")
                st.markdown(f"**Summary:** {summary}")
                if paper.url:
                    st.markdown(f"[Read full paper]({paper.url})", unsafe_allow_html=True)
                    if st.button(f"📥 Download PDF for: {paper.title}", key=paper.title):
                        file_path = download_pdf(paper.url)
                        if file_path:
                            st.success(f"Downloaded to {file_path}")
                        else:
                            st.error("Download failed.")

# -------------------- 📚 Citations & Bibliography Tab --------------------
with tab3:
    st.title("Citations")

    if not st.session_state.papers:
        st.info("No papers available for citation.")
    else:
        citations = [generate_citation(paper) for paper in st.session_state.papers]
        for i, citation in enumerate(citations, 1):
            st.markdown(f"{i}. {citation}")

# -------------------- ⬆️ Upload PDF Tab --------------------
with tab4:
    st.title("Upload Your Own PDF")
    uploaded_file = st.file_uploader("Upload a research paper PDF", type=["pdf"])
    if uploaded_file:
        from app.utils import load_pdf_text
        text = load_pdf_text(uploaded_file)
        st.success(f"Uploaded: {uploaded_file.name}")
        st.subheader("Extracted Text:")
        st.markdown(display_pdf_text(text))