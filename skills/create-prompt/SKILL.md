---
name: create-prompt
description: Use when the user wants help writing or improving a prompt (for an LLM, agent, or skill) — asks clarifying questions about goal, audience, and constraints, then drafts the prompt and checks it against a quality checklist.
tags: [create, prompt]
keywords: [create prompt, build prompt]
version: v0.1.0
default: true
status: experiment
---

# Create Prompt

## Step 1 — Clarify with the user

Ask (skip anything already known):

- What is this prompt for — what task, run against what model/agent, one-off or reusable?
- Who/what is the audience (a model, a person, a downstream system)?
- Required inputs, expected output format, and constraints (length, tone, structure)?
- Any examples of good/bad output, or existing prompts to match the style of?

## Step 2 — Draft

Write the prompt with:

- A clear task statement up front
- Only the context/constraints actually needed
- An explicit output format, if one is expected
- Examples only where they clarify something words alone can't

## Step 3 — Checklist

- [ ] Clarified purpose/audience before drafting
- [ ] States the task unambiguously in the first lines
- [ ] Includes only necessary context — no filler
- [ ] Output format specified if relevant
- [ ] Reviewed for ambiguity a reader/model could misinterpret

## Step 4 — Confirm

Show the draft back to the user and check it matches intent before finalizing.
