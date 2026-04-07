from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

instance_tags = Table(
    "instance_tags",
    Base.metadata,
    Column("instance_id", Integer, ForeignKey("research_instances.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String)  # method, domain, industry, application
    description = Column(Text)

    instances = relationship("ResearchInstance", secondary=instance_tags, back_populates="tags")
