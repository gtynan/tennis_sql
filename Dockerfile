FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN pip3 install poetry

COPY pyproject.toml poetry.lock .env ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

RUN mkdir src

COPY src/ /src

EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "src.main:app"]
