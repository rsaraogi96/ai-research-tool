"""RSS blog collector for AI company engineering blogs."""
import re
import json
import hashlib
from datetime import datetime, date
from time import mktime

import feedparser
import httpx

from backend.collectors.base import BaseCollector, RawResearchItem
from backend.collectors.taxonomy import (
    is_relevant_rss,
    compute_relevance_score,
    detect_industry,
    detect_domain,
)
from backend.seed.seed_data import RSS_FEEDS


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

                for entry in feed.entries[:20]:
                    title = entry.get("title", "").strip()
                    if not title:
                        continue

                    # Get description and strip HTML
                    description = entry.get("summary", "")
                    description = re.sub(r"<[^>]+>", "", description)[:2000].strip()

                    # Check relevance using taxonomy
                    if not is_relevant_rss(title, description):
                        continue

                    # Compute relevance score
                    relevance = compute_relevance_score(title, description)

                    # Generate stable source_id
                    entry_id = entry.get("id") or entry.get("link") or title
                    source_id = hashlib.sha256(f"{company}:{entry_id}".encode()).hexdigest()[:16]

                    published = None
                    if entry.get("published_parsed"):
                        try:
                            published = date.fromtimestamp(mktime(entry["published_parsed"]))
                        except (ValueError, OverflowError):
                            pass

                    combined = f"{title} {description}"
                    industry = detect_industry(combined)
                    domain = detect_domain(combined)

                    link = entry.get("link", "")
                    links = []
                    if link:
                        links.append({"url": link, "type": "blog", "title": f"{company} Blog"})

                    items.append(RawResearchItem(
                        title=title,
                        description=description or None,
                        source_type="rss",
                        relevance_score=relevance,
                        source_id=source_id,
                        source_url=link,
                        company_name=company,
                        industry=industry,
                        domain=domain,
                        date_published=published,
                        authors=[],
                        links=links,
                        raw_metadata=json.dumps({
                            "feed_url": url,
                            "company": company,
                            "relevance_score": relevance,
                        }),
                    ))

        return items
