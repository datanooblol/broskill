---
name: read-file
description: Use when the user or agent needs to read file contents — a single known file via scripts/read_file.py, or multiple files matched by a pattern/folder (e.g. "all .md files in skills/") via scripts/list_files.py then scripts/read_file.py per match.
tags: [read, load, file]
keywords: [read file, load file, list files]
version: v0.1.0
default: true
status: experiment
---

# Read File

## Instructions

- **Single, exactly-known file** → call `scripts/read_file.py` with the filename or path. It resolves that under the current directory with `Path.rglob`, so a bare filename or partial path works as long as it matches exactly one file.
- **Multiple files / a pattern / "all .md files in a folder"** →
  1. Call `scripts/list_files.py` first with a glob pattern (e.g. `skills/**/*.md`, `*.py`) to see what matches.
  2. Then call `scripts/read_file.py` for each match actually needed — don't dump every match unless the user asked for all of them.
- If `scripts/read_file.py` reports zero or multiple matches, narrow the pattern (use a fuller relative path) or use `scripts/list_files.py` to disambiguate, then retry.

## Error handling

Both scripts raise typed errors from `scripts/errors.py` (all subclass `ReadFileSkillError`) instead of failing silently. On any of them, do not blindly retry with a guess — call `ask_followup_question` (tool) with: what the error said, and what you need from the user to try again correctly. Don't re-invoke the same script with the same arguments.

| Error | Means | Ask the user for |
|---|---|---|
| `InvalidPatternError` | Pattern was empty, or an absolute path was given instead of one relative to the project root | The intended file/folder, described relative to the project |
| `NoMatchError` | Pattern matched nothing | Confirm the file exists / correct the name or location |
| `MultipleMatchError` (lists every match) | Pattern matched more than one file | Which of the listed matches they meant |
| `FileTooLargeError` | File exceeds the 1MB read limit | Whether to read a specific section, or confirm they want the whole (large) file another way |
| `UnreadableFileError` | File isn't valid UTF-8 (likely binary), or a permissions/OS error occurred | Whether this is actually the right file, since it may not be readable text at all |

## Checklist

- [ ] Picked `scripts/read_file.py` for a single known file, `scripts/list_files.py` first for anything ambiguous or plural
- [ ] Pattern passed to `scripts/list_files.py` is specific enough to avoid matching unrelated files
- [ ] Only read the files actually needed, not everything that matched
- [ ] On any script error, asked the user via `ask_followup_question` instead of guessing and retrying blindly
