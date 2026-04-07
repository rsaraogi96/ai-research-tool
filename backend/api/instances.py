"""Research instance CRUD and listing endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models import ResearchInstance, Tag
from backend.schemas.research_instance import (
    ResearchInstanceResponse,
    ResearchInstanceCreate,
    ResearchInstanceUpdate,
    InstanceListResponse,
)

router = APIRouter(prefix="/instances", tags=["instances"])


@router.get("", response_model=InstanceListResponse)
async def list_instances(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    source_type: str | None = None,
    company_id: int | None = None,
    industry: str | None = None,
    domain: str | None = None,
    is_curated: bool | None = None,
    sort_by: str = "date_discovered",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db),
):
    query = select(ResearchInstance).options(
        selectinload(ResearchInstance.company),
        selectinload(ResearchInstance.tags),
        selectinload(ResearchInstance.people),
        selectinload(ResearchInstance.links),
    )

    if source_type:
        query = query.where(ResearchInstance.source_type == source_type)
    if company_id:
        query = query.where(ResearchInstance.company_id == company_id)
    if industry:
        query = query.where(ResearchInstance.industry == industry)
    if domain:
        query = query.where(ResearchInstance.domain == domain)
    if is_curated is not None:
        query = query.where(ResearchInstance.is_curated == is_curated)

    # Count
    count_query = select(func.count(ResearchInstance.id))
    if source_type:
        count_query = count_query.where(ResearchInstance.source_type == source_type)
    if company_id:
        count_query = count_query.where(ResearchInstance.company_id == company_id)
    if industry:
        count_query = count_query.where(ResearchInstance.industry == industry)
    if domain:
        count_query = count_query.where(ResearchInstance.domain == domain)
    if is_curated is not None:
        count_query = count_query.where(ResearchInstance.is_curated == is_curated)
    total = await db.scalar(count_query) or 0

    # Sort
    sort_col = getattr(ResearchInstance, sort_by, ResearchInstance.date_discovered)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc().nullslast())

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    instances = result.unique().scalars().all()

    return InstanceListResponse(
        items=[ResearchInstanceResponse.model_validate(i) for i in instances],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{instance_id}", response_model=ResearchInstanceResponse)
async def get_instance(instance_id: int, db: AsyncSession = Depends(get_db)):
    query = select(ResearchInstance).options(
        selectinload(ResearchInstance.company),
        selectinload(ResearchInstance.tags),
        selectinload(ResearchInstance.people),
        selectinload(ResearchInstance.links),
    ).where(ResearchInstance.id == instance_id)
    result = await db.execute(query)
    instance = result.unique().scalar_one_or_none()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return ResearchInstanceResponse.model_validate(instance)


@router.post("", response_model=ResearchInstanceResponse, status_code=201)
async def create_instance(data: ResearchInstanceCreate, db: AsyncSession = Depends(get_db)):
    instance = ResearchInstance(
        title=data.title,
        description=data.description,
        source_type=data.source_type,
        source_id=data.source_id,
        source_url=data.source_url,
        company_id=data.company_id,
        industry=data.industry,
        domain=data.domain,
        date_published=data.date_published,
    )
    if data.tag_ids:
        tags = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        instance.tags = list(tags.scalars().all())

    db.add(instance)
    await db.commit()
    await db.refresh(instance)

    # Reload with relationships
    query = select(ResearchInstance).options(
        selectinload(ResearchInstance.company),
        selectinload(ResearchInstance.tags),
        selectinload(ResearchInstance.people),
        selectinload(ResearchInstance.links),
    ).where(ResearchInstance.id == instance.id)
    result = await db.execute(query)
    instance = result.unique().scalar_one()
    return ResearchInstanceResponse.model_validate(instance)


@router.put("/{instance_id}", response_model=ResearchInstanceResponse)
async def update_instance(instance_id: int, data: ResearchInstanceUpdate, db: AsyncSession = Depends(get_db)):
    query = select(ResearchInstance).options(
        selectinload(ResearchInstance.tags),
    ).where(ResearchInstance.id == instance_id)
    result = await db.execute(query)
    instance = result.unique().scalar_one_or_none()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "tag_ids":
            tags = await db.execute(select(Tag).where(Tag.id.in_(value)))
            instance.tags = list(tags.scalars().all())
        else:
            setattr(instance, field, value)

    await db.commit()

    # Reload
    query = select(ResearchInstance).options(
        selectinload(ResearchInstance.company),
        selectinload(ResearchInstance.tags),
        selectinload(ResearchInstance.people),
        selectinload(ResearchInstance.links),
    ).where(ResearchInstance.id == instance_id)
    result = await db.execute(query)
    instance = result.unique().scalar_one()
    return ResearchInstanceResponse.model_validate(instance)


@router.delete("/{instance_id}", status_code=204)
async def delete_instance(instance_id: int, db: AsyncSession = Depends(get_db)):
    instance = await db.get(ResearchInstance, instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    await db.delete(instance)
    await db.commit()
