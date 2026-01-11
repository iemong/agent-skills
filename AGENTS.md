# Repository Guidelines

## Project Structure & Module Organization
- `plugins/` holds all installed plugins/skills. Each plugin lives in its own folder (e.g., `plugins/frontend-design`).
- Plugin documentation lives in `SKILL.md` or `README.md`. Command definitions, when present, live under `commands/` (e.g., `plugins/dig/commands/dig.md`).
- Supporting materials (templates, references, scripts) are stored inside the plugin folder (e.g., `plugins/skill-creator/references/`).

## Build, Test, and Development Commands
- There is no global build or test runner for this repository.
- For plugin maintenance, run scripts inside the plugin when needed. Example:
  - `python3 plugins/skill-creator/scripts/quick_validate.py` — validates skill metadata and structure.
  - `python3 plugins/skill-creator/scripts/package_skill.py` — packages a skill for distribution.
- For content changes, a Markdown preview in your editor is typically sufficient.

## Coding Style & Naming Conventions
- Keep documentation concise and task-focused; favor short paragraphs and bullet lists.
- Use Markdown headings (`#`, `##`) to structure skill docs.
- Name plugin folders in lowercase kebab-case (e.g., `frontend-design`).
- Command files should match the command name: `commands/<command>.md`.

## Testing Guidelines
- No automated tests are present. Validate changes by:
  - running any plugin-provided scripts,
  - checking Markdown rendering,
  - verifying relative links and file paths.

## Commit & Pull Request Guidelines
- This repository currently has no commit history, so no established convention exists.
- Use clear, imperative commit messages (e.g., “Add dig plugin” or “Update skill-creator references”).
- PRs should include a brief description, affected plugin path(s), and example usage or commands when applicable.

## Security & Configuration Tips
- Avoid committing secrets in plugin docs or scripts.
- Keep external URLs minimal and prefer stable documentation links.
