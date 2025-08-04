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

# Session state for persistence
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "query" not in st.session_state:
    st.session_state.query = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Search Papers", "Papers List", "Bibliography", "Upload PDF", "Chat with AI"])

# ---- TAB 1: Search Papers ----
with tab1:
    st.header("Search Research Papers")
    query = st.text_input("Enter your research topic:", value=st.session_state.query, placeholder="e.g. Applications of AI in finance and banking")

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

# ---- TAB 2: Papers List ----
with tab2:
    st.header("Retrieved Papers")
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
                    if st.button(f"Download PDF: {paper.title}", key=paper.title):
                        file_path = download_pdf(paper.url)
                        st.success(f"Downloaded to {file_path}") if file_path else st.error("Download failed.")

# ---- TAB 3: Bibliography ----
with tab3:
    st.header("Citations & Bibliography")
    if not st.session_state.papers:
        st.info("No papers found. Run a search first.")
    else:
        citations = [generate_citation(p) for p in st.session_state.papers]
        for cite in citations:
            st.markdown(cite)
        st.download_button("Download Citations", "\n".join(citations), file_name="citations.txt")

# ---- TAB 4: Upload PDF ----
with tab4:
    st.header("Upload Your Own PDF")
    uploaded_file = st.file_uploader("Upload a research paper PDF", type=["pdf"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        # TODO: Implement PDF indexing if required

# ---- TAB 5: Chat with AI ----
with tab5:
    st.header("Chat with AI about Retrieved Papers")

    # Scrollable chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"<div style='background-color:#d4f4dd;color:#000;padding:8px;border-radius:8px;margin-bottom:5px'><b>You:</b> {msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color:#f0f0f0;color:#000;padding:8px;border-radius:8px;margin-bottom:5px'><b>AI:</b> {msg['content']}</div>",
                    unsafe_allow_html=True
                )

    # Chat input fixed at bottom
    st.markdown("---")
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("Type your message", key="chat_input", label_visibility="collapsed")
    with col2:
        send_pressed = st.button("Send")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if send_pressed and user_input.strip():
        context_text = "\n\n".join([f"{p.title}: {p.summary}" for p in st.session_state.papers])
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate AI response
        ai_reply = generate_response(user_input, context_text)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

        st.rerun()