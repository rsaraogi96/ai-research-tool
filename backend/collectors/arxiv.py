"""ArXiv API collector for applied AI research papers."""
import asyncio
import json
from datetime import datetime, date

import feedparser
import httpx

from backend.collectors.base import BaseCollector, RawResearchItem
from backend.collectors.taxonomy import (
    ARXIV_QUERIES,
    FRONTIER_AREAS,
    compute_relevance_score,
    detect_industry,
    detect_domain,
)

ARXIV_API = "https://export.arxiv.org/api/query"


class ArxivCollector(BaseCollector):
    name = "arxiv"
    schedule_interval_hours = 6

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []
        seen_ids: set[str] = set()

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            for query, frontier_area in ARXIV_QUERIES:
                for start in range(0, 50, 50):  # 50 per query
                    params = {
                        "search_query": query,
                        "start": start,
                        "max_results": 50,
                        "sortBy": "submittedDate",
                        "sortOrder": "descending",
                    }
                    try:
                        resp = await client.get(ARXIV_API, params=params)
                        resp.raise_for_status()
                    except httpx.HTTPError as e:
                        print(f"ArXiv API error for '{query}': {e}")
                        break

                    feed = feedparser.parse(resp.text)
                    if not feed.entries:
                        break

                    for entry in feed.entries:
                        arxiv_id = entry.get("id", "").split("/abs/")[-1].split("v")[0]
                        if not arxiv_id or arxiv_id in seen_ids:
                            continue
                        seen_ids.add(arxiv_id)

                        title = entry.get("title", "").replace("\n", " ").strip()
                        abstract = entry.get("summary", "").replace("\n", " ").strip()[:2000]

                        # Compute relevance and skip low-relevance items
                        relevance = compute_relevance_score(title, abstract)
                        if relevance < 0.2:
                            continue

                        authors = [
                            a.get("name", "")
                            for a in entry.get("authors", [])
                            if a.get("name")
                        ]

                        published = None
                        if entry.get("published"):
                            try:
                                published = datetime.fromisoformat(
                                    entry["published"].replace("Z", "+00:00")
                                ).date()
                            except (ValueError, TypeError):
                                pass

                        # Use taxonomy-aware detection, with frontier area as fallback
                        industry = detect_industry(abstract)
                        domain = detect_domain(abstract)
                        area_info = FRONTIER_AREAS.get(frontier_area, {})
                        if not domain and area_info.get("domain"):
                            domain = area_info["domain"]

                        links = [{"url": entry.get("id", ""), "type": "paper", "title": "ArXiv Page"}]
                        for link in entry.get("links", []):
                            if link.get("type") == "application/pdf":
                                links.append({"url": link["href"], "type": "paper", "title": "PDF"})

                        items.append(RawResearchItem(
                            title=title,
                            description=abstract,
                            source_type="arxiv",
                            relevance_score=relevance,
                            source_id=arxiv_id,
                            source_url=entry.get("id", ""),
                            company_name=None,
                            industry=industry,
                            domain=domain,
                            date_published=published,
                            authors=authors,
                            links=links,
                            raw_metadata=json.dumps({
                                "categories": [t.get("term", "") for t in entry.get("tags", [])],
                                "authors": authors,
                                "frontier_area": frontier_area,
                                "relevance_score": relevance,
                            }),
                        ))

                    # Rate limit: 3 seconds between requests per arXiv policy
                    await asyncio.sleep(3)

        return items
