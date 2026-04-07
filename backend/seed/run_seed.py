"""Seed the database with reference data (tags, companies)."""
import asyncio
from sqlalchemy import select

from backend.database import init_db, async_session
from backend.models import Tag, Company
from backend.seed.seed_data import TAGS, COMPANIES


async def seed():
    await init_db()

    async with async_session() as session:
        # Seed tags
        existing_tags = set()
        result = await session.execute(select(Tag.name))
        existing_tags = {row[0] for row in result}

        added_tags = 0
        for name, category in TAGS:
            if name not in existing_tags:
                session.add(Tag(name=name, category=category))
                added_tags += 1
        await session.commit()
        print(f"Seeded {added_tags} tags (skipped {len(TAGS) - added_tags} existing)")

        # Seed companies
        existing_companies = set()
        result = await session.execute(select(Company.name))
        existing_companies = {row[0] for row in result}

        added_companies = 0
        for comp in COMPANIES:
            if comp["name"] not in existing_companies:
                session.add(Company(**comp))
                added_companies += 1
        await session.commit()
        print(f"Seeded {added_companies} companies (skipped {len(COMPANIES) - added_companies} existing)")


if __name__ == "__main__":
    asyncio.run(seed())
