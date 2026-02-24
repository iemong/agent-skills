---
name: notion-db
description: |
  Notion APIを使ってデータベース/データソースから複数ページを取得するスキル。filter/sorts/start_cursorを指定して絞り込み取得できる。
  使用タイミング: (1) Notion DBを条件付きで取得したい (2) 一括取得したい (3) APIベースで再利用可能な取得処理が必要
  トリガーキーワード: Notion、データベース取得、Notion API、filter、query database
allowed-tools: Bash(python3:*) Read
---

# Notion DB Query Skill

Notion APIの`query database`/`query data source`でページを複数件取得する。

## 認証

| 環境変数 | 用途 |
|----------|------|
| `CLAUDE_NOTION_TOKEN` | Notion Integration Token |
| `NOTION_VERSION` | 任意。未指定時は `2022-06-28` |

## 使用方法

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

## 出力

JSONを標準出力する。主なキー:

- `count`: 取得件数
- `has_more`: 続きがあるか
- `next_cursor`: 次ページ取得に使うカーソル
- `target_type`: `database` または `data-source`
- `target_id`: クエリ対象ID
- `results`: Notionページ配列

`--compact` を使うと `id/url/created_time/last_edited_time/properties` のみを返す。

## 参考

- 公式（Database）: https://developers.notion.com/reference/post-database-query
- 公式（Data Source）: https://developers.notion.com/reference/query-a-data-source
- フィルター例: [references/filter_examples.md](references/filter_examples.md)
