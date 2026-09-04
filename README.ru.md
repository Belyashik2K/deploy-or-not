<div align="center">

# Deploy-or-Not-as-a-Service

**Катить или не катить, вот в чём вопрос...**

[![Живое API](https://img.shields.io/badge/live-donaas.belyashik2k.ru-2ea44f)](https://donaas.belyashik2k.ru/docs)
[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Modern REST](https://img.shields.io/badge/Modern%20REST-0C4B33?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTA4MCIgaGVpZ2h0PSIxMDgwIiB2aWV3Qm94PSIwIDAgMTA4MCAxMDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMiA3MDQuMDJMMTQ1LjQ1OSA0NjYuMTlMMjc3Ljg4MyA3MDQuMDJMMTQ1LjQ1OSA5NDEuODQ5TDIgNzA0LjAyWiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTE0NS40NTkgOTQxLjg0OUwyIDcwNC4wMkgyNzcuODgzTDE0NS40NTkgOTQxLjg0OVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik02NzguOTQ4IDcwNC4wMzVMMzQxLjIzIDEzOEwyMjcuMDcxIDMyOC4yNjRMNDM2LjM2MiA3MDQuMDM1TDMwMy4xNzcgOTQxLjg2NEg1MzYuMjVMNjc4Ljk0OCA3MDQuMDM1WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTY3OC45MzcgNzA0LjAyNkg0MzYuMzVMMzAzLjE2NiA5NDEuODU2SDUzNi4yMzlMNjc4LjkzNyA3MDQuMDI2WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTEwNzguMTcgNzA0LjAzNUw3NDAuNDUxIDEzOEw2MjYuMjkzIDMyOC4yNjRMODM1LjU4MyA3MDQuMDM1TDcwMi4zOTkgOTQxLjg2NEg5MzUuNDcyTDEwNzguMTcgNzA0LjAzNVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMDc4LjE3IDcwNC4wMzVIODM1LjU4M0w3MDIuMzk5IDk0MS44NjRIOTM1LjQ3MkwxMDc4LjE3IDcwNC4wMzVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K&color=35544A)](https://github.com/wemake-services/django-modern-rest)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-2A6DB2)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/Belyashik2K/deploy-or-not/actions/workflows/ci.yml/badge.svg)](https://github.com/Belyashik2K/deploy-or-not/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![README in English](https://img.shields.io/badge/README-english-informational)](README.md)

</div>

## Содержание

- [О проекте](#о-проекте)
- [Как это работает](#как-это-работает)
- [Быстрый старт](#быстрый-старт)
- [Как пользоваться](#как-пользоваться)
- [Описание API](#описание-api)
- [Структура проекта](#структура-проекта)
- [Как внести вклад](#как-внести-вклад)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

## О проекте

**17:34, вечер, пятница.** Вы уже мысленно представляете, как откроете пиво, включите футбол,
и... И тут тимлид вызывает на созвон, потому что начальник решил катить в прод. **Прямо сейчас.**
Не три часа назад и не в понедельник утром. Видите ли, «клиент ждёт» и «это же мелкий фикс».

Вы открываете терминал, палец завис над `Enter` — и в этот момент где-то внутри возникает одна
мысль: *«А стоит ли?»*

**Знакомо?** Мы вас не останавливаем, но хотя бы честно скажем, что думаем по этому поводу.

> **Спойлер:** по пятницам мы думаем плохо. Очень плохо.

## Как это работает

Отправляете запрос — получаете вердикт: true/false, день, по которому судили, и фразу, которой
можно оправдаться (или нет) перед тимлидом.

Вся суть — в вероятностях:

- 85% «да» в обычный день — API настроено доброжелательно, почти как джун, который ещё всем верит.
- 20% «да» по пятницам — оно превращается в сеньора, который видел прод по пятницам и трясётся при
  коммите `fix(auth): typo in comment`.
- Два настроения: `chill` мягко предупреждает, `savage` — сразу переходит на личности.
- Два языка из коробки — `en` и `ru`, фразы лежат обычным JSON-файлом, никакой магии.
- Без ключей, без регистрации, без клиента — обычный `GET`, и оправдание уже готово.

Написано на Django и [django-modern-rest](https://pypi.org/project/django-modern-rest/), полностью
типизировано, без базы и без состояния — просто подбрасывание монетки, но с характером.

## Быстрый старт

Один запрос — один вердикт, без ключей и настройки:

```bash
curl "https://donaas.belyashik2k.ru/api/v1/decide?lang=ru&day=thursday"
```

```json
{
  "decision": true,
  "day": "thursday",
  "message": "Го. Ты даже тесты написал, я почти горжусь."
}
```

Замените на `&day=friday&mood=savage` — и тон поменяется.

## Как пользоваться

### Онлайн

- **Swagger UI:** <https://donaas.belyashik2k.ru/docs>
- **OpenAPI-схема:** <https://donaas.belyashik2k.ru/docs/openapi.json>

```bash
curl "https://donaas.belyashik2k.ru/api/v1/decide?day=friday&mood=savage"
```

Или из Python, через [httpx](https://www.python-httpx.org/):

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

### Локально

Скопируйте пример файла окружения — каждая переменная описана внутри комментарием:

```bash
cp .env.example .env
```

С [Task](https://taskfile.dev) и Docker:

```bash
task dev BUILD=1
```

API поднимется на `http://localhost:8000`, каталог проекта примонтирован, так что правки
подхватываются на лету. Остальное покажет `task --list`.

`ENV=prod` переключает на продовый стек. Он исходит из того, что реверс-прокси уже есть, и просто
публикует приложение на `127.0.0.1:${APP_PORT}` — nginx или что угодно с хоста проксирует туда,
а контейнер с Traefik вместо этого читает лейблы. Если на хосте ничего нет, `TRAEFIK_MODE=compose`
поднимет Traefik рядом с приложением, вместе с сертификатами Let's Encrypt:

```bash
task prod BUILD=1 TRAEFIK_MODE=compose
```

Голым compose тоже можно — dev, прод и прод со своим Traefik:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
docker compose -f docker-compose.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.traefik.yml up -d --build
```

Проду нужны настоящие значения `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DOMAIN` и
`ACME_EMAIL`, а ещё доступные из интернета порты `80`/`443` для ACME-челленджа.

Или вообще без Docker:

```bash
DJANGO_DEBUG=1 uv run python manage.py runserver
```

## Описание API

`GET /api/v1/decide`, все параметры необязательные:

| Параметр | Значения                               | По умолчанию                           |
|----------|----------------------------------------|----------------------------------------|
| `lang`   | `en`, `ru`                             | `en`                                   |
| `day`    | `monday` … `sunday`, в нижнем регистре | сегодня по часам сервера, а они на UTC |
| `mood`   | `chill`, `savage`                      | `chill`                                |

```json
{
  "decision": false,
  "day": "friday",
  "message": "Нет. Тебе напомнить, что в прошлый раз в этой же ситуации ты написал 'прод лежит, дай и я полежу'?"
}
```

Неизвестные значения дают `400`. Больше десяти запросов в секунду с клиента — `429`. CORS открыт,
так что дёргать можно прямо из браузера. Остальное есть в
[Swagger](https://donaas.belyashik2k.ru/docs).

## Структура проекта

```
api/
  phrases/
    data/          en.json, ru.json — сами фразы
    loader.py      читает и валидирует локаль при первом обращении
    schemas.py     форма, которой обязан соответствовать файл фраз
  schemas.py       модели запроса и ответа, литералы Lang / Day / Mood
  services.py      самый ответственный код — подбрасывание монетки и вероятности
  views.py         единственный контроллер
config/            настройки Django, URL, точка входа ASGI, метаданные OpenAPI
tests/             эндпоинт, логика решения и структура файлов фраз
```

## Как внести вклад

Баг-репорты и пул-реквесты приветствуются — подробности в [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md).
Самый полезный вклад — новый язык.

## Разработка

Проект рассчитан на Python 3.14, зависимости — через [uv](https://docs.astral.sh/uv/):

```bash
uv sync --group dev
```

Тесты, линтеры и проверка типов — те же три команды, что гоняет CI:

```bash
uv run pytest
```

```bash
uv run ruff check . && uv run ruff format --check api config tests
```

```bash
uv run mypy .
```

Хуки описаны в [`.pre-commit-config.yaml`](.pre-commit-config.yaml); установите один раз, дальше они
отрабатывают на каждом коммите:

```bash
uv run pre-commit install
```

## Лицензия

Распространяется под [лицензией MIT](LICENSE).
