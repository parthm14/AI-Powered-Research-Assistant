# app/schema.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class ResearchPaper:
    title: Optional[str]
    authors: Optional[str]
    summary: Optional[str]
    url: Optional[str]
    source: Optional[str]

    def to_bibtex(self, index: int) -> str:
        """Returns a BibTeX entry for the paper."""
        safe_title = self.title.replace("{", "").replace("}", "") if self.title else "untitled"
        safe_authors = self.authors.replace("{", "").replace("}", "") if self.authors else "unknown"
        return (
            f"@article{{paper{index},\n"
            f"  title={{\"{safe_title}\"}},\n"
            f"  author={{\"{safe_authors}\"}},\n"
            f"  url={{\"{self.url or 'N/A'}\"}},\n"
            f"  journal={{\"{self.source or 'Unknown'}\"}},\n"
            f"}}\n"
        )

    def to_plaintext_citation(self) -> str:
        """Returns a simple plain-text citation."""
        return f"{self.authors or 'Unknown'}: \"{self.title or 'Untitled'}\". Source: {self.source or 'Unknown'}. URL: {self.url or 'N/A'}"