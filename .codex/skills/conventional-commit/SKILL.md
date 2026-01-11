---
name: conventional-commit
description: Create and run git commits using Conventional Commits. Use when asked to commit changes or standardize commit messages.
compatibility: Codex CLI/IDE with git available. No Python execution.
allowed-tools: Read Grep Glob Bash Git AskUserQuestion
---

# Conventional Commit Assistant

## When to use
Use this skill when the user asks to create a git commit or wants Conventional Commits formatting.

## Workflow
1. **Check repo state**
   - Run `git status -sb` and `git diff --stat`.
   - If no changes, report and stop.
2. **Review changes**
   - Inspect relevant diffs (`git diff`, `git diff --staged`).
   - Identify the primary change intent (feature, fix, docs, etc.).
3. **Confirm staging**
   - If nothing is staged, ask whether to stage all (`git add -A`) or stage selectively.
4. **Compose Conventional Commit**
   - Format: `type(scope): summary` or `type: summary`.
   - Use `!` for breaking changes: `type(scope)!: summary`.
   - Keep summary imperative, <= 50 chars if possible.
   - If needed, add body and footers (e.g., `BREAKING CHANGE: ...`).
5. **User confirmation**
   - Show the proposed message and the exact `git commit` command.
   - Ask for approval before running the commit.
6. **Run commit**
   - Execute `git commit -m "..."` (add additional `-m` for body/footer).

## Type guidance
Use the smallest type that matches intent. Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`, `style`, `revert`.

## Edge cases
- **No commit history**: skip `git log` checks and ask the user for the intended type/scope.
- **Mixed changes**: pick the dominant intent, or split commits after asking.
- **Breaking change**: require `!` and a `BREAKING CHANGE:` footer.

## References
See `references/conventional-commits.md` for the spec summary and examples.
