"""Проверки canonical semantic StatePath."""

from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from mindra.contracts import StatePath


def test_state_path_has_canonical_dotted_representation() -> None:
    path = StatePath(("synthetic", "source", "value"))

    assert path.segments == ("synthetic", "source", "value")
    assert path.dotted == "synthetic.source.value"
    assert str(path) == "synthetic.source.value"
    assert StatePath.from_dotted(path.dotted) == path


@pytest.mark.parametrize(
    "segments",
    [
        (),
        ("",),
        ("Synthetic",),
        ("synthetic-source",),
        ("synthetic.source",),
        ("1synthetic",),
        ("synthetic", ""),
    ],
)
def test_state_path_rejects_invalid_or_empty_segments(segments: tuple[str, ...]) -> None:
    with pytest.raises(ValueError):
        StatePath(segments)


def test_state_path_rejects_mutable_or_non_string_segments() -> None:
    with pytest.raises(TypeError):
        StatePath(cast(tuple[str, ...], ["synthetic", "value"]))

    with pytest.raises(TypeError):
        StatePath(cast(tuple[str, ...], ("synthetic", 1)))


def test_state_path_is_frozen() -> None:
    path = StatePath(("synthetic", "value"))
    segments_attribute = "segments"

    with pytest.raises(FrozenInstanceError):
        setattr(path, segments_attribute, ("synthetic", "other"))
