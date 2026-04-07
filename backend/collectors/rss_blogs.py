"""RSS blog collector for AI company engineering blogs."""
import json
import hashlib
from datetime import datetime, date
from time import mktime

import feedparser
import httpx

from backend.collectors.base import BaseCollector, RawResearchItem
from backend.seed.seed_data import RSS_FEEDS

DOMAIN_KEYWORDS = [
    "ai", "machine learning", "deep learning", "llm", "neural", "model",
    "research", "applied", "economics", "operations", "efficiency",
    "optimization", "automation", "production", "deployment", "inference",
    "fine-tuning", "training", "agents", "rag", "retrieval",
]


class RssBlogCollector(BaseCollector):
    name = "rss"
    schedule_interval_hours = 4

    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        items = []

        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            for feed_config in RSS_FEEDS:
                url = feed_config["url"]
                company = feed_config["company"]

                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    feed = feedparser.parse(resp.text)
                except Exception as e:
                    print(f"RSS error for {company} ({url}): {e}")
                    continue

                for entry in feed.entries[:20]:  # Limit per feed
                    title = entry.get("title", "").strip()
                    if not title:
                        continue

                    # Check relevance
                    combined = f"{title} {entry.get('summary', '')}".lower()
                    if not any(kw in combined for kw in DOMAIN_KEYWORDS):
                        continue

                    # Generate stable source_id
                    entry_id = entry.get("id") or entry.get("link") or title
                    source_id = hashlib.sha256(f"{company}:{entry_id}".encode()).hexdigest()[:16]

                    # Parse date
                    published = None
                    if entry.get("published_parsed"):
                        try:
                            published = date.fromtimestamp(mktime(entry["published_parsed"]))
                        except (ValueError, OverflowError):
                            pass

                    # Get description
                    description = entry.get("summary", "")
                    # Strip HTML tags roughly
                    import re
                    description = re.sub(r"<[^>]+>", "", description)[:2000].strip()

                    link = entry.get("link", "")
                    links = []
                    if link:
                        links.append({"url": link, "type": "blog", "title": f"{company} Blog"})

                    items.append(RawResearchItem(
                        title=title,
                        description=description or None,
                        source_type="rss",
                        source_id=source_id,
                        source_url=link,
                        company_name=company,
                        industry=None,
                        domain=None,
                        date_published=published,
                        authors=[],
                        links=links,
                        raw_metadata=json.dumps({
                            "feed_url": url,
                            "company": company,
                        }),
                    ))

        return items
