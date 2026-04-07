"""Semantic Scholar API collector for applied AI research papers."""
import asyncio
import json
from datetime import datetime, date

import httpx

from backend.collectors.base import BaseCollector, RawResearchItem
from backend.collectors.taxonomy import (
    SEMANTIC_SCHOLAR_QUERIES,
    FRONTIER_AREAS,
    compute_relevance_score,
    detect_industry,
    detect_domain,
)
from backend.config import settings

S2_API = "https://api.semanticscholar.org/graph/v1"


class SemanticScholarCollector(BaseCollector):
    name = "semantic_scholar"
    schedule_interval_hours = 6

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []
        seen_ids: set[str] = set()

        headers = {}
        if settings.semantic_scholar_api_key:
            headers["x-api-key"] = settings.semantic_scholar_api_key

        fields = "paperId,title,abstract,authors,venue,year,citationCount,fieldsOfStudy,publicationDate,openAccessPdf,externalIds"

        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            for query, frontier_area in SEMANTIC_SCHOLAR_QUERIES:
                try:
                    resp = await client.get(
                        f"{S2_API}/paper/search",
                        params={
                            "query": query,
                            "fields": fields,
                            "limit": 20,
                            "year": "2023-",
                        },
                    )
                    if resp.status_code == 429:
                        await asyncio.sleep(5)
                        continue
                    resp.raise_for_status()
                    data = resp.json()
                except (httpx.HTTPError, json.JSONDecodeError) as e:
                    print(f"S2 error for '{query}': {e}")
                    await asyncio.sleep(2)
                    continue

                for paper in data.get("data", []):
                    paper_id = paper.get("paperId", "")
                    if not paper_id or paper_id in seen_ids:
                        continue
                    seen_ids.add(paper_id)

                    title = (paper.get("title") or "").strip()
                    abstract = (paper.get("abstract") or "").strip()[:2000]

                    # Compute relevance and skip low-relevance items
                    relevance = compute_relevance_score(title, abstract)
                    if relevance < 0.2:
                        continue

                    authors = [
                        a.get("name", "")
                        for a in paper.get("authors", [])
                        if a.get("name")
                    ]

                    published = None
                    if paper.get("publicationDate"):
                        try:
                            published = date.fromisoformat(paper["publicationDate"])
                        except (ValueError, TypeError):
                            pass
                    elif paper.get("year"):
                        try:
                            published = date(paper["year"], 1, 1)
                        except (ValueError, TypeError):
                            pass

                    # Use taxonomy-aware detection
                    combined = f"{title} {abstract}"
                    industry = detect_industry(combined)
                    domain = detect_domain(combined)
                    area_info = FRONTIER_AREAS.get(frontier_area, {})
                    if not domain and area_info.get("domain"):
                        domain = area_info["domain"]

                    links = []
                    if paper.get("openAccessPdf", {}) and paper["openAccessPdf"].get("url"):
                        links.append({"url": paper["openAccessPdf"]["url"], "type": "paper", "title": "PDF"})

                    arxiv_id = None
                    ext_ids = paper.get("externalIds", {}) or {}
                    if ext_ids.get("ArXiv"):
                        arxiv_id = ext_ids["ArXiv"]
                        links.append({
                            "url": f"https://arxiv.org/abs/{arxiv_id}",
                            "type": "paper",
                            "title": "ArXiv",
                        })

                    source_url = f"https://www.semanticscholar.org/paper/{paper_id}"
                    links.append({"url": source_url, "type": "paper", "title": "Semantic Scholar"})

                    items.append(RawResearchItem(
                        title=title,
                        description=abstract if abstract else None,
                        source_type="semantic_scholar",
                        relevance_score=relevance,
                        source_id=paper_id,
                        source_url=source_url,
                        company_name=None,
                        industry=industry,
                        domain=domain,
                        date_published=published,
                        authors=authors,
                        links=links,
                        raw_metadata=json.dumps({
                            "venue": paper.get("venue", ""),
                            "citation_count": paper.get("citationCount", 0),
                            "fields_of_study": paper.get("fieldsOfStudy", []),
                            "arxiv_id": arxiv_id,
                            "authors": authors,
                            "frontier_area": frontier_area,
                            "relevance_score": relevance,
                        }),
                    ))

                await asyncio.sleep(1.5)

        return items
