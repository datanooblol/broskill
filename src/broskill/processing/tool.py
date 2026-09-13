import importlib.util
from typing import Any

from broskill.data_specs.tool import Arg, Tool
from broskill.processing.skill import SkillControl


def to_args(args: dict) -> list[Any]:
    """Convert a dict of tool arguments into a CLI argument list.

    Args:
        args (dict): Argument names mapped to their values, e.g. `{"path": "a.md"}`.

    Returns:
        list[Any]: A flat `--name value` list suitable for `subprocess.run`,
            e.g. `["--path", "a.md"]`. Empty list if `args` is falsy.
    """
    if not args:
        return []
    args_list = []
    for k, v in args.items():
        args_list.extend([f"--{k}", v])
    return args_list


class ToolControl:
    """Loads a skill's `scripts/*.py` files as callable `Tool` schemas.

    Composes with a `SkillControl` for skill_name -> directory resolution,
    so both classes share one source of truth for where a skill lives.
    Every script must define a module-level `get_args()` returning an
    `argparse.ArgumentParser` (see `skills/create-skill/references/script.md`);
    that parser is introspected to build the `Tool`/`Arg` schema.

    Attributes:
        skills (SkillControl): Used to resolve a skill name to its directory.
        tools (dict[str, Tool]): Tools loaded so far, keyed by `"skill_name:path"`.
    """

    def __init__(self, skills: SkillControl):
        """Initialize the controller.

        Args:
            skills (SkillControl): The skill controller to resolve skill
                directories through.
        """
        self.skills = skills
        self.tools: dict[str, Tool] = {}

    def load_tool(self, skill_name: str, path: str) -> Tool:
        """Load a skill's script as a `Tool` schema, caching the result.

        Args:
            skill_name (str): Name of the skill, as registered by `self.skills.load_skill`.
            path (str): Path to the script, relative to the skill's directory
                (e.g. `scripts/read_file.py`).

        Returns:
            Tool: The tool schema built from the script's `get_args()` parser.

        Raises:
            ValueError: If `skill_name` isn't loaded, the file can't be loaded
                as a Python module, it has no `get_args()`, or one of its
                arguments uses a type `Arg` doesn't recognize (see `DTYPE_MAP`
                in `broskill.data_specs.tool`).
            FileNotFoundError: If `path` doesn't exist under the skill's directory.
        """
        skill_path = self.skills.get_skill_path(skill_name)
        if skill_path is None:
            raise ValueError(f"Skill '{skill_name}' is not loaded — call load_skill first")

        cache_key = f"{skill_name}:{path}"
        if cache_key in self.tools:
            return self.tools[cache_key]

        script_path = skill_path / path
        if not script_path.is_file():
            raise FileNotFoundError(f"Script not found: {script_path}")

        spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load '{script_path}' as a Python module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "get_args"):
            raise ValueError(f"'{script_path}' must define a get_args() function")
        parser = module.get_args()

        args = []
        for action in parser._actions:
            if action.dest == "help":
                continue
            try:
                args.append(
                    Arg(
                        name=action.dest,
                        type=action.type,
                        description=action.help,
                        required=action.required,
                    )
                )
            except ValueError as e:
                raise ValueError(f"{e} (in '{script_path}')") from e

        tool = Tool(name=script_path.stem, description=parser.description, args=args, path=script_path)
        self.tools[cache_key] = tool
        return tool
