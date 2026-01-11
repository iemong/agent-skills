---
description: "Agent Skills の SKILL.md を検証する (skills-ref 推奨)"
version: "1.0.0"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Git
  - AskUserQuestion
context: fork
---

このコマンドは `agents/validate-skill.md` の手順に従い、Agent Skills の検証を行う。

実行手順:
1. 対象のスキルディレクトリを確認する。
2. 可能なら `skills-ref validate <path>` を使う。
3. `skills-ref` が無い場合は、インストールするか `scripts/validate-skill.sh <path>` で代替するかを確認する（スクリプトは skills-ref があれば自動利用）。
4. 結果を簡潔に報告する。
