"""Full-text search endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models import ResearchInstance
from backend.services.search import fts_search, fts_facets
from backend.schemas.search import SearchResponse, SearchResult, SearchFacets
from backend.schemas.research_instance import ResearchInstanceResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    rows, total = await fts_search(db, q, limit=per_page, offset=offset)
    sources, industries, domains = await fts_facets(db, q)

    results = []
    for row in rows:
        # Load full instance with relationships
        query = select(ResearchInstance).options(
            selectinload(ResearchInstance.company),
            selectinload(ResearchInstance.tags),
            selectinload(ResearchInstance.people),
            selectinload(ResearchInstance.links),
        ).where(ResearchInstance.id == row.id)
        result = await db.execute(query)
        instance = result.unique().scalar_one_or_none()
        if instance:
            results.append(SearchResult(
                instance=ResearchInstanceResponse.model_validate(instance),
                relevance_score=abs(row.relevance) if hasattr(row, 'relevance') else 0,
                title_snippet=row.title_snippet if hasattr(row, 'title_snippet') else None,
                description_snippet=row.desc_snippet if hasattr(row, 'desc_snippet') else None,
            ))

    return SearchResponse(
        results=results,
        total=total,
        page=page,
        per_page=per_page,
        query=q,
        facets=SearchFacets(sources=sources, industries=industries, domains=domains),
    )
