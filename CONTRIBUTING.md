# Contributing

[![CONTRIBUTING на русском](https://img.shields.io/badge/CONTRIBUTING-русский-informational)](CONTRIBUTING.ru.md)

Thanks for taking the time. This is a small joke project, so the bar is simple: it should still be
funny, still be typed, and still pass CI.

## Setup

```bash
uv sync --group dev
uv run pre-commit install
```

## Before opening a pull request

Run what CI runs:

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check api config tests
uv run mypy .
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), matching the
existing history — `feat(i18n): ...`, `fix(urls): ...`, `refactor(docker): ...`.

Keep a pull request to one topic. If you are changing behaviour, add or adjust a test for it.

## Adding a language

The most useful contribution here is a new locale. Phrases are plain JSON, one file per locale in
[`api/phrases/data/`](api/phrases/data) — two moods × three kinds of day × two decisions, and none
of the twelve lists may be empty:

```json
{
  "chill":  { "normal":  { "yes": ["..."], "no": ["..."] },
              "friday":  { "yes": ["..."], "no": ["..."] },
              "weekend": { "yes": ["..."], "no": ["..."] } },
  "savage": { "normal":  { "yes": ["..."], "no": ["..."] },
              "friday":  { "yes": ["..."], "no": ["..."] },
              "weekend": { "yes": ["..."], "no": ["..."] } }
}
```

1. Copy `api/phrases/data/en.json` to `api/phrases/data/<code>.json` and translate it.
2. Add `<code>` to the `Lang` literal in [`api/schemas.py`](api/schemas.py) — it is the single
   source of truth for both validation and the OpenAPI schema.
3. Add `<code>` to `SUPPORTED_LANGS` in
   [`tests/test_phrases_loading.py`](tests/test_phrases_loading.py) and to `LANGS` in the other two
   test modules. The suite then checks the new file's structure automatically.

The structure is validated on load, so a malformed or incomplete file fails loudly instead of
serving half-broken responses.

One thing worth knowing before you translate: the phrases are the whole joke. Translate the tone,
not the words — a literal translation of an English one-liner usually lands flat.

## Reporting a bug

Open an issue with the request you sent and the response you got back. For anything about the
deployed instance, the output of `curl -i` is ideal.
