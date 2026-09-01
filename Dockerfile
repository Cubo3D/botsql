FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen

FROM python:3.14-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages

COPY ./src .
COPY ./alembic .
COPY alembic.ini .

CMD ["python", "src/bot.py"]