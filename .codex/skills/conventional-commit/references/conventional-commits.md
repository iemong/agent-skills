# Conventional Commits v1.0.0 (summary)

Source: https://www.conventionalcommits.org/ja/v1.0.0/

## Core format
- `type(scope): summary`
- `scope` is optional. Use short nouns (e.g., `plugins`, `agents`).
- Summary should be imperative and concise.

## Common types
- `feat`: a new feature
- `fix`: a bug fix
- Other common types: `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`, `style`, `revert`

## Breaking changes
- Add `!` after type or scope: `feat!: ...` or `feat(core)!: ...`
- Or include a footer: `BREAKING CHANGE: ...`

## Examples
- `feat(agents): add commit sub-agent`
- `fix: handle empty git status`
- `docs: document plugin layout`
- `refactor!: remove legacy command`
