"""Collector management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import CollectionLog
from backend.collectors.arxiv import ArxivCollector
from backend.collectors.semantic_scholar import SemanticScholarCollector
from backend.collectors.rss_blogs import RssBlogCollector

from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/collectors", tags=["collectors"])

COLLECTORS = {
    "arxiv": ArxivCollector(),
    "semantic_scholar": SemanticScholarCollector(),
    "rss": RssBlogCollector(),
}


class CollectorStatus(BaseModel):
    name: str
    last_run: datetime | None = None
    last_status: str | None = None
    items_collected: int = 0


class CollectorRunResult(BaseModel):
    collector: str
    items_found: int
    items_added: int
    errors: list[str] = []


@router.get("", response_model=list[CollectorStatus])
async def list_collectors(db: AsyncSession = Depends(get_db)):
    statuses = []
    for name in COLLECTORS:
        result = await db.execute(
            select(CollectionLog)
            .where(CollectionLog.collector_name == name)
            .order_by(CollectionLog.started_at.desc())
            .limit(1)
        )
        log = result.scalar_one_or_none()
        statuses.append(CollectorStatus(
            name=name,
            last_run=log.finished_at if log else None,
            last_status=log.status if log else None,
            items_collected=log.items_added if log else 0,
        ))
    return statuses


@router.post("/{name}/run", response_model=CollectorRunResult)
async def run_collector(name: str, db: AsyncSession = Depends(get_db)):
    if name not in COLLECTORS:
        raise HTTPException(status_code=404, detail=f"Collector '{name}' not found")

    collector = COLLECTORS[name]
    result = await collector.run(db)

    return CollectorRunResult(
        collector=name,
        items_found=result.items_found,
        items_added=result.items_added,
        errors=result.errors,
    )


@router.get("/logs", response_model=list[dict])
async def get_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CollectionLog)
        .order_by(CollectionLog.started_at.desc())
        .limit(50)
    )
    logs = result.scalars().all()
    return [
        {
            "id": log.id,
            "collector_name": log.collector_name,
            "started_at": log.started_at.isoformat() if log.started_at else None,
            "finished_at": log.finished_at.isoformat() if log.finished_at else None,
            "status": log.status,
            "items_found": log.items_found,
            "items_added": log.items_added,
            "error_message": log.error_message,
        }
        for log in logs
    ]
