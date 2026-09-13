---
name: create-skill
description: Use when the user wants to create a new Claude Code skill — asks clarifying questions about the skill's purpose and trigger conditions, then writes a SKILL.md with instructions and a checklist, progressively loading references/reference.md, references/script.md, or references/asset.md only when the new skill actually needs that kind of file.
tags: [create, skill]
keywords: [create skill, build skill]
version: v0.1.0
status: experiment
default: false
---

# Create Skill

Helps build a new skill under `skills/<skill-name>/SKILL.md`.

## Step 1 — Clarify with the user

Before writing anything, ask (skip anything already answered):

- What should trigger this skill? (user phrasing, task type)
- What is the skill supposed to produce or do, end to end?
- Any existing skill, doc, or example it should follow the style of?
- Does it need to run scripts, provide reference detail, or use static assets — or is plain instructions enough?
- Is the scope small enough for one file, or does it have several large sub-topics?

## Step 2 — Decide what the new skill needs

Default is SKILL.md only — most skills fit here. Add a file type below only when the skill actually needs it, and always load its practice file first, before writing into that folder:

| The new skill needs... | Load practice from | Then write content to |
|---|---|---|
| Detail too long/detailed for SKILL.md itself | `references/reference.md` | `references/<topic>.md` |
| To execute code | `references/script.md` | `scripts/<name>.py` |
| Static templates/examples/fixtures to copy or show | `references/asset.md` | `assets/<name>.<ext>` |

Never write into `references/`, `scripts/`, or `assets/` without first loading the matching practice file above — each one holds conventions specific to that file type.

## Step 3 — Write SKILL.md

Frontmatter must match the `Skill` dataclass in `src/broskill/data_specs/skill.py` field-for-field — `SkillControl.load_skill` parses it as `Skill(**metadata, path=...)`, so an extra, missing (required), or misnamed key will fail to load:

```yaml
---
name: <kebab-case, matches folder name>                        # required
description: <what it does + when to trigger it>               # required
version: v0.1.0                                                # required — vMajor.Minor.Patch
tags: [tag-one, tag-two]                                        # optional — for search/filtering
keywords: [phrase one, phrase two]                              # optional — for search/filtering
default: false                                                  # optional — true if this skill must always load/display
status: experiment                                               # optional — stable | experiment | deprecated
---
```

Do not add a `path` key — it's supplied automatically from the skill's folder, not read from frontmatter. Do not add any key not on `Skill`.

Body:

- A short instructions section (what to do, in order)
- Every `references/<name>.md`, `scripts/<name>.py`, or `assets/<name>.<ext>` added must be explicitly named in SKILL.md's text, with the condition under which it's loaded — this is what makes progressive loading work. A file only discoverable by listing the directory is a bug.
- A checklist the model runs through before finishing, e.g.:
  - [ ] Clarified ambiguous requirements with the user
  - [ ] Frontmatter `name` matches the folder name
  - [ ] Description states both what the skill does and when to trigger it
  - [ ] No unnecessary references/scripts/assets added
  - [ ] Every references/scripts/assets file is named and linked from SKILL.md, with a clear load condition
  - [ ] Any scripts followed `references/script.md`; any references followed `references/reference.md`; any assets followed `references/asset.md`

## Step 4 — Verify

- Re-read the description as if deciding whether to trigger it — is it specific enough not to fire on unrelated tasks?
- Confirm every `references/*.md`, `scripts/*.py`, and `assets/*.*` file is referenced from SKILL.md's own text.
- Confirm each followed its practice file (`references/reference.md`, `references/script.md`, `references/asset.md` respectively).
