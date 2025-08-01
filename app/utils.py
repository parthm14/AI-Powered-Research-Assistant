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


def format_authors(authors: str) -> str:
    """
    Cleans and formats the authors string for citation.
    """
    if not authors:
        return "Unknown"
    
    author_list = [a.strip() for a in authors.replace(",", ";").split(";") if a.strip()]
    
    if len(author_list) == 0:
        return "Unknown"
    elif len(author_list) == 1:
        return author_list[0]
    elif len(author_list) == 2:
        return f"{author_list[0]} and {author_list[1]}"
    else:
        return f"{author_list[0]} et al."


def generate_citation(paper: ResearchPaper) -> str:
    """
    Generates a simplified citation string for a research paper.
    """
    author_str = format_authors(paper.authors)
    title = paper.title or "Untitled"
    source = paper.source or "Unknown Source"

    return f'{author_str}. "{title}". {source}.'

def format_authors(authors: str) -> str:
    """
    Formats author string into "Last, First" style and handles multiple authors.
    """
    if not authors:
        return "Unknown"

    # Split authors by comma or 'and' or semicolon
    raw_authors = [a.strip() for a in authors.replace(" and ", ",").split(",")]
    formatted = []

    for author in raw_authors:
        parts = author.split()
        if len(parts) >= 2:
            formatted.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        else:
            formatted.append(author)

    return "; ".join(formatted[:3]) + (" et al." if len(formatted) > 3 else "")


def generate_citation(paper: ResearchPaper) -> str:
    """
    Generates a clean citation for a given research paper.
    """
    authors = format_authors(paper.authors or "")
    title = paper.title.strip('" ').rstrip(".") if paper.title else "Untitled"
    source = paper.source or "Unknown Source"

    return f"{authors}. \"{title}.\" {source}."