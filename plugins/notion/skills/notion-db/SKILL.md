---
name: notion-db
description: |
  Notion APIを使ってデータベース/データソースから複数ページを取得し、ページ更新もできるスキル。
  使用タイミング: (1) Notion DBを条件付きで取得したい (2) 一括取得したい (3) DB itemのプロパティを更新したい (4) ページのコンテンツをMarkdownで取得したい
  トリガーキーワード: Notion、データベース取得、Notion API、filter、query database、update page、get markdown、ページ内容取得
allowed-tools: Bash(python3:*) Read
---

# Notion DB Skill

Notion APIの`query database`/`query data source`でページを複数件取得し、`update page`でitem更新、`get markdown`でページコンテンツをMarkdown取得する。

## 認証

| 環境変数 | 用途 |
|----------|------|
| `CLAUDE_NOTION_TOKEN` | Notion Integration Token |
| `NOTION_VERSION` | 任意。未指定時は `2022-06-28` |

## 使用方法

### 取得（既存挙動）

### 基本（最大50件取得）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py \
  --database-id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --max-items 50
```

### 最新API（Data Source）を使う場合

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py \
  --data-source-id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --max-items 50
```

### フィルター指定（JSON文字列）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py \
  --database-id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --filter '{"property":"Status","status":{"equals":"Done"}}' \
  --max-items 100
```

### フィルター指定（JSONファイル）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py \
  --database-id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --filter-file ./filter.json \
  --sorts-file ./sorts.json
```

### 途中カーソルから再開

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py \
  --database-id "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --start-cursor "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 更新（itemのプロパティ更新）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py update-page \
  --page-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  --properties '{"Status":{"status":{"name":"In progress"}}}'
```

### 更新（JSONファイルで更新）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py update-page \
  --page-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  --properties-file ./properties.json
```

### Markdown取得（ページコンテンツをMarkdownで取得）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py get-markdown \
  --page-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Markdown取得（会議ノートのトランスクリプト込み）

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/notion-db/scripts/notion_db.py get-markdown \
  --page-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  --include-transcript
```

> **注意**: `get-markdown` は Notion API `2025-09-03` を自動的に使用します（`--notion-version` の指定は不要）。

## 出力

JSONを標準出力する。主なキー:

- `action`: `query` または `update-page`
- `count`: 取得件数
- `has_more`: 続きがあるか
- `next_cursor`: 次ページ取得に使うカーソル
- `target_type`: `database` または `data-source`
- `target_id`: クエリ対象ID
- `results`: Notionページ配列
- `page`: 更新後ページ（`update-page` の場合）
- `markdown`: ページコンテンツのMarkdown文字列（`get-markdown` の場合）
- `truncated`: コンテンツが切り詰められたか（`get-markdown` の場合）
- `unknown_block_ids`: 未知ブロックID配列（`get-markdown` の場合）

`--compact` を使うと `id/url/created_time/last_edited_time/properties` のみを返す。

## 参考

- 公式（Database）: https://developers.notion.com/reference/post-database-query
- 公式（Data Source）: https://developers.notion.com/reference/query-a-data-source
- 公式（Update Page）: https://developers.notion.com/reference/patch-page
- 公式（Retrieve Page Markdown）: https://developers.notion.com/reference/retrieve-page-markdown
- フィルター例: [references/filter_examples.md](references/filter_examples.md)
- 更新例: [references/update_examples.md](references/update_examples.md)
