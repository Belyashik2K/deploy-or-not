import random
from typing import (
    Final,
)

from django.utils import timezone

from .phrases.loader import (
    get_phrases,
)
from .schemas import (
    DayKind,
    DecideQuery,
    DecideResponse,
)

FRIDAY_YES_CHANCE: Final[float] = 0.2
NORMAL_YES_CHANCE: Final[float] = 0.85
WEEKEND_YES_CHANCE: Final[float] = 0.1

WEEKEND_DAYS: Final[frozenset[str]] = frozenset({"saturday", "sunday"})
YES_CHANCE: Final[dict[DayKind, float]] = {
    "normal": NORMAL_YES_CHANCE,
    "friday": FRIDAY_YES_CHANCE,
    "weekend": WEEKEND_YES_CHANCE,
}


def _day_kind(day: str) -> DayKind:
    if day == "friday":
        return "friday"
    if day in WEEKEND_DAYS:
        return "weekend"
    return "normal"


def decide(query: DecideQuery) -> DecideResponse:
    resolved_day: str = (query.day or timezone.localtime().strftime("%A")).lower()
    kind = _day_kind(resolved_day)

    decision = random.random() < YES_CHANCE[kind]

    day_phrases = get_phrases(query.lang).for_mood(query.mood).for_kind(kind)
    phrases = day_phrases.yes if decision else day_phrases.no

    return DecideResponse(
        decision=decision,
        day=resolved_day,
        message=random.choice(phrases),
    )
