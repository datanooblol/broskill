import pytest

from broskill.processing.path import find_root, strip_path


# --- strip_path ---

@pytest.mark.parametrize(
    "raw,expected",
    [
        ("*/references/*", "references"),
        ("/scripts/", "scripts"),
        ("**/assets/**", "assets"),
        ("plain", "plain"),
        ("", ""),
    ],
)
def test_strip_path_strips_leading_and_trailing_stars_and_slashes(raw, expected):
    assert strip_path(raw) == expected


# --- find_root ---

def test_find_root_finds_marker_in_start_dir(tmp_path):
    (tmp_path / "skills").mkdir()
    assert find_root(start=tmp_path) == tmp_path


def test_find_root_finds_marker_in_an_ancestor(tmp_path):
    (tmp_path / "skills").mkdir()
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    assert find_root(start=nested) == tmp_path


def test_find_root_raises_when_marker_not_found(tmp_path):
    isolated = tmp_path / "no-marker-anywhere-near-here"
    isolated.mkdir()
    with pytest.raises(ValueError):
        find_root(start=isolated, marker="a-marker-that-should-never-exist-xyz123")


def test_find_root_supports_a_custom_marker(tmp_path):
    (tmp_path / "custom-marker").mkdir()
    assert find_root(start=tmp_path, marker="custom-marker") == tmp_path
