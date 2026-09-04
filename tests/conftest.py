from collections.abc import Iterator

import pytest
from pytest_django import Settings

from api.phrases.loader import get_phrases


@pytest.fixture(autouse=True)
def _no_ssl_redirect(settings: Settings) -> None:
    """The API is plain HTTP in tests; SECURE_SSL_REDIRECT would 301 every request."""
    settings.SECURE_SSL_REDIRECT = False


@pytest.fixture(autouse=True)
def _clear_phrases_cache() -> Iterator[None]:
    get_phrases.cache_clear()
    yield
    get_phrases.cache_clear()
