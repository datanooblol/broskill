# broskill

yo. **broskill** is a lightweight, quick-loading skill loader for agentic projects — a "skill" being a folder with instructions (`SKILL.md`) plus optional reference docs, python scripts as tools, and static assets. broskill's whole job is finding those folders, loading them, and turning their scripts into callable tools. That's it. That's the lib.

part of the **bro lib family** — small, opinionated, do-one-thing tools built to stop us from writing the same glue code every time we spin up a new agentic project.

## why this exists

every time you start a new agent project you end up rebuilding the same boring plumbing: some way to discover "skills," some way to load their instructions, some way to turn a script into a tool the model can call. broskill is that plumbing, ripped out of real projects where we got tired of writing it again and again.

**heads up:** this is an opinionated lib. it works one way — SKILL.md + `references/` + `scripts/` + `assets/`, discovered off a `skills/` folder. if that convention fits your project, great, you just saved yourself a bunch of setup. if it doesn't, this probably isn't your lib, and that's fine — go build your own, that's basically how broskill got made in the first place. inspired by real work and real struggle. voilà, here it is.

## install

```bash
uv pip install -e .
```

## the shape of a skill

```
skills/
  read-file/
    SKILL.md              # frontmatter (name, description, version, ...) + instructions
    references/
      script.md            # optional deep-dive docs, loaded on demand
    scripts/
      read_file.py          # a get_args()-based python script -> becomes a callable tool
    assets/
      template.md            # optional static files a skill hands out
```

`SKILL.md`'s frontmatter has to match the [`Skill`](src/broskill/data_specs/skill.py) dataclass field-for-field (`name`, `description`, `version` required; `tags`, `keywords`, `default`, `status` optional). Want to build one from scratch? There's a skill for that: [`skills/create-skill`](skills/create-skill/SKILL.md).

## quick start

### load skills — `SkillControl`

```python
from broskill.processing.path import find_root
from broskill.processing.skill import SkillControl

root = find_root()  # walks up 'til it finds a skills/ folder
sc = SkillControl(root=root / "skills")

for skill in sc.list_skills():
    print(skill.name, "-", skill.description)

body = sc.load_skill("read-file")          # -> SKILL.md's instructions, as a str
ref = sc.load_skill_extension("read-file", "references/script.md")
```

Full runnable version: [`examples/case1.py`](examples/case1.py).

### turn a script into a tool — `ToolControl`

```python
from broskill.processing.skill import SkillControl
from broskill.processing.tool import ToolControl, to_args
import subprocess, sys

sc = SkillControl(root=root / "skills")
sc.load_skill("read-file")

tc = ToolControl(sc)
tool = tc.load_tool("read-file", "scripts/list_files.py")
# tool.name, tool.description, tool.args -> ready to hand to an LLM's tool schema

result = subprocess.run(
    [sys.executable, str(tool.path), *to_args({"path": "skills/**/*.md"})],
    capture_output=True, text=True,
)
```

A script only needs one thing to become a tool: a module-level `get_args()` returning an `argparse.ArgumentParser`. broskill reads that parser and builds the schema for you — no separate tool-definition file to keep in sync. See [`skills/create-skill/references/script.md`](skills/create-skill/references/script.md) for the full contract.

Full runnable version: [`examples/case2.py`](examples/case2.py).

## running the tests

```bash
uv run pytest
uv run ruff check
```

## more

- [`VERSIONS.md`](VERSIONS.md) — changelog
- [`LICENSE`](LICENSE) — MIT
- [`skills/create-skill`](skills/create-skill/SKILL.md) — a skill that helps you build more skills
- [`skills/read-file`](skills/read-file/SKILL.md) — the skill used in both examples above, a decent reference for what a real skill looks like

stay chill, ship skills. 🤙
