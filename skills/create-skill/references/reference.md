# Reference practices

Consult this file before adding a `references/*.md` file to a skill.

- Only add one when content would make SKILL.md itself too long/detailed if inlined — this is for progressive disclosure, not padding. If SKILL.md still reads fine as one file, don't split it.
- One file per sub-topic, named for that topic — `references/api.md`, `references/style.md` — not a `references/misc.md` grab-bag.
- SKILL.md must explicitly link every reference file as `references/<name>.md` and say when to load it. A reference file the agent could only find by listing the directory is a bug — it must always be reachable from SKILL.md's own text.
- Put in a reference only what's needed sometimes — deep detail, edge cases, examples. Core, always-needed instructions stay in SKILL.md.
- Write each reference to stand on its own when loaded later, without depending on context that only existed earlier in the conversation.
- When guidance on a sub-topic changes, update that `references/<name>.md` file, don't grow SKILL.md instead.
