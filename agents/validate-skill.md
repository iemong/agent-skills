---
name: validate-skill
description: Validate Agent Skills directories using skills-ref or the local validator script.
version: "1.0.0"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Git
  - AskUserQuestion
---

# Skill Validation Sub-Agent

## Goal
Validate a skill directory against the Agent Skills spec. Prefer the official reference validator when available, otherwise use the local shell validator.

## Preferred path (official)
1. Check if `skills-ref` is available (`command -v skills-ref`).
2. If present and user approves, run:
   - `skills-ref validate <skill-dir>`
3. Report errors verbatim.

## If skills-ref is missing
Ask the user whether to install the skills-ref reference library or to proceed with the local validator.

## Fallback path (skills-ref unavailable)
Use `scripts/validate-skill.sh <skill-dir>` for a conservative check. The script will use `skills-ref` automatically if it is on `PATH`.

## What to check
- `SKILL.md` exists and has YAML frontmatter.
- Required fields: `name`, `description`.
- Allowed fields only: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`.
- Name rules: lowercase, no leading/trailing hyphen, no consecutive hyphens, directory name matches, <= 64 chars.
- Description length <= 1024 chars; compatibility <= 500 chars.

## Output
- Summarize pass/fail per skill path.
- If fallback validator is used, note its limitations (ASCII-only name check; no multiline YAML).
