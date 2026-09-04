import json
from functools import lru_cache
from pathlib import Path

from api.schemas import Lang

PHRASES_DIR = Path(__file__).parent

PHRASES_ANNOTATION = dict[str, dict[str, dict[str, list[str]]]]


@lru_cache
def get_phrases(lang: Lang) -> PHRASES_ANNOTATION:
    path = PHRASES_DIR / f"{lang}.json"

    try:
        phrases: PHRASES_ANNOTATION = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise ValueError(
            f"Language '{lang}' is not supported. Please add a corresponding JSON file in the phrases directory."
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON file for language '{lang}': {e}"
        ) from e

    return phrases
