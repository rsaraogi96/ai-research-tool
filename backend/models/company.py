from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    aliases = Column(Text, default="[]")  # JSON array
    website = Column(String)
    sector = Column(String)  # big_tech, startup, academic, consulting
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    instances = relationship("ResearchInstance", back_populates="company")
