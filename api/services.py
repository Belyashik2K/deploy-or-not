import random
from datetime import datetime
from typing import (
    Final,
)

from .phrases.loader import (
    get_phrases,
)
from .schemas import (
    DecideQuery,
    DecideResponse,
)

FRIDAY_YES_CHANCE: Final[float] = 0.2
NORMAL_YES_CHANCE: Final[float] = 0.85


def decide(query: DecideQuery) -> DecideResponse:
    resolved_day: str = (query.day or datetime.now().strftime("%A")).lower()
    is_friday = resolved_day == "friday"

    yes_chance = FRIDAY_YES_CHANCE if is_friday else NORMAL_YES_CHANCE
    decision = random.random() < yes_chance

    phrases_file = get_phrases(query.lang)
    mood_phrases = getattr(phrases_file, query.mood)
    day_phrases = mood_phrases.friday if is_friday else mood_phrases.normal
    phrases = day_phrases.yes if decision else day_phrases.no

    return DecideResponse(
        decision=decision,
        day=resolved_day,
        message=random.choice(phrases),
    )
