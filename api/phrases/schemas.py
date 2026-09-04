from typing import assert_never

from pydantic import (
    BaseModel,
    Field,
)

from api.schemas import (
    DayKind,
    Mood,
)


class PhraseSet(BaseModel):
    yes: list[str] = Field(min_length=1, description="List of phrases for a 'yes' decision.")
    no: list[str] = Field(min_length=1, description="List of phrases for a 'no' decision.")


class MoodPhrases(BaseModel):
    normal: PhraseSet = Field(description="Phrases for normal working days.")
    friday: PhraseSet = Field(description="Phrases for Fridays.")
    weekend: PhraseSet = Field(description="Phrases for Saturdays and Sundays.")

    def for_kind(self, kind: DayKind) -> PhraseSet:
        match kind:
            case "normal":
                return self.normal
            case "friday":
                return self.friday
            case "weekend":
                return self.weekend
        assert_never(kind)


class PhrasesFile(BaseModel):
    chill: MoodPhrases = Field(description="Phrases for a chill mood.")
    savage: MoodPhrases = Field(description="Phrases for a savage mood.")

    def for_mood(self, mood: Mood) -> MoodPhrases:
        match mood:
            case "chill":
                return self.chill
            case "savage":
                return self.savage
        assert_never(mood)
