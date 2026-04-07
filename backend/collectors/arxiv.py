"""ArXiv API collector for applied AI research papers."""
import asyncio
import json
from datetime import datetime, date
from urllib.parse import quote

import feedparser
import httpx

from backend.collectors.base import BaseCollector, RawResearchItem

ARXIV_API = "http://export.arxiv.org/api/query"

DOMAIN_KEYWORDS = [
    "economics", "operations", "efficiency", "manufacturing", "healthcare",
    "finance", "supply chain", "pricing", "applied", "industry",
    "production", "deployment", "optimization", "automation", "logistics",
    "resource allocation", "scheduling", "cost", "productivity", "retail",
    "energy", "transportation",
]

CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML"]


class ArxivCollector(BaseCollector):
    name = "arxiv"
    schedule_interval_hours = 6

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []
        # Build queries combining categories with domain keywords
        cat_query = " OR ".join(f"cat:{c}" for c in CATEGORIES)
        keyword_query = " OR ".join(f"abs:{kw}" for kw in DOMAIN_KEYWORDS[:10])
        query = f"({cat_query}) AND ({keyword_query})"

        async with httpx.AsyncClient(timeout=30.0) as client:
            for start in range(0, 200, 100):  # Fetch up to 200 papers
                params = {
                    "search_query": query,
                    "start": start,
                    "max_results": 100,
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
                    if not arxiv_id:
                        continue

                    # Extract authors and affiliations
                    authors = []
                    company_name = None
                    for author in entry.get("authors", []):
                        name = author.get("name", "")
                        if name:
                            authors.append(name)
                        # Check for affiliation
                        affiliation = None
                        if hasattr(author, "arxiv_affiliation"):
                            affiliation = author.get("arxiv_affiliation", "")
                        for tag in entry.get("tags", []):
                            pass  # affiliations are sparse in arXiv

                    # Parse date
                    published = None
                    if entry.get("published"):
                        try:
                            published = datetime.fromisoformat(
                                entry["published"].replace("Z", "+00:00")
                            ).date()
                        except (ValueError, TypeError):
                            pass

                    # Detect industry/domain from abstract
                    abstract = entry.get("summary", "")
                    industry = self._detect_industry(abstract)
                    domain = self._detect_domain(abstract)

                    # Build links
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
                        company_name=company_name,
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
