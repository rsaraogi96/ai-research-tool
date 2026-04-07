"""Full-text search service using SQLite FTS5."""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def fts_search(session: AsyncSession, query: str, limit: int = 20, offset: int = 0):
    """Search research instances using FTS5 with BM25 ranking."""
    clean_query = query.replace('"', '').replace("'", "").strip()
    if not clean_query:
        return [], 0

    sql = text("""
        SELECT
            ri.*,
            bm25(research_instances_fts, 10.0, 5.0, 2.0, 2.0) AS relevance,
            snippet(research_instances_fts, 0, '<mark>', '</mark>', '...', 32) AS title_snippet,
            snippet(research_instances_fts, 1, '<mark>', '</mark>', '...', 64) AS desc_snippet
        FROM research_instances_fts
        JOIN research_instances ri ON ri.id = research_instances_fts.rowid
        WHERE research_instances_fts MATCH :query
        ORDER BY relevance
        LIMIT :limit OFFSET :offset
    """)

    result = await session.execute(sql, {"query": clean_query, "limit": limit, "offset": offset})
    rows = result.fetchall()

    count_sql = text("""
        SELECT COUNT(*) FROM research_instances_fts
        WHERE research_instances_fts MATCH :query
    """)
    count_result = await session.execute(count_sql, {"query": clean_query})
    total = count_result.scalar() or 0

    return rows, total


async def fts_facets(session: AsyncSession, query: str):
    """Get faceted counts for a search query."""
    clean_query = query.replace('"', '').replace("'", "").strip()
    if not clean_query:
        return {}, {}, {}

    # Source facets
    source_sql = text("""
        SELECT ri.source_type, COUNT(*) as cnt
        FROM research_instances_fts
        JOIN research_instances ri ON ri.id = research_instances_fts.rowid
        WHERE research_instances_fts MATCH :query
        GROUP BY ri.source_type
    """)
    result = await session.execute(source_sql, {"query": clean_query})
    sources = {row[0]: row[1] for row in result if row[0]}

    # Industry facets
    industry_sql = text("""
        SELECT ri.industry, COUNT(*) as cnt
        FROM research_instances_fts
        JOIN research_instances ri ON ri.id = research_instances_fts.rowid
        WHERE research_instances_fts MATCH :query AND ri.industry IS NOT NULL
        GROUP BY ri.industry
    """)
    result = await session.execute(industry_sql, {"query": clean_query})
    industries = {row[0]: row[1] for row in result if row[0]}

    # Domain facets
    domain_sql = text("""
        SELECT ri.domain, COUNT(*) as cnt
        FROM research_instances_fts
        JOIN research_instances ri ON ri.id = research_instances_fts.rowid
        WHERE research_instances_fts MATCH :query AND ri.domain IS NOT NULL
        GROUP BY ri.domain
    """)
    result = await session.execute(domain_sql, {"query": clean_query})
    domains = {row[0]: row[1] for row in result if row[0]}

    return sources, industries, domains
