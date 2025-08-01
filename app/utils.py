# app/utils.py

import fitz  # PyMuPDF
from typing import List
from app.schema import ResearchPaper


def load_pdf_text(file_path: str) -> str:
    """
    Extracts and returns text from a given PDF file path.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Failed to load PDF: {e}"


def display_pdf_text(text: str, max_chars=1500) -> str:
    """
    Truncates long PDF text for display.
    """
    return text[:max_chars] + "..." if len(text) > max_chars else text


def deduplicate_papers(papers: List[ResearchPaper]) -> List[ResearchPaper]:
    """
    Deduplicates papers based on title similarity (case-insensitive).
    """
    seen = set()
    unique = []

    for paper in papers:
        key = paper.title.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(paper)

    return unique