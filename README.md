<div align="center">

# Deploy-or-Not-as-a-Service

**To deploy or not to deploy, that is the question...**

[![Live API](https://img.shields.io/badge/live-donaas.belyashik2k.ru-2ea44f)](https://donaas.belyashik2k.ru/docs)
[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Modern REST](https://img.shields.io/badge/Modern%20REST-0C4B33?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTA4MCIgaGVpZ2h0PSIxMDgwIiB2aWV3Qm94PSIwIDAgMTA4MCAxMDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMiA3MDQuMDJMMTQ1LjQ1OSA0NjYuMTlMMjc3Ljg4MyA3MDQuMDJMMTQ1LjQ1OSA5NDEuODQ5TDIgNzA0LjAyWiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTE0NS40NTkgOTQxLjg0OUwyIDcwNC4wMkgyNzcuODgzTDE0NS40NTkgOTQxLjg0OVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik02NzguOTQ4IDcwNC4wMzVMMzQxLjIzIDEzOEwyMjcuMDcxIDMyOC4yNjRMNDM2LjM2MiA3MDQuMDM1TDMwMy4xNzcgOTQxLjg2NEg1MzYuMjVMNjc4Ljk0OCA3MDQuMDM1WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTY3OC45MzcgNzA0LjAyNkg0MzYuMzVMMzAzLjE2NiA5NDEuODU2SDUzNi4yMzlMNjc4LjkzNyA3MDQuMDI2WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTEwNzguMTcgNzA0LjAzNUw3NDAuNDUxIDEzOEw2MjYuMjkzIDMyOC4yNjRMODM1LjU4MyA3MDQuMDM1TDcwMi4zOTkgOTQxLjg2NEg5MzUuNDcyTDEwNzguMTcgNzA0LjAzNVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMDc4LjE3IDcwNC4wMzVIODM1LjU4M0w3MDIuMzk5IDk0MS44NjRIOTM1LjQ3MkwxMDc4LjE3IDcwNC4wMzVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K&color=35544A)](https://github.com/wemake-services/django-modern-rest)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-2A6DB2)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/Belyashik2K/deploy-or-not/actions/workflows/ci.yml/badge.svg)](https://github.com/Belyashik2K/deploy-or-not/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![README на русском](https://img.shields.io/badge/README-русский-informational)](README.ru.md)

</div>

<details>
<summary><b>Contents</b></summary>

- [About](#about)
- [How it works](#how-it-works)
- [Usage](#usage)
- [API reference](#api-reference)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Development](#development)
- [License](#license)

</details>

## About

**17:34 on a Friday.** You are already picturing the evening — beer open, match on, laptop shut.
And then the call comes in, because someone upstairs decided this ships today. **Right now.** Not
three hours ago, not Monday morning. You see, "the client is waiting" and "it's a one-line fix".

You open the terminal, your finger hovers over `Enter` — and somewhere in the back of your head one
thought shows up: *"should I, though?"*

**Sound familiar?** We won't stop you. We will, at least, tell you honestly what we think.

> **Spoiler:** on Fridays we think badly of it. Very badly.

## How it works

Send a request, get a verdict: true/false, the day it was judged by, and a phrase to justify it to
your team lead. Or not.

```bash
curl "https://donaas.belyashik2k.ru/api/v1/decide?day=thursday"
```

```json
{
  "decision": true,
  "day": "thursday",
  "message": "Green across the board. Push the button and go get a coffee."
}
```

It is all in the odds:

- 85% yes on a normal day — the API is friendly about it, roughly like a junior who still trusts
  everyone.
- 20% yes on Fridays — it turns into the senior who has seen a Friday production incident and
  flinches at a commit named `fix(auth): typo in comment`.
- Two moods: `chill` warns you gently, `savage` goes straight for the person.
- Two languages out of the box — `en` and `ru`, phrases live in a plain JSON file, no magic.
- No key, no signup, no client — a plain `GET`, and your excuse is ready.

Built with Django and [django-modern-rest](https://pypi.org/project/django-modern-rest/), fully
typed, no database, no state — just a coin flip with opinions.

## Usage

### Online

- **Swagger UI:** <https://donaas.belyashik2k.ru/docs>
- **OpenAPI schema:** <https://donaas.belyashik2k.ru/docs/openapi.json>

From Python, with [httpx](https://www.python-httpx.org/):

```python
import asyncio

import httpx


async def main() -> None:
    async with httpx.AsyncClient(base_url="https://donaas.belyashik2k.ru") as client:
        response = await client.get("/api/v1/decide", params={"day": "friday", "mood": "savage"})
        print(response.json()["message"])


if __name__ == "__main__":
    asyncio.run(main())
```

### Locally

Copy the example environment file — every variable is documented inside it:

```bash
cp .env.example .env
```

With [Task](https://taskfile.dev) and Docker:

```bash
task dev BUILD=1
```

The API comes up on `http://localhost:8000` with the source directory mounted, so edits reload live.
`task --list` shows the rest.

`ENV=prod` switches to the production stack. It assumes a reverse proxy is already in place and just
publishes the app on `127.0.0.1:${APP_PORT}` for it — nginx or anything else on the host proxies
there, a Traefik container reads the labels instead. If the host has nothing yet,
`TRAEFIK_MODE=compose` brings up a Traefik alongside the app, with Let's Encrypt certificates:

```bash
task prod BUILD=1 TRAEFIK_MODE=compose
```

Plain compose works too — dev, production, and production carrying its own Traefik:

```bash
# dev: hot reload, debug on, port on the host
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# production behind a proxy you already run
docker compose -f docker-compose.yml up -d --build

# production with Traefik brought up alongside it
docker compose -f docker-compose.yml -f docker-compose.traefik.yml up -d --build
```

Production needs real values for `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DOMAIN` and
`ACME_EMAIL`, plus ports `80`/`443` reachable from the internet for the ACME challenge.

Or skip Docker entirely:

```bash
DJANGO_DEBUG=1 uv run python manage.py runserver
```

## API reference

`GET /api/v1/decide`, all parameters optional:

| Parameter | Values                         | Default                    |
|-----------|--------------------------------|----------------------------|
| `lang`    | `en`, `ru`                     | `en`                       |
| `day`     | `monday` … `sunday`, lowercase | the server's today, on UTC |
| `mood`    | `chill`, `savage`              | `chill`                    |

```json
{
  "decision": false,
  "day": "friday",
  "message": "Friday deploy? Get some help."
}
```

Unknown values give `400`. Over ten requests a second per client gives `429`. CORS is open, so this
works straight from a browser. Everything else is in
[Swagger](https://donaas.belyashik2k.ru/docs).

## Project structure

```
api/
  phrases/
    data/          en.json, ru.json — the phrases themselves
    loader.py      reads and validates a locale on first use
    schemas.py     the shape every phrase file must match
  schemas.py       query and response models, and the Lang / Day / Mood literals
  services.py      the most critical code here — the coin flip and the odds behind it
  views.py         the single controller
config/            Django settings, URLs, ASGI entrypoint, OpenAPI metadata
tests/             endpoint, decision logic and phrase file structure
```

## Contributing

Bug reports and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
The most useful contribution is a new language.

## Development

The project targets Python 3.14 and uses [uv](https://docs.astral.sh/uv/) for dependencies:

```bash
uv sync --group dev
```

Tests, linters and type checking — the same three commands CI runs:

```bash
uv run pytest
```

```bash
uv run ruff check . && uv run ruff format --check api config tests
```

```bash
uv run mypy .
```

Hooks are configured in [`.pre-commit-config.yaml`](.pre-commit-config.yaml); install them once and
they run on every commit:

```bash
uv run pre-commit install
```

## License

Released under the [MIT License](LICENSE).
