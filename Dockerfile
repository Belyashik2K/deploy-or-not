FROM python:3.14-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./


FROM base AS dev
RUN uv sync --group dev --frozen
COPY . .
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS builder
RUN uv sync --frozen --no-dev


FROM python:3.13-slim AS prod
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN useradd --create-home --uid 1000 deploy-or-not

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

USER deploy-or-not

EXPOSE 8000
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]