# Script practices

Consult this file before writing any script into a skill's `scripts/` folder.

- One script, one purpose. Don't build a multi-command CLI when a task-specific script will do.
- Prefer the project's existing language/tooling (this repo is Python, managed with `uv`) unless the task clearly calls for shell.
- No unnecessary error handling — trust inputs the skill controls, validate only what comes from outside the skill (user-provided paths, external data).
- No hardcoded absolute paths; take paths as arguments or derive them relative to the script.
- Keep a one-line usage comment at the top only if invocation isn't obvious from the filename/args.
- Idempotent where possible — safe to re-run without side effects piling up.
- Update this file when a new convention is established, so future scripts stay consistent.
