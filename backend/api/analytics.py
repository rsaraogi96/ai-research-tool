"""Analytics and pattern detection endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.services.analytics import get_overview, get_breakdown, get_timeline, get_company_activity
from backend.schemas.analytics import (
    AnalyticsOverview,
    IndustryBreakdown,
    DomainBreakdown,
    SourceBreakdown,
    TimelineData,
    CompanyActivityData,
    BreakdownItem,
    TimelinePoint,
    CompanyActivity,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
async def overview(db: AsyncSession = Depends(get_db)):
    data = await get_overview(db)
    return AnalyticsOverview(**data)


@router.get("/industry", response_model=IndustryBreakdown)
async def industry_breakdown(db: AsyncSession = Depends(get_db)):
    items = await get_breakdown(db, "industry")
    return IndustryBreakdown(items=[BreakdownItem(**i) for i in items])


@router.get("/domain", response_model=DomainBreakdown)
async def domain_breakdown(db: AsyncSession = Depends(get_db)):
    items = await get_breakdown(db, "domain")
    return DomainBreakdown(items=[BreakdownItem(**i) for i in items])


@router.get("/source", response_model=SourceBreakdown)
async def source_breakdown(db: AsyncSession = Depends(get_db)):
    items = await get_breakdown(db, "source_type")
    return SourceBreakdown(items=[BreakdownItem(**i) for i in items])


@router.get("/timeline", response_model=TimelineData)
async def timeline(
    granularity: str = Query("week", pattern="^(week|month)$"),
    db: AsyncSession = Depends(get_db),
):
    points = await get_timeline(db, granularity)
    return TimelineData(points=[TimelinePoint(**p) for p in points])


@router.get("/companies", response_model=CompanyActivityData)
async def company_activity(db: AsyncSession = Depends(get_db)):
    items = await get_company_activity(db)
    return CompanyActivityData(items=[CompanyActivity(**i) for i in items])
