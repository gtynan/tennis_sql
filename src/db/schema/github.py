from sqlalchemy import Column, String, DateTime
from datetime import datetime

from .base import BaseTable, BaseModel


class GithubTable(BaseTable):
    __tablename__ = 'github'

    sha = Column(String(50))
    date = Column(DateTime, default=datetime.now)


class GithubBaseSchema(BaseModel):
    sha: str


class GithubCreateSchema(GithubBaseSchema):
    pass


class GithubSchema(GithubBaseSchema):
    date: datetime
