import random
from datetime import datetime

import pytest
from pytest import MonkeyPatch

from api import services
from api.phrases import get_phrases
from api.schemas import (
    Day,
    DecideQuery,
    Lang,
    Mood,
)
from api.services import (
    FRIDAY_YES_CHANCE,
    NORMAL_YES_CHANCE,
    WEEKEND_YES_CHANCE,
    _day_kind,
    decide,
)

ALL_DAYS: list[Day] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
WEEKEND_DAYS: list[Day] = ["saturday", "sunday"]
WORKDAYS: list[Day] = [d for d in ALL_DAYS if d not in {"friday", *WEEKEND_DAYS}]
MOODS: list[Mood] = ["chill", "savage"]
LANGS: list[Lang] = ["en", "ru"]

SAMPLE_SIZE = 2000


def _frozen_timezone(moment: datetime) -> type:
    """Stand-in for `django.utils.timezone` in `api.services`, frozen on a given day."""

    class Frozen:
        @staticmethod
        def localtime() -> datetime:
            return moment

    return Frozen


def _yes_ratio(day: Day, *, seed: int = 20260904, size: int = SAMPLE_SIZE) -> float:
    random.seed(seed)
    query = DecideQuery(day=day)
    yes = sum(decide(query).decision for _ in range(size))
    return yes / size


@pytest.mark.parametrize("day", WORKDAYS)
def test_workdays_mostly_say_yes(day: Day) -> None:
    ratio = _yes_ratio(day)

    assert ratio > 0.5
    assert ratio == pytest.approx(NORMAL_YES_CHANCE, abs=0.05)


def test_friday_mostly_says_no() -> None:
    ratio = _yes_ratio("friday")

    assert ratio < 0.5
    assert ratio == pytest.approx(FRIDAY_YES_CHANCE, abs=0.05)


@pytest.mark.parametrize("day", WEEKEND_DAYS)
def test_weekend_says_no_even_more_than_friday(day: Day) -> None:
    ratio = _yes_ratio(day)

    assert ratio < _yes_ratio("friday")
    assert ratio == pytest.approx(WEEKEND_YES_CHANCE, abs=0.05)


@pytest.mark.parametrize("day", WORKDAYS)
def test_friday_is_stricter_than_any_workday(day: Day) -> None:
    assert _yes_ratio("friday") < _yes_ratio(day)


def test_chances_are_ordered_weekend_friday_normal() -> None:
    assert 0 <= WEEKEND_YES_CHANCE < FRIDAY_YES_CHANCE < NORMAL_YES_CHANCE <= 1


@pytest.mark.parametrize(
    ("day", "roll", "expected"),
    [
        ("friday", FRIDAY_YES_CHANCE - 0.01, True),
        ("friday", FRIDAY_YES_CHANCE + 0.01, False),
        ("monday", NORMAL_YES_CHANCE - 0.01, True),
        ("monday", NORMAL_YES_CHANCE + 0.01, False),
        ("saturday", WEEKEND_YES_CHANCE - 0.01, True),
        ("saturday", WEEKEND_YES_CHANCE + 0.01, False),
    ],
)
def test_decision_follows_the_threshold(
    monkeypatch: MonkeyPatch,
    day: Day,
    roll: float,
    expected: bool,
) -> None:
    monkeypatch.setattr("api.services.random.random", lambda: roll)

    result = decide(DecideQuery(day=day))

    assert result.decision is expected


@pytest.mark.parametrize("day", ALL_DAYS)
def test_explicit_day_is_echoed_back(day: Day) -> None:
    query = DecideQuery(day=day)

    result = decide(query)

    assert result.day == day


@pytest.mark.parametrize(
    ("today", "expected_day"),
    [
        (datetime(2026, 8, 31), "monday"),
        (datetime(2026, 9, 1), "tuesday"),
        (datetime(2026, 9, 2), "wednesday"),
        (datetime(2026, 9, 3), "thursday"),
        (datetime(2026, 9, 4), "friday"),
        (datetime(2026, 9, 5), "saturday"),
        (datetime(2026, 9, 6), "sunday"),
    ],
)
def test_missing_day_falls_back_to_today(
    monkeypatch: MonkeyPatch,
    today: datetime,
    expected_day: Day,
) -> None:
    monkeypatch.setattr(services, "timezone", _frozen_timezone(today))

    result = decide(DecideQuery())

    assert result.day == expected_day


@pytest.mark.parametrize(
    ("today", "expected_decision"),
    [
        (datetime(2026, 9, 4), False),
        (datetime(2026, 8, 31), True),
    ],
)
def test_today_fallback_drives_the_threshold(
    monkeypatch: MonkeyPatch,
    today: datetime,
    expected_decision: bool,
) -> None:
    monkeypatch.setattr(services, "timezone", _frozen_timezone(today))
    monkeypatch.setattr(
        "api.services.random.random",
        lambda: (FRIDAY_YES_CHANCE + NORMAL_YES_CHANCE) / 2,
    )

    result = decide(DecideQuery())

    assert result.decision is expected_decision


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("mood", MOODS)
@pytest.mark.parametrize("day", ALL_DAYS)
def test_message_comes_from_the_matching_bucket(lang: Lang, mood: Mood, day: Day) -> None:
    query = DecideQuery(lang=lang, mood=mood, day=day)
    day_phrases = get_phrases(lang).for_mood(mood).for_kind(_day_kind(day))

    result = decide(query)

    expected = day_phrases.yes if result.decision else day_phrases.no
    assert result.message in expected


@pytest.mark.parametrize("mood", MOODS)
def test_languages_do_not_leak_into_each_other(mood: Mood) -> None:
    random.seed(1)
    en_messages = {
        decide(DecideQuery(lang="en", mood=mood, day="monday")).message for _ in range(50)
    }

    random.seed(1)
    ru_messages = {
        decide(DecideQuery(lang="ru", mood=mood, day="monday")).message for _ in range(50)
    }

    assert not en_messages & ru_messages


@pytest.mark.parametrize("day", ALL_DAYS)
def test_phrase_pool_matches_the_kind_of_day(day: Day) -> None:
    random.seed(7)
    query = DecideQuery(day=day)

    messages = {decide(query).message for _ in range(200)}

    pool = get_phrases("en").chill.for_kind(_day_kind(day))
    assert messages <= set(pool.yes) | set(pool.no)


def test_response_shape_is_stable() -> None:
    query = DecideQuery(lang="en", mood="savage", day="tuesday")

    result = decide(query)

    assert isinstance(result.decision, bool)
    assert isinstance(result.day, str)
    assert isinstance(result.message, str) and result.message


def test_query_defaults() -> None:
    query = DecideQuery()

    assert query.lang == "en"
    assert query.mood == "chill"
    assert query.day is None
