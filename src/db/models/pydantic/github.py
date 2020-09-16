from datetime import datetime

from .base import BaseModel


class GithubBase(BaseModel):
    sha: str


class GithubCreate(GithubBase):
    pass


class Github(GithubBase):
    date: datetime
