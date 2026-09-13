import re
from pathlib import Path

import yaml

from broskill.data_specs.skill import Skill


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a SKILL.md file's text into its frontmatter and body.

    Args:
        text (str): Raw file contents, expected to start with a `---`
            delimited YAML block followed by the markdown body.

    Returns:
        tuple[dict, str]: The parsed frontmatter as a dict, and the
            remaining body text with surrounding whitespace stripped.

    Raises:
        ValueError: If no `---` delimited frontmatter block is found.
    """
    match = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.DOTALL)
    if not match:
        raise ValueError('No frontmatter block found')
    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    return metadata, body

class SkillControl:
    """Discovers, loads, and reads skills from a skills directory.

    `root` is the skills directory itself (e.g. `project_root / "skills"`),
    not the project root — every method searches directly under `root`,
    with no implicit `"skills"` subfolder appended.

    Skills loaded via `load_skill`/`list_skills` are cached on `self.skills`
    (keyed by skill name), so later calls that only need a skill's path
    (`load_skill_extension`) don't need to search the filesystem again.

    Attributes:
        root (Path): Default skills directory (e.g. `project_root / "skills"`),
            not the project root.
        skills (dict[str, Skill]): Skills loaded so far, keyed by name.
    """

    def __init__(self, root:Path):
        """Initialize the controller.

        Args:
            root (Path): Default skills directory (e.g. `project_root / "skills"`),
                not the project root.
        """
        self.root:Path = root
        self.skills:dict[str, Skill] = {}

    def get_skill_path(self, skill_name:str)->Path | None:
        """Get a previously loaded skill's directory path.

        Args:
            skill_name (str): Name of the skill, as registered by `load_skill`.

        Returns:
            Path | None: The skill's directory, or None if it hasn't been
                loaded yet (call `load_skill` first).
        """
        skill = self.skills.get(skill_name, None)
        if skill:
            return skill.path
        return None

    def get_root(self, root:Path|None)->Path|None:
        """Resolve the skills directory to use for a call.

        Args:
            root (Path | None): An explicit skills directory to use, or None
                to fall back to `self.root`.

        Returns:
            Path | None: `root` if given, otherwise `self.root`.
        """
        if root is None:
            return self.root
        return root

    def list_skills(self, root:Path|None=None)->list[Skill]|list:
        """List and load every skill under the skills directory.

        Args:
            root (Path | None): Skills directory to search. Defaults to `self.root`.

        Returns:
            list[Skill]: Every skill discovered by scanning `root` for
                `SKILL.md` files.

        Raises:
            FileNotFoundError: If `root` doesn't exist.
        """
        root = self.get_root(root)
        if not root.exists():
            raise FileNotFoundError(f"Skills directory not found: {root}")
        skills = list(root.rglob("SKILL.md"))
        _ = [self.load_skill(s.parent.name, root) for s in skills]
        return list(self.skills.values())

    def load_skill(self, skill_name:str, root:Path|None=None)->str|None:
        """Load a skill by name and register it into `self.skills`.

        Args:
            skill_name (str): Name of the skill's directory under the skills directory.
            root (Path | None): Skills directory to search. Defaults to `self.root`.

        Returns:
            Skill | None: The loaded skill, or None if no directory named
                `skill_name` exists under `root`.

        Raises:
            ValueError: If a path named `skill_name` exists but none of the
                matches is a valid skill directory, or if its `SKILL.md`
                frontmatter doesn't match the `Skill` dataclass fields.
            FileNotFoundError: If the matched directory has no `SKILL.md`.
        """
        root = self.get_root(root)
        skills = list(root.rglob(skill_name))
        if len(skills) == 0:
            return None
        candidates = [s for s in skills if s.is_dir() and s.exists()]
        if not candidates:
            raise ValueError(f"No skill directory found for '{skill_name}' under {root}")
        skill = candidates[0]
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            raise FileNotFoundError(f"'{skill_md}' not found for skill '{skill_name}'")
        text = skill_md.read_text(encoding='utf-8')
        metadata, body = split_frontmatter(text)
        try:
            _skill = Skill(**metadata, path=skill)
        except TypeError as e:
            raise ValueError(f"'{skill_md}' frontmatter doesn't match the Skill schema: {e}") from e
        self.skills[skill_name] = _skill
        return body

    def load_skill_extension(self, skill_name:str, path:str, root:Path|None=None)->str|None:
        """Load any skill artifact under its `references/`, `scripts/`, or `assets/` folder.

        Args:
            skill_name (str): Name of the skill, as registered by `load_skill`.
            path (str): Path to the artifact, relative to the skill's directory
                (e.g. `references/script.md`, `scripts/read_file.py`).
            root (Path | None): Project root, currently unused directly (the
                skill's own registered path is used) but accepted for a
                consistent signature with the other loaders.

        Returns:
            str | None: The artifact's text content, or None if `path` doesn't
                exist under the skill's directory.

        Raises:
            ValueError: If `skill_name` hasn't been loaded yet — call
                `load_skill` first.
        """
        root = self.get_root(root)
        skill_path = self.get_skill_path(skill_name)
        if skill_path is None:
            raise ValueError(f"Skill '{skill_name}' is not loaded — call load_skill first")
        target = skill_path / path
        if target.is_file():
            return target.read_text(encoding='utf-8')
        return None
