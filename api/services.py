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

    day_type = "friday" if is_friday else "normal"
    outcome = "yes" if decision else "no"
    phrases = get_phrases(query.lang)[query.mood][day_type][outcome]

    return DecideResponse(
        decision=decision,
        day=resolved_day,
        message=random.choice(phrases),
    )
