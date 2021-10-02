from server.settings import Settings
from pytest import MonkeyPatch
import pytest


@pytest.fixture
def monkeypatch() -> MonkeyPatch:
    return MonkeyPatch()


def test_generator_interval_in_seconds(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("GENERATOR_INTERVAL_IN_SECONDS", "1.5")

    modified_settings = Settings()

    assert modified_settings.generator_interval_in_seconds == 1.5


def test_generator_interval_in_seconds_has_default() -> None:
    modified_settings = Settings()

    assert isinstance(modified_settings.generator_interval_in_seconds, float)
