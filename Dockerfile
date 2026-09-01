FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN uv pip install -r requirements.txt --system

FROM python:3.14-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages

COPY bot-refatorado.py .

CMD ["python", "bot-refatorado.py"]
