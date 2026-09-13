import pytest

from broskill.processing.skill import SkillControl
from broskill.processing.tool import ToolControl, to_args


def write_skill(root, name, frontmatter=None):
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    fm = frontmatter or {"name": name, "description": "a sample skill", "version": "v0.1.0"}
    lines = "\n".join(f"{k}: {v}" for k, v in fm.items())
    (skill_dir / "SKILL.md").write_text(f"---\n{lines}\n---\n\n# Body", encoding="utf-8")
    return skill_dir


def write_script(skill_dir, rel_path, content):
    target = skill_dir / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


VALID_SCRIPT = """\
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Reads a thing")
    parser.add_argument('--path', type=str, required=True, help="a path")
    parser.add_argument('--limit', type=int, required=False, help="a limit")
    return parser

def main():
    pass

if __name__ == '__main__':
    main()
"""

NO_GET_ARGS_SCRIPT = "def main():\n    pass\n"

UNSUPPORTED_TYPE_SCRIPT = """\
import argparse
import json

def get_args():
    parser = argparse.ArgumentParser(description="bad type")
    parser.add_argument('--data', type=json.loads, required=True, help="a blob")
    return parser
"""


@pytest.fixture
def skills_root(tmp_path):
    root = tmp_path / "skills"
    root.mkdir()
    return root


@pytest.fixture
def loaded(skills_root):
    skill_dir = write_skill(skills_root, "sample")
    sc = SkillControl(root=skills_root)
    sc.load_skill("sample")
    return sc, ToolControl(sc), skill_dir


def test_load_tool_builds_schema_from_get_args(loaded):
    sc, tc, skill_dir = loaded
    write_script(skill_dir, "scripts/do_thing.py", VALID_SCRIPT)

    tool = tc.load_tool("sample", "scripts/do_thing.py")

    assert tool.name == "do_thing"
    assert tool.description == "Reads a thing"
    assert tool.path == skill_dir / "scripts" / "do_thing.py"
    by_name = {a.name: a for a in tool.args}
    assert by_name["path"].type == "string"
    assert by_name["path"].required is True
    assert by_name["path"].description == "a path"
    assert by_name["limit"].type == "integer"
    assert by_name["limit"].required is False


def test_load_tool_caches_by_skill_and_path(loaded):
    sc, tc, skill_dir = loaded
    write_script(skill_dir, "scripts/do_thing.py", VALID_SCRIPT)

    first = tc.load_tool("sample", "scripts/do_thing.py")
    second = tc.load_tool("sample", "scripts/do_thing.py")

    assert first is second
    assert tc.tools["sample:scripts/do_thing.py"] is first


def test_load_tool_raises_when_skill_not_loaded(skills_root):
    sc = SkillControl(root=skills_root)
    tc = ToolControl(sc)
    with pytest.raises(ValueError):
        tc.load_tool("sample", "scripts/do_thing.py")


def test_load_tool_raises_when_script_missing(loaded):
    sc, tc, skill_dir = loaded
    with pytest.raises(FileNotFoundError):
        tc.load_tool("sample", "scripts/does_not_exist.py")


def test_load_tool_raises_when_get_args_missing(loaded):
    sc, tc, skill_dir = loaded
    write_script(skill_dir, "scripts/broken.py", NO_GET_ARGS_SCRIPT)
    with pytest.raises(ValueError):
        tc.load_tool("sample", "scripts/broken.py")


def test_load_tool_raises_on_unsupported_arg_type(loaded):
    sc, tc, skill_dir = loaded
    write_script(skill_dir, "scripts/bad_type.py", UNSUPPORTED_TYPE_SCRIPT)
    with pytest.raises(ValueError):
        tc.load_tool("sample", "scripts/bad_type.py")


# --- to_args ---

def test_to_args_empty_dict_returns_empty_list():
    assert to_args({}) == []


def test_to_args_converts_dict_to_flag_list():
    assert to_args({"path": "a.md", "limit": 5}) == ["--path", "a.md", "--limit", 5]
