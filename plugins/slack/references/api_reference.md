# Slack API Reference

> Based on https://docs.slack.dev/reference/

## Web API Methods

### Method Families

| Family | Description |
|--------|-------------|
| `chat` | メッセージ送受信 |
| `conversations` | チャンネル・DM管理 |
| `users` | ユーザー情報管理 |
| `files` | ファイル操作 |
| `reactions` | リアクション管理 |
| `pins` | ピン留め機能 |
| `search` | メッセージ検索 |
| `views` | モーダル・ホームタブ |
| `workflows` | ワークフロー自動化 |
| `team` | ワークスペース情報 |
| `usergroups` | ユーザーグループ |
| `reminders` | リマインダー |
| `bookmarks` | ブックマーク管理 |
| `assistant` | AIアシスタント機能 |

---

### chat.postMessage

メッセージを投稿。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID (C1234567890) |
| text | Conditional | メッセージテキスト（blocksがない場合は必須） |
| blocks | No | Block Kit形式のリッチコンテンツ (JSON配列) |
| thread_ts | No | スレッドの親メッセージのタイムスタンプ |
| reply_broadcast | No | スレッド返信をチャンネルにも表示 |
| unfurl_links | No | URLプレビューを展開 (default: false) |
| unfurl_media | No | メディアプレビューを展開 (default: true) |
| metadata | No | メッセージメタデータ |
| mrkdwn | No | mrkdwn形式を有効化 (default: true) |

**Required Scope:** `chat:write`

---

### chat.update

既存メッセージを更新。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| ts | Yes | 更新対象メッセージのタイムスタンプ |
| text | Conditional | 新しいテキスト |
| blocks | No | 新しいBlock Kit |

**Required Scope:** `chat:write`

---

### chat.delete

メッセージを削除。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| ts | Yes | 削除対象メッセージのタイムスタンプ |

**Required Scope:** `chat:write`

---

### conversations.history

チャンネルのメッセージ履歴を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| limit | No | 取得件数 (default: 100, max: 1000) |
| oldest | No | 開始タイムスタンプ (exclusive) |
| latest | No | 終了タイムスタンプ (exclusive) |
| inclusive | No | oldest/latestを含める (default: false) |
| cursor | No | ページネーションカーソル |
| include_all_metadata | No | メタデータを含める |

**Required Scope:** `channels:history`, `groups:history`, `mpim:history`, `im:history`

---

### conversations.replies

スレッドの返信を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| ts | Yes | 親メッセージのタイムスタンプ |
| limit | No | 取得件数 (default: 10, max: 1000) |
| oldest | No | 開始タイムスタンプ |
| latest | No | 終了タイムスタンプ |
| cursor | No | ページネーションカーソル |
| inclusive | No | 親メッセージを含める (default: false) |

**Required Scope:** `channels:history`, `groups:history`, `mpim:history`, `im:history`

---

### conversations.list

チャンネル一覧を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| types | No | チャンネルタイプ (public_channel, private_channel, mpim, im) |
| limit | No | 取得件数 (default: 100, max: 1000) |
| cursor | No | ページネーションカーソル |
| exclude_archived | No | アーカイブ済みを除外 (default: false) |

**Required Scope:** `channels:read`, `groups:read`, `mpim:read`, `im:read`

---

### conversations.info

チャンネル情報を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| include_num_members | No | メンバー数を含める |
| include_locale | No | ロケール情報を含める |

**Required Scope:** `channels:read`, `groups:read`, `mpim:read`, `im:read`

---

### search.messages

メッセージを検索。**User tokenが必須。**

| Parameter | Required | Description |
|-----------|----------|-------------|
| query | Yes | 検索クエリ |
| count | No | 結果件数 (default: 20, max: 100) |
| page | No | ページ番号 |
| sort | No | ソート順 (score / timestamp) |
| sort_dir | No | ソート方向 (asc / desc) |
| highlight | No | マッチ部分をハイライト |

**Required Scope:** `search:read` (User token only)

#### Search Query Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| `from:` | `from:@username` | 特定ユーザーの投稿 |
| `in:` | `in:#channel` | 特定チャンネル内 |
| `to:` | `to:@me` | 自分宛てのDM |
| `has:` | `has:link`, `has:emoji`, `has:pin` | 特定要素を含む |
| `is:` | `is:thread`, `is:saved` | 特定状態 |
| `before:` | `before:2024-01-01` | 指定日より前 |
| `after:` | `after:2024-01-01` | 指定日より後 |
| `on:` | `on:2024-01-15` | 指定日 |
| `during:` | `during:january` | 指定期間 |

---

### users.info

ユーザー情報を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| user | Yes | ユーザーID (U1234567890) |
| include_locale | No | ロケール情報を含める |

**Required Scope:** `users:read`

---

### users.list

ユーザー一覧を取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| limit | No | 取得件数 (max: 1000) |
| cursor | No | ページネーションカーソル |
| include_locale | No | ロケール情報を含める |

**Required Scope:** `users:read`

---

### reactions.add

リアクションを追加。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| timestamp | Yes | メッセージのタイムスタンプ |
| name | Yes | 絵文字名 (コロンなし、例: thumbsup) |

**Required Scope:** `reactions:write`

---

### reactions.get

メッセージのリアクションを取得。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | Yes | チャンネルID |
| timestamp | Yes | メッセージのタイムスタンプ |
| full | No | 全リアクション詳細を取得 |

**Required Scope:** `reactions:read`

---

### files.upload (v2)

ファイルをアップロード。v2 APIを推奨。

| Parameter | Required | Description |
|-----------|----------|-------------|
| channel | No | 共有先チャンネルID |
| content | Conditional | ファイル内容 (file未指定時) |
| file | Conditional | ファイルパス (content未指定時) |
| filename | No | ファイル名 |
| filetype | No | ファイルタイプ |
| initial_comment | No | 添付コメント |
| title | No | ファイルタイトル |
| thread_ts | No | スレッドに投稿 |

**Required Scope:** `files:write`

---

### views.open

モーダルを開く。

| Parameter | Required | Description |
|-----------|----------|-------------|
| trigger_id | Yes | インタラクションから取得したトリガーID |
| view | Yes | モーダルビューのJSON |

**Required Scope:** `(trigger_id経由のため不要)`

---

### views.update

モーダルを更新。

| Parameter | Required | Description |
|-----------|----------|-------------|
| view_id | Conditional | ビューID (external_id未指定時) |
| external_id | Conditional | 外部ID (view_id未指定時) |
| view | Yes | 更新後のビューJSON |
| hash | No | 競合検出用ハッシュ |

---

## Events API

### Connection Methods

| Method | Description |
|--------|-------------|
| Socket Mode | WebSocket接続、ファイアウォール内対応 |
| HTTP Request URL | イベントをHTTP POSTで受信 |

### Core Events

| Event | Description |
|-------|-------------|
| `message` | メッセージ投稿・編集・削除 |
| `app_mention` | アプリへのメンション |
| `app_home_opened` | ホームタブを開いた |
| `reaction_added` | リアクション追加 |
| `reaction_removed` | リアクション削除 |
| `member_joined_channel` | メンバーがチャンネル参加 |
| `member_left_channel` | メンバーがチャンネル退出 |
| `channel_created` | チャンネル作成 |
| `channel_renamed` | チャンネル名変更 |
| `channel_deleted` | チャンネル削除 |
| `channel_archive` | チャンネルアーカイブ |
| `user_change` | ユーザー情報変更 |
| `team_join` | 新メンバー参加 |
| `file_shared` | ファイル共有 |
| `pin_added` | ピン追加 |
| `pin_removed` | ピン削除 |
| `message_metadata_posted` | メタデータ付きメッセージ投稿 |
| `workflow_step_execute` | ワークフローステップ実行 |

### Message Subtypes

| Subtype | Description |
|---------|-------------|
| `bot_message` | Botからのメッセージ |
| `me_message` | /me コマンド |
| `message_changed` | メッセージ編集 |
| `message_deleted` | メッセージ削除 |
| `thread_broadcast` | スレッド返信のブロードキャスト |
| `file_share` | ファイル共有メッセージ |
| `channel_join` | チャンネル参加通知 |
| `channel_leave` | チャンネル退出通知 |

---

## Scopes

### Bot Token Scopes (Primary)

| Scope | Description |
|-------|-------------|
| `chat:write` | メッセージ送信 |
| `chat:write.public` | 未参加の公開チャンネルに投稿 |
| `channels:read` | 公開チャンネル情報取得 |
| `channels:history` | 公開チャンネル履歴取得 |
| `channels:join` | 公開チャンネルに参加 |
| `groups:read` | プライベートチャンネル情報取得 |
| `groups:history` | プライベートチャンネル履歴取得 |
| `im:read` | DM情報取得 |
| `im:history` | DM履歴取得 |
| `im:write` | DM開始 |
| `mpim:read` | グループDM情報取得 |
| `mpim:history` | グループDM履歴取得 |
| `users:read` | ユーザー情報取得 |
| `users:read.email` | ユーザーのメールアドレス取得 |
| `reactions:read` | リアクション取得 |
| `reactions:write` | リアクション追加 |
| `files:read` | ファイル情報取得 |
| `files:write` | ファイルアップロード |
| `pins:read` | ピン取得 |
| `pins:write` | ピン追加・削除 |
| `bookmarks:read` | ブックマーク取得 |
| `bookmarks:write` | ブックマーク追加・削除 |
| `app_mentions:read` | アプリメンションイベント受信 |

### User Token Scopes

| Scope | Description |
|-------|-------------|
| `search:read` | メッセージ・ファイル検索 |
| `identify` | ユーザー識別 |

---

## Block Kit

→ 詳細は [block_kit.md](./block_kit.md) を参照

---

## ID Formats

| Type | Format | Example |
|------|--------|---------|
| User | `U` + 10 chars | U0123456789 |
| Bot User | `U` + 10 chars | U0123456789 |
| Channel (public) | `C` + 10 chars | C0123456789 |
| Channel (private) | `G` + 10 chars | G0123456789 |
| DM | `D` + 10 chars | D0123456789 |
| App | `A` + 10 chars | A0123456789 |
| Team/Workspace | `T` + 10 chars | T0123456789 |
| Enterprise | `E` + 10 chars | E0123456789 |
| File | `F` + 10 chars | F0123456789 |
| Message ts | Unix timestamp | 1234567890.123456 |

---

## Rate Limits

| Tier | Rate | Description |
|------|------|-------------|
| Tier 1 | 1 req/min | 制限の厳しいメソッド |
| Tier 2 | 20 req/min | 標準メソッド |
| Tier 3 | 50 req/min | 頻繁な呼び出し向け |
| Tier 4 | 100 req/min | 高頻度向け |
| Special | varies | chat.postMessage等は別ルール |

**chat.postMessage:** 1メッセージ/秒/チャンネル (バースト許容あり)

---

## Error Codes

| Code | Description |
|------|-------------|
| `channel_not_found` | チャンネルが存在しない |
| `not_in_channel` | Botがチャンネルに未参加 |
| `is_archived` | チャンネルがアーカイブ済み |
| `msg_too_long` | メッセージが長すぎる (40,000文字制限) |
| `no_text` | テキストもblocksも指定されていない |
| `invalid_auth` | トークンが無効 |
| `token_revoked` | トークンが取り消された |
| `missing_scope` | 必要なスコープがない |
| `account_inactive` | ユーザーアカウントが無効 |
| `user_not_found` | ユーザーが存在しない |
| `invalid_cursor` | ページネーションカーソルが無効 |
| `ratelimited` | レート制限に到達 |
| `request_timeout` | リクエストタイムアウト |
| `service_unavailable` | Slackサービス一時停止 |
| `team_added_to_org` | Enterprise Grid移行中 |
| `accesslimited` | アクセス制限中 |
| `fatal_error` | サーバー内部エラー |

---

## HTTP Response Structure

```json
{
  "ok": true,
  "channel": "C1234567890",
  "ts": "1234567890.123456",
  "message": {
    "type": "message",
    "subtype": "bot_message",
    "text": "Hello",
    "ts": "1234567890.123456",
    "username": "bot",
    "bot_id": "B1234567890"
  }
}
```

### Error Response

```json
{
  "ok": false,
  "error": "channel_not_found"
}
```

### Paginated Response

```json
{
  "ok": true,
  "messages": [...],
  "has_more": true,
  "response_metadata": {
    "next_cursor": "dXNlcjpVMDYxTkZUVDI="
  }
}
```

---

## References

**Internal:**
- [Authentication & Scopes](./authentication.md) - トークン作成・スコープ設定
- [Block Kit](./block_kit.md) - UIコンポーネント詳細

**External:**
- [Web API Methods](https://docs.slack.dev/reference/methods)
- [Events API](https://docs.slack.dev/reference/events)
- [Scopes](https://docs.slack.dev/reference/scopes)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Slack API Apps](https://api.slack.com/apps)
