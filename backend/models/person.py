from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database import Base

instance_people = Table(
    "instance_people",
    Base.metadata,
    Column("instance_id", Integer, ForeignKey("research_instances.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True),
    Column("role", String, default="author"),
)


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    affiliation = Column(String)
    semantic_scholar_id = Column(String)
    arxiv_author_id = Column(String)
    github_username = Column(String)
    website = Column(String)
    notes = Column(Text)
    is_following = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    instances = relationship("ResearchInstance", secondary=instance_people, back_populates="people")
