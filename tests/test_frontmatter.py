import pytest

from broskill.processing.skill import split_frontmatter


def test_split_frontmatter_parses_metadata_and_body():
    text = "---\nname: sample\nversion: v0.1.0\n---\n\n# Body\n\nSome text."
    metadata, body = split_frontmatter(text)
    assert metadata == {"name": "sample", "version": "v0.1.0"}
    assert body == "# Body\n\nSome text."


def test_split_frontmatter_strips_surrounding_whitespace_from_body():
    text = "---\nname: sample\n---\n\n\n  # Body  \n\n\n"
    _, body = split_frontmatter(text)
    assert body == "# Body"


def test_split_frontmatter_handles_empty_frontmatter_block():
    text = "---\n\n---\nbody text"
    metadata, body = split_frontmatter(text)
    assert metadata == {}
    assert body == "body text"


def test_split_frontmatter_raises_without_a_frontmatter_block():
    with pytest.raises(ValueError):
        split_frontmatter("just a plain markdown file, no frontmatter here")
