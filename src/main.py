from fastapi import FastAPI

from .db.db import DBClient

app = FastAPI()


# dependency
def get_db():
    db = DBClient()
    try:
        yield db.session
    finally:
        db.session.close()
