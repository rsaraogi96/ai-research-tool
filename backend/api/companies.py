"""Company endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import Company, ResearchInstance

from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None = None
    sector: str | None = None
    description: str | None = None
    instance_count: int = 0

    model_config = {"from_attributes": True}


class CompanyListResponse(BaseModel):
    items: list[CompanyResponse]
    total: int


router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=CompanyListResponse)
async def list_companies(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # Get companies with instance counts
    query = (
        select(
            Company,
            func.count(ResearchInstance.id).label("instance_count"),
        )
        .outerjoin(ResearchInstance, Company.id == ResearchInstance.company_id)
        .group_by(Company.id)
        .order_by(func.count(ResearchInstance.id).desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(query)
    rows = result.all()

    total = await db.scalar(select(func.count(Company.id))) or 0

    items = []
    for company, count in rows:
        resp = CompanyResponse.model_validate(company)
        resp.instance_count = count
        items.append(resp)

    return CompanyListResponse(items=items, total=total)
