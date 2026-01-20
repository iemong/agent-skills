# claude-code

A collection of personal Claude Code plugins and custom slash commands.

## Plugins

| Plugin | Description |
|--------|-------------|
| **dig** | 計画段階での曖昧性を構造化された質問で明確化 |
| **frontend-design** | フロントエンドデザイン支援 |
| **mermaid-state-diagram** | Mermaid状態図の作成支援 |
| **skill-creator** | 新しいスキル/プラグインの作成支援 |
| **browser-history** | Arcブラウザの履歴を取得してMarkdown形式で出力 |
| **commit-summary** | 日報用にGitコミットを日付ごとに集計してMarkdownテーブルで出力 |
| **slack** | Slack Web APIを操作してメッセージ投稿・取得、検索を実行 |

## Structure

```
plugins/
├── dig/                      # 曖昧性明確化プラグイン
├── frontend-design/          # フロントエンドデザイン
├── mermaid-state-diagram/    # Mermaid状態図
├── skill-creator/            # スキル作成ツール
├── browser-history/          # Arcブラウザ履歴取得
├── commit-summary/           # Gitコミット集計
└── slack/                    # Slack API操作
```

## Installation

Claude Code内で以下のコマンドを実行：

```
/install-plugin iemong/claude-code
```

## License

MIT License - see [LICENSE](LICENSE) for details.
