import pytest

from broskill.processing.skill import SkillControl


def write_skill(root, name, frontmatter, body="# Body\n\nSome instructions.", extensions=None):
    """Create a skill directory under `root` with a SKILL.md and optional extension files.

    Args:
        root: Skills directory (a tmp_path-based Path).
        name: Skill directory name.
        frontmatter: Dict of frontmatter fields, or a raw YAML string to allow malformed cases.
        body: Markdown body text.
        extensions: Optional dict of {relative_path: content} written under the skill dir,
            e.g. {"references/api.md": "..."}.
    """
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(frontmatter, str):
        yaml_block = frontmatter
    else:
        lines = []
        for k, v in frontmatter.items():
            if isinstance(v, list):
                items = ", ".join(v)
                lines.append(f"{k}: [{items}]")
            elif isinstance(v, bool):
                lines.append(f"{k}: {str(v).lower()}")
            else:
                lines.append(f"{k}: {v}")
        yaml_block = "\n".join(lines)

    text = f"---\n{yaml_block}\n---\n\n{body}"
    (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")

    for rel_path, content in (extensions or {}).items():
        target = skill_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return skill_dir


@pytest.fixture
def skills_root(tmp_path):
    root = tmp_path / "skills"
    root.mkdir()
    return root


def minimal_frontmatter(**overrides):
    fm = {"name": "sample", "description": "a sample skill", "version": "v0.1.0"}
    fm.update(overrides)
    return fm


# --- get_root ---

def test_get_root_defaults_to_self_root(skills_root):
    sc = SkillControl(root=skills_root)
    assert sc.get_root(None) == skills_root


def test_get_root_uses_explicit_root(skills_root, tmp_path):
    sc = SkillControl(root=skills_root)
    other = tmp_path / "other"
    assert sc.get_root(other) == other


# --- get_skill_path ---

def test_get_skill_path_none_when_not_loaded(skills_root):
    sc = SkillControl(root=skills_root)
    assert sc.get_skill_path("read-file") is None


def test_get_skill_path_after_load(skills_root):
    skill_dir = write_skill(skills_root, "read-file", minimal_frontmatter(name="read-file"))
    sc = SkillControl(root=skills_root)
    sc.load_skill("read-file")
    assert sc.get_skill_path("read-file") == skill_dir


# --- load_skill ---

def test_load_skill_returns_body_and_registers_skill(skills_root):
    write_skill(
        skills_root, "read-file",
        minimal_frontmatter(name="read-file", description="reads files"),
        body="# Read File\n\nDo the thing.",
    )
    sc = SkillControl(root=skills_root)
    body = sc.load_skill("read-file")

    assert body == "# Read File\n\nDo the thing."
    assert "read-file" in sc.skills
    skill = sc.skills["read-file"]
    assert skill.name == "read-file"
    assert skill.description == "reads files"
    assert skill.version == "v0.1.0"
    assert skill.path == skills_root / "read-file"


def test_load_skill_returns_none_when_not_found(skills_root):
    sc = SkillControl(root=skills_root)
    assert sc.load_skill("does-not-exist") is None
    assert sc.skills == {}


def test_load_skill_raises_when_match_is_a_file_not_a_directory(skills_root):
    (skills_root / "read-file").write_text("not a directory", encoding="utf-8")
    sc = SkillControl(root=skills_root)
    with pytest.raises(ValueError):
        sc.load_skill("read-file")


def test_load_skill_raises_when_skill_md_missing(skills_root):
    (skills_root / "read-file").mkdir()
    sc = SkillControl(root=skills_root)
    with pytest.raises(FileNotFoundError):
        sc.load_skill("read-file")


def test_load_skill_raises_on_missing_required_field(skills_root):
    fm = {"name": "read-file", "description": "reads files"}  # no version
    write_skill(skills_root, "read-file", fm)
    sc = SkillControl(root=skills_root)
    with pytest.raises(ValueError):
        sc.load_skill("read-file")


def test_load_skill_raises_on_unknown_frontmatter_field(skills_root):
    fm = minimal_frontmatter(name="read-file", bogus_field="nope")
    write_skill(skills_root, "read-file", fm)
    sc = SkillControl(root=skills_root)
    with pytest.raises(ValueError):
        sc.load_skill("read-file")


def test_load_skill_parses_optional_fields(skills_root):
    fm = minimal_frontmatter(
        name="read-file",
        tags=["read", "file"],
        keywords=["load file"],
        default=True,
        status="stable",
    )
    write_skill(skills_root, "read-file", fm)
    sc = SkillControl(root=skills_root)
    sc.load_skill("read-file")
    skill = sc.skills["read-file"]

    assert skill.tags == ["read", "file"]
    assert skill.keywords == ["load file"]
    assert skill.default is True
    assert skill.status == "stable"


def test_load_skill_handles_utf8_body(skills_root):
    write_skill(
        skills_root, "read-file", minimal_frontmatter(name="read-file"),
        body="Step 1 → Step 2",
    )
    sc = SkillControl(root=skills_root)
    body = sc.load_skill("read-file")
    assert body == "Step 1 → Step 2"


# --- list_skills ---

def test_list_skills_raises_when_root_missing(tmp_path):
    sc = SkillControl(root=tmp_path / "does-not-exist")
    with pytest.raises(FileNotFoundError):
        sc.list_skills()


def test_list_skills_loads_every_skill_and_populates_cache(skills_root):
    write_skill(skills_root, "read-file", minimal_frontmatter(name="read-file"))
    write_skill(skills_root, "create-skill", minimal_frontmatter(name="create-skill"))
    sc = SkillControl(root=skills_root)

    skills = sc.list_skills()

    assert {s.name for s in skills} == {"read-file", "create-skill"}
    assert set(sc.skills.keys()) == {"read-file", "create-skill"}


def test_list_skills_uses_explicit_root_override(tmp_path):
    other_root = tmp_path / "other-skills"
    other_root.mkdir()
    write_skill(other_root, "read-file", minimal_frontmatter(name="read-file"))
    sc = SkillControl(root=tmp_path / "unused")

    skills = sc.list_skills(root=other_root)

    assert [s.name for s in skills] == ["read-file"]


# --- load_skill_extension ---

def test_load_skill_extension_raises_when_skill_not_loaded(skills_root):
    sc = SkillControl(root=skills_root)
    with pytest.raises(ValueError):
        sc.load_skill_extension("read-file", "references/script.md")


def test_load_skill_extension_returns_none_when_missing(skills_root):
    write_skill(skills_root, "read-file", minimal_frontmatter(name="read-file"))
    sc = SkillControl(root=skills_root)
    sc.load_skill("read-file")
    assert sc.load_skill_extension("read-file", "references/does-not-exist.md") is None


def test_load_skill_extension_returns_content(skills_root):
    write_skill(
        skills_root, "read-file", minimal_frontmatter(name="read-file"),
        extensions={"scripts/read_file.py": "print('hello')"},
    )
    sc = SkillControl(root=skills_root)
    sc.load_skill("read-file")
    content = sc.load_skill_extension("read-file", "scripts/read_file.py")
    assert content == "print('hello')"


def test_load_skill_extension_handles_utf8_content(skills_root):
    write_skill(
        skills_root, "read-file", minimal_frontmatter(name="read-file"),
        extensions={"references/note.md": "arrow: →"},
    )
    sc = SkillControl(root=skills_root)
    sc.load_skill("read-file")
    content = sc.load_skill_extension("read-file", "references/note.md")
    assert content == "arrow: →"
