FROM python:3.10 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app .
COPY templates/ templates

CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
