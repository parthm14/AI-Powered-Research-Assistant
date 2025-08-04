# app.py

import streamlit as st
import asyncio
from app.schema import ResearchPaper
from app.paper_fetcher import fetch_papers
from app.summarizer import summarize_text
from app.paper_downloader import download_pdf
from app.utils import generate_citation
from app.generate_answer import generate_response

st.set_page_config(page_title="AI-Powered Research Assistant", layout="wide")

# Initialize session state
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "query" not in st.session_state:
    st.session_state.query = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Search Papers",
    "Papers List",
    "Citations",
    "Upload PDF",
    "Chat with AI"
])

# ---------------- TAB 1: SEARCH PAPERS ----------------
with tab1:
    st.title("Search Research Papers")
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

# ---------------- TAB 2: LIST PAPERS ----------------
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
                    if st.button(f"Download PDF for: {paper.title}", key=paper.title):
                        file_path = download_pdf(paper.url)
                        if file_path:
                            st.success(f"Downloaded to {file_path}")
                        else:
                            st.error("Download failed.")

# ---------------- TAB 3: CITATIONS ----------------
with tab3:
    st.title("Citations & Bibliography")
    if not st.session_state.papers:
        st.info("No citations to display yet. Please run a search first.")
    else:
        for paper in st.session_state.papers:
            citation = generate_citation(paper)
            st.markdown(f"- {citation}")

# ---------------- TAB 4: UPLOAD PDF ----------------
with tab4:
    st.title("Upload Your Own PDF")
    uploaded_file = st.file_uploader("Upload a research paper PDF", type=["pdf"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        # You can later integrate PDF processing here

# ---------------- TAB 5: Chat with AI  ----------------

with tab5:
    st.title("Chat with AI about Retrieved Papers")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask a question about the retrieved papers:", key="chat_input")

    col1, col2 = st.columns([4, 1])  # Send button wider, Clear Chat smaller

    with col1:
        send_clicked = st.button("Send")

    with col2:
        clear_clicked = st.button("Clear Chat")

    if clear_clicked:
        st.session_state.chat_history = []
        st.rerun()

    if send_clicked and user_input.strip():
        # Collect context from summaries
        context_text = "\n".join([
            f"{p.title} - {s}" for p, s in zip(st.session_state.papers, st.session_state.summaries)
        ])
        # Append user message in standardized format
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate AI response
        ai_response = generate_response(user_input, context_text)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        st.rerun()

    # Display chat history safely
    for msg in st.session_state.chat_history:
        role = msg.get("role", "user")  # default to 'user' if missing
        content = msg.get("content", "")
        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**AI:** {content}")