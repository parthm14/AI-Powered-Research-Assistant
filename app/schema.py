# app/schema.py

from dataclasses import dataclass

@dataclass
class ResearchPaper:
    title: str
    authors: str
    summary: str
    source: str
    url: str