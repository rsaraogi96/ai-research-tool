from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date, timezone

from backend.database import Base
from backend.models.tag import instance_tags
from backend.models.person import instance_people


class ResearchInstance(Base):
    __tablename__ = "research_instances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    source_type = Column(String, nullable=False)  # arxiv, semantic_scholar, rss, manual
    source_id = Column(String)
    source_url = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    industry = Column(String)
    domain = Column(String)
    date_published = Column(Date)
    date_discovered = Column(Date, default=lambda: date.today())
    relevance_score = Column(Float, default=0.0)
    is_curated = Column(Boolean, default=False)
    raw_metadata = Column(Text)  # JSON blob
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("source_type", "source_id", name="uq_source"),
    )

    company = relationship("Company", back_populates="instances")
    tags = relationship("Tag", secondary=instance_tags, back_populates="instances")
    people = relationship("Person", secondary=instance_people, back_populates="instances")
    links = relationship("InstanceLink", back_populates="instance", cascade="all, delete-orphan")


class InstanceLink(Base):
    __tablename__ = "instance_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer, ForeignKey("research_instances.id", ondelete="CASCADE"))
    url = Column(String, nullable=False)
    link_type = Column(String)  # paper, code, blog, video, dataset
    title = Column(String)

    instance = relationship("ResearchInstance", back_populates="links")


class CollectionLog(Base):
    __tablename__ = "collection_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    collector_name = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime)
    status = Column(String)  # running, success, failed
    items_found = Column(Integer, default=0)
    items_added = Column(Integer, default=0)
    error_message = Column(Text)
