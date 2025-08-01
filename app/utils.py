# app/utils.py

import fitz  # PyMuPDF
from typing import List
from app.schema import ResearchPaper


def load_pdf_text(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Failed to load PDF: {e}"


def display_pdf_text(text: str, max_chars=1500) -> str:
    return text[:max_chars] + "..." if len(text) > max_chars else text


def deduplicate_papers(papers: List[ResearchPaper]) -> List[ResearchPaper]:
    seen = set()
    unique = []

    for paper in papers:
        key = paper.title.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(paper)

    return unique


def generate_citation(paper: ResearchPaper) -> str:
    """
    Generates a clean citation for a given research paper.
    """
    def format_authors(authors: str) -> str:
        if not authors:
            return "Unknown"
        raw_authors = [a.strip() for a in authors.replace(" and ", ",").split(",")]
        formatted = []
        for author in raw_authors:
            parts = author.split()
            if len(parts) >= 2:
                formatted.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
            else:
                formatted.append(author)
        return "; ".join(formatted[:3]) + (" et al." if len(formatted) > 3 else "")

    authors = format_authors(paper.authors or "")
    title = paper.title.strip('" ').rstrip(".") if paper.title else "Untitled"
    source = paper.source or "Unknown Source"
    return f"{authors}. \"{title}.\" {source}."