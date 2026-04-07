from pydantic import BaseModel
from backend.schemas.research_instance import ResearchInstanceResponse


class SearchResult(BaseModel):
    instance: ResearchInstanceResponse
    relevance_score: float
    title_snippet: str | None = None
    description_snippet: str | None = None


class SearchFacets(BaseModel):
    sources: dict[str, int] = {}
    industries: dict[str, int] = {}
    domains: dict[str, int] = {}


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    page: int
    per_page: int
    query: str
    facets: SearchFacets
