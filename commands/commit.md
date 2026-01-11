---
description: "Conventional Commits に従ってコミットを作成する"
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

このコマンドは `agents/commit.md` のサブエージェント手順に従って、差分の確認から Conventional Commits 形式のメッセージ作成、`git commit` 実行まで行う。

実行手順:
1. `agents/commit.md` の手順に従う。
2. ユーザー承認後に `git commit` を実行する。
