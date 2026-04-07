from pydantic import BaseModel
from datetime import date, datetime


class InstanceLinkResponse(BaseModel):
    id: int
    url: str
    link_type: str | None = None
    title: str | None = None

    model_config = {"from_attributes": True}


class TagResponse(BaseModel):
    id: int
    name: str
    category: str | None = None

    model_config = {"from_attributes": True}


class PersonBrief(BaseModel):
    id: int
    name: str
    affiliation: str | None = None
    is_following: bool = False

    model_config = {"from_attributes": True}


class CompanyBrief(BaseModel):
    id: int
    name: str
    sector: str | None = None

    model_config = {"from_attributes": True}


class ResearchInstanceResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    source_type: str
    source_id: str | None = None
    source_url: str | None = None
    company: CompanyBrief | None = None
    industry: str | None = None
    domain: str | None = None
    date_published: date | None = None
    date_discovered: date | None = None
    relevance_score: float = 0.0
    is_curated: bool = False
    tags: list[TagResponse] = []
    people: list[PersonBrief] = []
    links: list[InstanceLinkResponse] = []
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ResearchInstanceCreate(BaseModel):
    title: str
    description: str | None = None
    source_type: str = "manual"
    source_id: str | None = None
    source_url: str | None = None
    company_id: int | None = None
    industry: str | None = None
    domain: str | None = None
    date_published: date | None = None
    tag_ids: list[int] = []


class ResearchInstanceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    industry: str | None = None
    domain: str | None = None
    relevance_score: float | None = None
    is_curated: bool | None = None
    company_id: int | None = None
    tag_ids: list[int] | None = None


class InstanceListResponse(BaseModel):
    items: list[ResearchInstanceResponse]
    total: int
    page: int
    per_page: int
