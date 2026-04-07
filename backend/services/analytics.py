"""Analytics service for pattern detection."""
from datetime import date, timedelta

from sqlalchemy import text, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import ResearchInstance, Company, Person


async def get_overview(session: AsyncSession) -> dict:
    total = await session.scalar(select(func.count(ResearchInstance.id)))
    week_ago = date.today() - timedelta(days=7)
    this_week = await session.scalar(
        select(func.count(ResearchInstance.id)).where(ResearchInstance.date_discovered >= week_ago)
    )
    companies = await session.scalar(select(func.count(Company.id)))
    following = await session.scalar(
        select(func.count(Person.id)).where(Person.is_following == True)
    )
    sources = await session.scalar(
        select(func.count(func.distinct(ResearchInstance.source_type)))
    )
    return {
        "total_instances": total or 0,
        "instances_this_week": this_week or 0,
        "total_companies": companies or 0,
        "total_people_following": following or 0,
        "sources_active": sources or 0,
    }


async def get_breakdown(session: AsyncSession, field: str) -> list[dict]:
    col = getattr(ResearchInstance, field)
    result = await session.execute(
        select(col, func.count(ResearchInstance.id).label("cnt"))
        .where(col.isnot(None))
        .group_by(col)
        .order_by(func.count(ResearchInstance.id).desc())
    )
    rows = result.all()
    total = sum(r[1] for r in rows) or 1
    return [{"label": r[0], "count": r[1], "percentage": round(r[1] / total * 100, 1)} for r in rows]


async def get_timeline(session: AsyncSession, granularity: str = "week") -> list[dict]:
    if granularity == "month":
        fmt = "%Y-%m"
    else:
        fmt = "%Y-%W"

    sql = text(f"""
        SELECT strftime(:fmt, date_discovered) as period, COUNT(*) as cnt
        FROM research_instances
        WHERE date_discovered IS NOT NULL
        GROUP BY period
        ORDER BY period
    """)
    result = await session.execute(sql, {"fmt": fmt})
    return [{"date": row[0], "count": row[1]} for row in result]


async def get_company_activity(session: AsyncSession) -> list[dict]:
    sql = text("""
        SELECT c.name, strftime('%Y-%m', ri.date_discovered) as month, COUNT(*) as cnt
        FROM research_instances ri
        JOIN companies c ON ri.company_id = c.id
        WHERE ri.date_discovered IS NOT NULL
        GROUP BY c.name, month
        ORDER BY c.name, month
    """)
    result = await session.execute(sql)
    return [{"company": row[0], "month": row[1], "count": row[2]} for row in result]
