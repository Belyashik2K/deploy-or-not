from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)

Lang = Literal["en", "ru"]
Day = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
Mood = Literal["chill", "savage"]
DayKind = Literal["normal", "friday", "weekend"]


class DecideQuery(BaseModel):
    lang: Lang = Field(
        default="en", description="Language for the response message. Default is 'en'."
    )
    day: Day | None = Field(
        default=None,
        description=(
            "Day of the week for the decision. "
            "Default is None, which means the current day will be used."
        ),
    )
    mood: Mood = Field(
        default="chill", description="Mood for the response message. Default is 'chill'."
    )


class DecideResponse(BaseModel):
    decision: bool = Field(description="Decision deploy or not deploy.")
    day: str = Field(description="Day of the week for the decision.")
    message: str = Field(description="Response message based on the decision.")
