# Slack認証ガイド

## 環境変数

| 環境変数 | 用途 | 必須 |
|----------|------|------|
| `CLAUDE_SLACK_TOKEN` | Slack Token（xoxp-またはxoxb-） | Yes |

検索機能を使用する場合はUser Token（xoxp-）を設定する。

## 必要なスコープ

| コマンド | 必要なスコープ |
|----------|----------------|
| `post_message` | `chat:write` |
| `dm_me` | `chat:write`, `im:write` |
| `get_history` | `channels:history`, `groups:history`, `im:history`, `mpim:history` |
| `get_thread` | `channels:history`, `groups:history`, `im:history`, `mpim:history` |
| `search` | `search:read` |
| `get_user` | `users:read` |

## 推奨スコープ

```
chat:write
im:write
channels:history
groups:history
im:history
mpim:history
users:read
search:read
```

## トークン取得手順

1. https://api.slack.com/apps でアプリ作成
2. 「OAuth & Permissions」→「Scopes」でUser Token Scopesを追加
3. 「Install to Workspace」でインストール
4. 「User OAuth Token」をコピー
5. 環境変数に設定: `export CLAUDE_SLACK_TOKEN=xoxp-...`

## 注意事項

- プライベートチャンネルへのアクセスには適切なスコープが必要
