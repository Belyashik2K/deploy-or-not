import random
from typing import Any

import pytest
from django.test import Client

from api.phrases import get_phrases
from api.schemas import (
    Day,
    Lang,
    Mood,
)

DECIDE_URL = "/api/v1/decide"
OPENAPI_URL = "/docs/openapi.json"

ALL_DAYS: list[Day] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
MOODS: list[Mood] = ["chill", "savage"]
LANGS: list[Lang] = ["en", "ru"]


def test_returns_200_with_full_payload(client: Client) -> None:
    response = client.get(DECIDE_URL, {"day": "monday", "lang": "en", "mood": "chill"})

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"decision", "day", "message"}
    assert isinstance(body["decision"], bool)
    assert body["day"] == "monday"
    assert body["message"]


def test_works_without_any_query_params(client: Client) -> None:
    response = client.get(DECIDE_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["day"] in ALL_DAYS
    assert isinstance(body["decision"], bool)


@pytest.mark.parametrize("day", ALL_DAYS)
def test_echoes_every_supported_day(client: Client, day: Day) -> None:
    response = client.get(DECIDE_URL, {"day": day})

    assert response.status_code == 200
    assert response.json()["day"] == day


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("mood", MOODS)
def test_every_lang_and_mood_combination_is_served(client: Client, lang: Lang, mood: Mood) -> None:
    normal = getattr(get_phrases(lang), mood).normal
    expected_pool = set(normal.yes) | set(normal.no)

    response = client.get(DECIDE_URL, {"lang": lang, "mood": mood, "day": "monday"})

    assert response.status_code == 200
    assert response.json()["message"] in expected_pool


def test_friday_mostly_refuses_over_the_wire(client: Client) -> None:
    random.seed(20260904)

    decisions = [client.get(DECIDE_URL, {"day": "friday"}).json()["decision"] for _ in range(200)]

    assert sum(decisions) / len(decisions) < 0.5


def test_regular_day_mostly_approves_over_the_wire(client: Client) -> None:
    random.seed(20260904)

    decisions = [
        client.get(DECIDE_URL, {"day": "wednesday"}).json()["decision"] for _ in range(200)
    ]

    assert sum(decisions) / len(decisions) > 0.5


@pytest.mark.parametrize(
    "params",
    [
        {"day": "funday"},
        {"lang": "de"},
        {"mood": "angry"},
        {"day": "Monday"},
    ],
)
def test_invalid_query_params_are_rejected(client: Client, params: dict[str, Any]) -> None:
    response = client.get(DECIDE_URL, params)

    assert response.status_code == 400


def test_unknown_method_is_not_allowed(client: Client) -> None:
    response = client.post(DECIDE_URL)

    assert response.status_code == 405


def test_openapi_schema_documents_the_endpoint(client: Client) -> None:
    response = client.get(OPENAPI_URL)

    assert response.status_code == 200
    schema = response.json()
    assert DECIDE_URL in schema["paths"]
    assert schema["paths"][DECIDE_URL]["get"]["operationId"] == "decideDeployOrNot"
