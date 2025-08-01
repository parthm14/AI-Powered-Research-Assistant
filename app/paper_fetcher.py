import feedparser
import aiohttp
import asyncio
from urllib.parse import quote
from typing import List
from app.schema import ResearchPaper
from app.utils import deduplicate_papers


async def fetch_arxiv(query: str, max_results: int = 10) -> List[ResearchPaper]:
    encoded_query = quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    feed = feedparser.parse(url)

    papers = []
    for entry in feed.entries:
        papers.append(
            ResearchPaper(
                title=entry.title,
                authors=", ".join(author.name for author in entry.authors),
                summary=entry.summary,
                url=entry.link,
                source="arXiv"
            )
        )
    return papers


async def fetch_semantic_scholar(query: str, max_results: int = 5) -> List[ResearchPaper]:
    base_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote(query)}&limit={max_results}"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, headers=headers) as response:
            data = await response.json()

    papers = []
    for item in data.get("data", []):
        papers.append(
            ResearchPaper(
                title=item.get("title"),
                authors=", ".join(author.get("name", "") for author in item.get("authors", [])),
                summary=item.get("abstract", "Summary not available."),
                url=item.get("url", ""),
                source="Semantic Scholar"
            )
        )
    return papers


async def fetch_core(query: str, max_results: int = 5) -> List[ResearchPaper]:
    # Simulate results as CORE may require an API key
    dummy_papers = [
        ResearchPaper(
            title=f"CORE Paper {i} on {query}",
            authors="Author X, Author Y",
            summary=f"Summary of CORE Paper {i} related to {query}",
            url=f"https://core.ac.uk/paper/{i}",
            source="CORE"
        ) for i in range(1, max_results + 1)
    ]
    await asyncio.sleep(0.1)  # Simulate latency
    return dummy_papers


async def fetch_papers(query: str) -> List[ResearchPaper]:
    tasks = [
        fetch_arxiv(query),
        fetch_semantic_scholar(query),
        fetch_core(query)
    ]
    results = await asyncio.gather(*tasks)

    # Flatten results and deduplicate
    all_papers = [paper for result in results for paper in result]
    unique_papers = deduplicate_papers(all_papers)

    return unique_papers[:10]