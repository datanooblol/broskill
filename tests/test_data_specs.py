from pathlib import Path

import pytest

from broskill.data_specs.skill import Skill, SkillStatus
from broskill.data_specs.tool import Arg, DTYPE_MAP, Tool


# --- SkillStatus ---

def test_skill_status_values():
    assert SkillStatus.STABLE == "stable"
    assert SkillStatus.EXPERIMENT == "experiment"
    assert SkillStatus.DEPRECATED == "deprecated"


# --- Skill ---

def test_skill_requires_name_description_version_path():
    with pytest.raises(TypeError):
        Skill(name="x", description="y")  # missing version, path


def test_skill_defaults():
    skill = Skill(name="x", description="y", version="v0.1.0", path=Path("skills/x"))
    assert skill.tags is None
    assert skill.keywords is None
    assert skill.default is False
    assert skill.status == SkillStatus.EXPERIMENT


def test_skill_accepts_all_fields():
    skill = Skill(
        name="x", description="y", version="v0.1.0", path=Path("skills/x"),
        tags=["a", "b"], keywords=["c"], default=True, status="stable",
    )
    assert skill.tags == ["a", "b"]
    assert skill.keywords == ["c"]
    assert skill.default is True
    assert skill.status == "stable"


def test_skill_rejects_unknown_field():
    with pytest.raises(TypeError):
        Skill(name="x", description="y", version="v0.1.0", path=Path("skills/x"), bogus="nope")


# --- Arg ---

def test_arg_converts_python_types_to_json_schema():
    assert Arg(name="a", type=str).type == "string"
    assert Arg(name="a", type=int).type == "integer"
    assert Arg(name="a", type=float).type == "number"
    assert Arg(name="a", type=bool).type == "boolean"


def test_arg_passes_through_an_already_string_type():
    assert Arg(name="a", type="string").type == "string"


def test_arg_raises_on_unsupported_type():
    with pytest.raises(ValueError):
        Arg(name="a", type=dict)


def test_arg_defaults():
    arg = Arg(name="a", type=str)
    assert arg.description is None
    assert arg.required is True


def test_dtype_map_covers_the_basic_python_types():
    assert set(DTYPE_MAP.keys()) == {str, int, float, bool}


# --- Tool ---

def test_tool_holds_its_fields():
    args = [Arg(name="path", type=str)]
    tool = Tool(name="read_file", description="reads a file", args=args, path=Path("scripts/read_file.py"))
    assert tool.name == "read_file"
    assert tool.description == "reads a file"
    assert tool.args == args
    assert tool.path == Path("scripts/read_file.py")
