"""Base collector interface for data collection pipeline."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from backend.models import ResearchInstance, CollectionLog, Company


@dataclass
class RawResearchItem:
    title: str
    description: str | None = None
    source_type: str = ""
    source_id: str = ""
    source_url: str = ""
    company_name: str | None = None
    industry: str | None = None
    domain: str | None = None
    date_published: Any = None
    authors: list[str] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)
    raw_metadata: str = "{}"


@dataclass
class CollectionResult:
    collector_name: str
    items_found: int = 0
    items_added: int = 0
    errors: list[str] = field(default_factory=list)


class BaseCollector(ABC):
    name: str = "base"
    schedule_interval_hours: int = 6

    @abstractmethod
    async def collect(self, since: datetime | None = None) -> list[RawResearchItem]:
        ...

    async def _resolve_company(self, session: AsyncSession, name: str | None) -> int | None:
        if not name:
            return None
        result = await session.execute(select(Company).where(Company.name == name))
        company = result.scalar_one_or_none()
        if company:
            return company.id
        # Check aliases
        result = await session.execute(select(Company))
        for c in result.scalars():
            import json
            aliases = json.loads(c.aliases) if c.aliases else []
            if name in aliases or name.lower() in [a.lower() for a in aliases]:
                return c.id
        return None

    async def run(self, session: AsyncSession) -> CollectionResult:
        log = CollectionLog(
            collector_name=self.name,
            started_at=datetime.now(timezone.utc),
            status="running",
        )
        session.add(log)
        await session.commit()

        result = CollectionResult(collector_name=self.name)

        try:
            # Get last successful run time
            last_run = await session.execute(
                select(CollectionLog.finished_at)
                .where(CollectionLog.collector_name == self.name)
                .where(CollectionLog.status == "success")
                .order_by(CollectionLog.finished_at.desc())
                .limit(1)
            )
            since = last_run.scalar_one_or_none()

            items = await self.collect(since=since)
            result.items_found = len(items)

            for item in items:
                try:
                    company_id = await self._resolve_company(session, item.company_name)
                    instance = ResearchInstance(
                        title=item.title,
                        description=item.description,
                        source_type=item.source_type,
                        source_id=item.source_id,
                        source_url=item.source_url,
                        company_id=company_id,
                        industry=item.industry,
                        domain=item.domain,
                        date_published=item.date_published,
                        raw_metadata=item.raw_metadata,
                    )
                    # Try insert, skip on duplicate
                    existing = await session.execute(
                        select(ResearchInstance).where(
                            ResearchInstance.source_type == item.source_type,
                            ResearchInstance.source_id == item.source_id,
                        )
                    )
                    if not existing.scalar_one_or_none():
                        session.add(instance)
                        await session.flush()

                        # Add links
                        from backend.models import InstanceLink
                        for link in item.links:
                            session.add(InstanceLink(
                                instance_id=instance.id,
                                url=link.get("url", ""),
                                link_type=link.get("type", ""),
                                title=link.get("title", ""),
                            ))

                        result.items_added += 1
                except Exception as e:
                    result.errors.append(f"Item '{item.title[:50]}': {str(e)}")

            await session.commit()
            log.status = "success"
            log.items_found = result.items_found
            log.items_added = result.items_added
            log.finished_at = datetime.now(timezone.utc)
            await session.commit()

        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            log.finished_at = datetime.now(timezone.utc)
            await session.commit()
            result.errors.append(str(e))

        return result
