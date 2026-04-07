"""Tag endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import Tag

from pydantic import BaseModel


class TagResponse(BaseModel):
    id: int
    name: str
    category: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}


class TagListResponse(BaseModel):
    items: list[TagResponse]
    by_category: dict[str, list[TagResponse]] = {}


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=TagListResponse)
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.category, Tag.name))
    tags = result.scalars().all()

    items = [TagResponse.model_validate(t) for t in tags]
    by_category: dict[str, list[TagResponse]] = {}
    for tag in items:
        cat = tag.category or "other"
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tag)

    return TagListResponse(items=items, by_category=by_category)
