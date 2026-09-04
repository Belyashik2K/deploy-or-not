FROM python:3.14-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./


FROM base AS dev
RUN uv sync --group dev --frozen
COPY . .
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS builder
RUN uv sync --frozen --no-dev


FROM python:3.14-slim AS prod
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /app

RUN useradd --create-home --uid 1000 deploy-or-not

COPY --from=builder /opt/venv /opt/venv
COPY . .


RUN DJANGO_DEBUG=0 python manage.py collectstatic --noinput \
    && chown -R deploy-or-not:deploy-or-not /app/staticfiles

USER deploy-or-not

EXPOSE 8000
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
