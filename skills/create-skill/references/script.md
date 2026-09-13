# Script practices

Consult this file before writing any script into a skill's `scripts/` folder.

## Required: `get_args()` for tool-schema loading

Every script must define a module-level `get_args()` that returns an `argparse.ArgumentParser` — `ToolControl.load_tool(skill_name, path)` (in `broskill.processing.tool`) imports the script and calls `get_args()` to auto-generate its `Tool`/`Arg` schema. Without it, `load_tool` raises `ValueError`.

- `parser.description` becomes the tool's description — write it for whoever/whatever decides when to call the tool, not just as a docstring.
- Each `add_argument` becomes an `Arg`: `dest` → name, `help` → description, `required` → required.
- `type=` must be one of the types in `DTYPE_MAP` (`str`, `int`, `float`, `bool`) — anything else raises `ValueError` when the tool is loaded.
- Don't reference `--flag` syntax in SKILL.md instructions; scripts are invoked as tools with named params (e.g. `path=...`), not raw CLI.

```python
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument('--path', type=str, required=True, help="...")
    return parser

def main():
    args = get_args().parse_args()
    ...

if __name__ == '__main__':
    main()
```

## General

- One script, one purpose. Don't build a multi-command CLI when a task-specific script will do.
- Prefer the project's existing language/tooling (this repo is Python, managed with `uv`) unless the task clearly calls for shell.
- No unnecessary error handling — trust inputs the skill controls, validate only what comes from outside the skill (user-provided paths, external data).
- No hardcoded absolute paths; take paths as arguments or derive them relative to the script.
- Keep a one-line usage comment at the top only if invocation isn't obvious from the filename/args.
- Idempotent where possible — safe to re-run without side effects piling up.
- Update this file when a new convention is established, so future scripts stay consistent.
