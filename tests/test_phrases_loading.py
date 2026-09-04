import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from api.phrases import loader
from api.phrases.loader import PHRASES_DIR, get_phrases
from api.phrases.schemas import PhrasesFile
from api.schemas import Lang

SUPPORTED_LANGS: list[Lang] = ["en", "ru"]
MOODS = ["chill", "savage"]
DAY_KINDS = ["normal", "friday"]
DECISIONS = ["yes", "no"]


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_loads_supported_language(lang: Lang) -> None:
    phrases = get_phrases(lang)

    assert isinstance(phrases, PhrasesFile)


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
@pytest.mark.parametrize("mood", MOODS)
@pytest.mark.parametrize("day_kind", DAY_KINDS)
@pytest.mark.parametrize("decision", DECISIONS)
def test_every_bucket_is_non_empty(lang: Lang, mood: str, day_kind: str, decision: str) -> None:
    phrases = get_phrases(lang)

    bucket = getattr(getattr(getattr(phrases, mood), day_kind), decision)

    assert bucket, f"{lang}.{mood}.{day_kind}.{decision} is empty"
    assert all(isinstance(p, str) and p.strip() for p in bucket)


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_data_file_exists_for_each_supported_lang(lang: Lang) -> None:
    path = PHRASES_DIR / f"{lang}.json"

    exists = path.is_file()

    assert exists


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_result_is_cached_between_calls(lang: Lang) -> None:
    first = get_phrases(lang)

    second = get_phrases(lang)

    assert first is second


def test_languages_share_the_same_structure() -> None:
    en, ru = get_phrases("en"), get_phrases("ru")

    en_dump, ru_dump = en.model_dump(), ru.model_dump()

    assert en_dump.keys() == ru_dump.keys()
    for mood in MOODS:
        assert en_dump[mood].keys() == ru_dump[mood].keys()


def test_unknown_language_raises_value_error(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(loader, "PHRASES_DIR", tmp_path)

    with pytest.raises(ValueError, match="is not supported"):
        get_phrases("de")


def test_malformed_json_raises_value_error(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    (tmp_path / "en.json").write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(loader, "PHRASES_DIR", tmp_path)

    with pytest.raises(ValueError, match="Failed to parse JSON"):
        get_phrases("en")


def test_json_missing_required_section_raises_validation_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    payload = json.loads((PHRASES_DIR / "en.json").read_text(encoding="utf-8"))
    payload.pop("savage")
    (tmp_path / "en.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(loader, "PHRASES_DIR", tmp_path)

    with pytest.raises(ValidationError):
        get_phrases("en")


def test_empty_phrase_list_raises_validation_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    payload = json.loads((PHRASES_DIR / "en.json").read_text(encoding="utf-8"))
    payload["chill"]["normal"]["yes"] = []
    (tmp_path / "en.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(loader, "PHRASES_DIR", tmp_path)

    with pytest.raises(ValidationError):
        get_phrases("en")
