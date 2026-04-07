import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event, text

from backend.config import settings

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "research.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


FTS5_SETUP_SQL = [
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS research_instances_fts USING fts5(
        title,
        description,
        industry,
        domain,
        content='research_instances',
        content_rowid='id',
        tokenize='porter unicode61'
    )
    """,
    """
    CREATE TRIGGER IF NOT EXISTS research_instances_ai AFTER INSERT ON research_instances BEGIN
      INSERT INTO research_instances_fts(rowid, title, description, industry, domain)
      VALUES (new.id, new.title, new.description, new.industry, new.domain);
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS research_instances_ad AFTER DELETE ON research_instances BEGIN
      INSERT INTO research_instances_fts(research_instances_fts, rowid, title, description, industry, domain)
      VALUES ('delete', old.id, old.title, old.description, old.industry, old.domain);
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS research_instances_au AFTER UPDATE ON research_instances BEGIN
      INSERT INTO research_instances_fts(research_instances_fts, rowid, title, description, industry, domain)
      VALUES ('delete', old.id, old.title, old.description, old.industry, old.domain);
      INSERT INTO research_instances_fts(rowid, title, description, industry, domain)
      VALUES (new.id, new.title, new.description, new.industry, new.domain);
    END
    """,
]


async def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        for sql in FTS5_SETUP_SQL:
            await conn.execute(text(sql))


async def get_db():
    async with async_session() as session:
        yield session
