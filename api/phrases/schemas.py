from pydantic import (
    BaseModel,
    Field,
)


class PhraseSet(BaseModel):
    yes: list[str] = Field(
        min_length=1,
        description="List of phrases for a 'yes' decision."
    )
    no: list[str] = Field(
        min_length=1,
        description="List of phrases for a 'no' decision."
    )


class MoodPhrases(BaseModel):
    normal: PhraseSet = Field(
        description="Phrases for normal days."
    )
    friday: PhraseSet = Field(
        description="Phrases for Fridays."
    )


class PhrasesFile(BaseModel):
    chill: MoodPhrases = Field(
        description="Phrases for a chill mood."
    )
    savage: MoodPhrases = Field(
        description="Phrases for a savage mood."
    )
