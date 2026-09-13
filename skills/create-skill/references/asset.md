# Asset practices

Consult this file before adding an `assets/*.*` file to a skill.

- `assets/` holds static, non-code, non-instruction files the skill's output is built from or shows: templates, boilerplate, example/fixture files, images, schemas. Things copied or filled in or displayed — not executed (`scripts/`) and not read as guidance (`references/`).
- Name each file for what it is, with its real extension — `assets/template.md`, `assets/logo.png`, `assets/config.schema.json` — since the loader keys off the literal `assets/<name>.<ext>` path.
- SKILL.md must explicitly name every asset and say when to use it. An asset the agent has to discover by listing the directory is a bug.
- Keep it minimal — only the asset(s) the skill actually needs to produce its output, not multiple variants bundled "just in case."
