"""ArXiv API collector for applied AI research papers."""
import asyncio
import json
from datetime import datetime, date

import feedparser
import httpx

from backend.collectors.base import BaseCollector, RawResearchItem

ARXIV_API = "https://export.arxiv.org/api/query"


class ArxivCollector(BaseCollector):
    name = "arxiv"
    schedule_interval_hours = 6

    QUERIES = [
        "cat:cs.AI AND abs:economics",
        "cat:cs.AI AND abs:operations",
        "cat:cs.AI AND abs:efficiency",
        "cat:cs.LG AND abs:manufacturing",
        "cat:cs.LG AND abs:healthcare",
        "cat:cs.LG AND abs:finance",
        "cat:cs.AI AND abs:optimization AND abs:applied",
        "cat:cs.LG AND abs:supply AND abs:chain",
        "cat:cs.CL AND abs:applied AND abs:industry",
        "cat:cs.AI AND abs:logistics",
        "cat:cs.LG AND abs:pricing",
        "cat:cs.AI AND abs:automation AND abs:industry",
    ]

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            for query in self.QUERIES:
                for start in range(0, 100, 50):
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
                        print(f"ArXiv API error: {e}")
                        break

                    feed = feedparser.parse(resp.text)
                    if not feed.entries:
                        break

                    for entry in feed.entries:
                        arxiv_id = entry.get("id", "").split("/abs/")[-1].split("v")[0]
                        if not arxiv_id or arxiv_id in seen_ids:
                            continue
                        seen_ids.add(arxiv_id)

                        authors = []
                        for author in entry.get("authors", []):
                            name = author.get("name", "")
                            if name:
                                authors.append(name)

                        published = None
                        if entry.get("published"):
                            try:
                                published = datetime.fromisoformat(
                                    entry["published"].replace("Z", "+00:00")
                                ).date()
                            except (ValueError, TypeError):
                                pass

                        abstract = entry.get("summary", "")
                        industry = self._detect_industry(abstract)
                        domain = self._detect_domain(abstract)

                        links = [{"url": entry.get("id", ""), "type": "paper", "title": "ArXiv Page"}]
                        for link in entry.get("links", []):
                            if link.get("type") == "application/pdf":
                                links.append({"url": link["href"], "type": "paper", "title": "PDF"})

                        items.append(RawResearchItem(
                            title=entry.get("title", "").replace("\n", " ").strip(),
                            description=abstract.replace("\n", " ").strip()[:2000],
                            source_type="arxiv",
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
                            }),
                        ))

                    # Rate limit: 3 seconds between requests per arXiv policy
                    await asyncio.sleep(3)

        return items

    def _detect_industry(self, text: str) -> str | None:
        text_lower = text.lower()
        industry_keywords = {
            "Healthcare": ["healthcare", "medical", "clinical", "hospital", "patient", "diagnosis", "drug"],
            "Finance": ["financial", "banking", "trading", "stock", "portfolio", "credit", "fraud"],
            "Manufacturing": ["manufacturing", "factory", "assembly", "production line", "industrial"],
            "Retail": ["retail", "e-commerce", "shopping", "consumer", "merchandise"],
            "Energy": ["energy", "power grid", "renewable", "solar", "wind", "electricity"],
            "Transportation": ["transportation", "autonomous driving", "vehicle", "traffic", "routing"],
            "Agriculture": ["agriculture", "crop", "farming", "soil", "harvest"],
            "Logistics": ["logistics", "warehouse", "delivery", "shipping", "fleet"],
            "Education": ["education", "student", "learning outcome", "tutoring", "curriculum"],
            "Telecommunications": ["telecom", "network traffic", "5g", "wireless", "cellular"],
        }
        for industry, keywords in industry_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return industry
        return None

    def _detect_domain(self, text: str) -> str | None:
        text_lower = text.lower()
        domain_keywords = {
            "Economics": ["economics", "economic", "market", "equilibrium", "welfare", "incentive"],
            "Operations Research": ["operations research", "combinatorial", "scheduling", "assignment", "routing"],
            "Efficiency": ["efficiency", "speed", "latency", "throughput", "compression", "pruning"],
            "Supply Chain": ["supply chain", "inventory", "procurement", "vendor"],
            "Pricing": ["pricing", "price", "auction", "revenue", "cost optimization"],
            "Automation": ["automation", "automate", "workflow", "robotic process"],
            "Decision Making": ["decision making", "decision support", "policy", "planning"],
            "Optimization": ["optimization", "optimize", "resource allocation", "scheduling"],
            "Forecasting": ["forecasting", "prediction", "demand", "time series"],
        }
        for domain, keywords in domain_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return domain
        return None
