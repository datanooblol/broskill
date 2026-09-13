---
name: create-skill
description: Use when the user wants to create a new Claude Code skill — asks clarifying questions about the skill's purpose and trigger conditions, then writes a SKILL.md with instructions and a checklist, adding references/*.md for progressive loading or scripts/ (after consulting references/script.md) only when needed.
---

# Create Skill

Helps build a new skill under `skills/<skill-name>/SKILL.md`.

## Step 1 — Clarify with the user

Before writing anything, ask (skip anything already answered):
- What should trigger this skill? (user phrasing, task type)
- What is the skill supposed to produce or do, end to end?
- Any existing skill, doc, or example it should follow the style of?
- Does it need to run scripts, or just give instructions?
- Is the scope small enough for one file, or does it have several large sub-topics?

## Step 2 — Decide the shape

- **SKILL.md only** — default. Most skills fit here.
- **+ `references/*.md`** — only when instructions are too long/detailed for one file. Split by sub-topic (e.g. `references/api.md`, `references/style.md`). SKILL.md should point to these files and describe when to load each one, not inline their content.
- **+ `scripts/`** — only when the skill needs to execute code, not just guide the model. Before writing a script:
  1. Read `references/script.md` for this project's scripting conventions.
  2. Follow those conventions when writing the script.
  3. If a new convention gets established, add it to `references/script.md`.

## Step 3 — Write SKILL.md

Frontmatter:
```yaml
---
name: <kebab-case, matches folder name>
description: <one line: what it does + when to trigger it, written for a model deciding whether to invoke it>
---
```

Body:
- A short instructions section (what to do, in order)
- A checklist the model runs through before finishing, e.g.:
  - [ ] Clarified ambiguous requirements with the user
  - [ ] Frontmatter `name` matches the folder name
  - [ ] Description states both what the skill does and when to trigger it
  - [ ] No unnecessary references/scripts added
  - [ ] Any references are actually linked from SKILL.md
  - [ ] Any scripts followed `references/script.md`

## Step 4 — Verify

- Re-read the description as if deciding whether to trigger it — is it specific enough not to fire on unrelated tasks?
- Confirm every `references/*.md` file is referenced from SKILL.md.
- Confirm any scripts followed `references/script.md`.
