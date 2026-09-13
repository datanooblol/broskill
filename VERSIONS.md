# VERSIONS

Changelog for broskill. Newest first.

## v0.1.1

Patch — packaging metadata, no code changes.

- Real `description` in `pyproject.toml` (was the uv-generated placeholder).
- `authors`, `license = "MIT"`, and `[project.urls]` (`Repository`, `Changelog`) added.
- `broskill.__version__` added alongside the package's top-level exports.

## v0.1.0

First real drop. This is where broskill stopped being a notebook full of scratch code and became an actual lib.

- **`SkillControl`** — discovers skills under a `skills/` dir, loads a skill's `SKILL.md` (frontmatter → `Skill`, body returned to you), and reads any `references/`, `scripts/`, or `assets/` file a skill points to. Caches what it loads so you're not re-walking the filesystem every call.
- **`ToolControl`** — turns a skill's `scripts/*.py` into a callable `Tool` schema by reading its `get_args()` (yep, plain `argparse`). Composes with `SkillControl` instead of re-solving "where's this skill" itself. Caches too.
- **`Skill` / `Tool` / `Arg`** — the dataclasses everything above hands you back. Fields carry their own `description` in `metadata`, so the schema is self-documenting.
- **`processing.path`** — `find_root()` (walk up 'til you hit a `skills/` folder, git-style) and `strip_path()` (clean up glob-y path fragments).
- Real error handling everywhere that matters — no bare `raise`, no silent `IndexError`s. Every failure mode tells you what to do next.
- Full test suite (`tests/`) covering all of the above.
- Two runnable examples: [`examples/case1.py`](examples/case1.py) (SkillControl) and [`examples/case2.py`](examples/case2.py) (ToolControl).

See [README.md](README.md) for the how/why.
