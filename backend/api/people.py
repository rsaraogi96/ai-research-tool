"""People endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models import Person

from pydantic import BaseModel
from datetime import datetime


class PersonResponse(BaseModel):
    id: int
    name: str
    email: str | None = None
    affiliation: str | None = None
    semantic_scholar_id: str | None = None
    github_username: str | None = None
    website: str | None = None
    notes: str | None = None
    is_following: bool = False
    instance_count: int = 0

    model_config = {"from_attributes": True}


class PersonCreate(BaseModel):
    name: str
    email: str | None = None
    affiliation: str | None = None
    website: str | None = None
    notes: str | None = None
    is_following: bool = False


class PersonListResponse(BaseModel):
    items: list[PersonResponse]
    total: int


router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=PersonListResponse)
async def list_people(
    following_only: bool = False,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Person).options(selectinload(Person.instances))
    count_query = select(func.count(Person.id))

    if following_only:
        query = query.where(Person.is_following == True)
        count_query = count_query.where(Person.is_following == True)

    total = await db.scalar(count_query) or 0
    query = query.order_by(Person.name).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    people = result.unique().scalars().all()

    items = []
    for p in people:
        resp = PersonResponse.model_validate(p)
        resp.instance_count = len(p.instances)
        items.append(resp)

    return PersonListResponse(items=items, total=total)


@router.post("", response_model=PersonResponse, status_code=201)
async def create_person(data: PersonCreate, db: AsyncSession = Depends(get_db)):
    person = Person(**data.model_dump())
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return PersonResponse.model_validate(person)


@router.patch("/{person_id}/follow")
async def toggle_follow(person_id: int, db: AsyncSession = Depends(get_db)):
    person = await db.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person.is_following = not person.is_following
    await db.commit()
    return {"id": person_id, "is_following": person.is_following}
