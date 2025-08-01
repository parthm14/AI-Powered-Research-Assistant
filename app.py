import streamlit as st
import asyncio
from app.schema import ResearchPaper
from app.paper_fetcher import fetch_papers
from app.summarizer import summarize_text
from app.paper_downloader import download_pdf
from app.utils import generate_citation  

st.set_page_config(page_title="ResearchBot", layout="wide")

# Global memory (session state)
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "query" not in st.session_state:
    st.session_state.query = ""
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "notes" not in st.session_state:
    st.session_state.notes = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Search Papers",
    "Papers List",
    "Bibliography",
    "Upload PDF",
    "Favorites & Notes"
])

with tab1:
    st.title("Search Research Papers")
    st.markdown("Search and summarize research papers from ArXiv, Semantic Scholar, and CORE.")

    query = st.text_input("Enter your research topic:", value=st.session_state.query,
                          placeholder="e.g. Applications of AI in finance and banking")

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
                # Favorite toggle
                if paper in st.session_state.favorites:
                    if st.button("❌ Remove from Favorites", key=f"remove_{paper.title}"):
                        index = st.session_state.favorites.index(paper)
                        st.session_state.favorites.pop(index)
                        st.session_state.notes.pop(index)
                        st.success("Removed from favorites")
                else:
                    if st.button("Add to Favorites", key=f"fav_{paper.title}"):
                        st.session_state.favorites.append(paper)
                        st.session_state.notes.append("")
                        st.success("Added to favorites")

with tab3:
    st.title("Citations & Bibliography")

    if not st.session_state.papers:
        st.info("No papers to cite yet. Please run a search first.")
    else:
        st.markdown("### Formatted Citations (APA Style)")
        for paper in st.session_state.papers:
            st.markdown(generate_citation(paper))

with tab4:
    st.title("Upload Your Own PDF")
    uploaded_file = st.file_uploader("Upload a research paper PDF", type=["pdf"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        # Future: display PDF text using `load_pdf_text(uploaded_file)`

with tab5:
    st.title("Favorites & Notes")

    if not st.session_state.favorites:
        st.info("No favorite papers added yet.")
    else:
        for i, paper in enumerate(st.session_state.favorites):
            with st.expander(paper.title or f"Paper {i+1}"):
                st.markdown(f"**Authors:** {paper.authors}")
                st.markdown(f"**Source:** {paper.source}")
                st.markdown(f"**Link:** [View Paper]({paper.url})")
                note = st.text_area("Your Note:", value=st.session_state.notes[i], key=f"note_{i}")
                st.session_state.notes[i] = note

        # Download button for all notes + favorites
        export_content = ""
        for paper, note in zip(st.session_state.favorites, st.session_state.notes):
            export_content += f"Title: {paper.title}\n"
            export_content += f"Authors: {paper.authors}\n"
            export_content += f"Source: {paper.source}\n"
            export_content += f"URL: {paper.url}\n"
            export_content += f"Note: {note or 'No note added.'}\n"
            export_content += "-" * 50 + "\n\n"

        st.download_button(
            label="Download All Favorites & Notes",
            data=export_content,
            file_name="favorites_notes.txt",
            mime="text/plain"
        )