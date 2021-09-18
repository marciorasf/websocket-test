FROM python:3.9.7-slim-buster

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry export --output requirements.txt
RUN pip install -r requirements.txt

COPY server/ server/

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "server.main:app"]
