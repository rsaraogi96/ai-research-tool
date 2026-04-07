"""Semantic Scholar API collector for applied AI research papers."""
import asyncio
import json
from datetime import datetime, date

import httpx

from backend.collectors.base import BaseCollector, RawResearchItem
from backend.config import settings

S2_API = "https://api.semanticscholar.org/graph/v1"

SEARCH_QUERIES = [
    "applied AI economics",
    "machine learning operations efficiency",
    "AI manufacturing optimization",
    "deep learning supply chain",
    "AI healthcare operations",
    "machine learning pricing",
    "AI logistics optimization",
    "applied machine learning finance",
    "AI automation industry",
    "neural network forecasting demand",
    "AI resource allocation",
    "LLM applied industry",
    "AI production system deployment",
    "machine learning retail optimization",
    "AI energy efficiency",
]


class SemanticScholarCollector(BaseCollector):
    name = "semantic_scholar"
    schedule_interval_hours = 6

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []
        seen_ids = set()

        headers = {}
        if settings.semantic_scholar_api_key:
            headers["x-api-key"] = settings.semantic_scholar_api_key

        fields = "paperId,title,abstract,authors,venue,year,citationCount,fieldsOfStudy,publicationDate,openAccessPdf,journal,externalIds"

        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            for query in SEARCH_QUERIES:
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

                    # Parse authors
                    authors = []
                    company_name = None
                    for author in paper.get("authors", []):
                        name = author.get("name", "")
                        if name:
                            authors.append(name)

                    # Parse date
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

                    # Detect industry/domain from abstract
                    abstract = paper.get("abstract") or ""
                    title = paper.get("title") or ""
                    combined = f"{title} {abstract}"

                    industry = self._detect_industry(combined)
                    domain = self._detect_domain(combined)

                    # Build links
                    links = []
                    if paper.get("openAccessPdf", {}) and paper["openAccessPdf"].get("url"):
                        links.append({"url": paper["openAccessPdf"]["url"], "type": "paper", "title": "PDF"})

                    # Check for arXiv ID
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
                        title=title.strip(),
                        description=abstract.strip()[:2000] if abstract else None,
                        source_type="semantic_scholar",
                        source_id=paper_id,
                        source_url=source_url,
                        company_name=company_name,
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
                        }),
                    ))

                # Rate limit
                await asyncio.sleep(1.5)

        return items

    def _detect_industry(self, text: str) -> str | None:
        text_lower = text.lower()
        industry_keywords = {
            "Healthcare": ["healthcare", "medical", "clinical", "hospital", "patient", "diagnosis"],
            "Finance": ["financial", "banking", "trading", "stock", "portfolio", "credit"],
            "Manufacturing": ["manufacturing", "factory", "assembly", "production line"],
            "Retail": ["retail", "e-commerce", "shopping", "consumer"],
            "Energy": ["energy", "power grid", "renewable", "solar", "electricity"],
            "Transportation": ["transportation", "autonomous driving", "vehicle", "traffic"],
            "Agriculture": ["agriculture", "crop", "farming"],
            "Logistics": ["logistics", "warehouse", "delivery", "shipping"],
            "Education": ["education", "student", "tutoring"],
            "Telecommunications": ["telecom", "network traffic", "5g", "wireless"],
        }
        for industry, keywords in industry_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return industry
        return None

    def _detect_domain(self, text: str) -> str | None:
        text_lower = text.lower()
        domain_keywords = {
            "Economics": ["economics", "economic", "market", "equilibrium", "welfare"],
            "Operations Research": ["operations research", "combinatorial", "scheduling"],
            "Efficiency": ["efficiency", "latency", "throughput", "compression", "pruning"],
            "Supply Chain": ["supply chain", "inventory", "procurement"],
            "Pricing": ["pricing", "price", "auction", "revenue"],
            "Automation": ["automation", "automate", "workflow"],
            "Decision Making": ["decision making", "decision support", "policy"],
            "Optimization": ["optimization", "optimize", "resource allocation"],
            "Forecasting": ["forecasting", "prediction", "demand forecasting"],
        }
        for domain, keywords in domain_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return domain
        return None
