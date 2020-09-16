from sqlalchemy import Column, String, DateTime
from datetime import datetime

from .base import Base


class Github(Base):
    __tablename__ = 'github'

    sha = Column(String(50))
    date = Column(DateTime, default=datetime.now)
