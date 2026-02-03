# agent-skills

Codex向けのSkillsと、Claude Code向けのプラグイン/スラッシュコマンドをまとめたリポジトリです。

## Plugins

| Plugin | Description |
|--------|-------------|
| **dig** | 計画段階での曖昧性を構造化された質問で明確化 |
| **frontend-design** | フロントエンドデザイン支援 |
| **mermaid-state-diagram** | Mermaid状態図の作成支援 |
| **skill-creator** | 新しいスキル/プラグインの作成支援 |
| **browser-history** | Arcブラウザの履歴を取得してMarkdown形式で出力 |
| **commit-summary** | Gitコミットを日付ごとに集計してMarkdownテーブルで出力 |
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

### マーケットプレイスから追加

```bash
# マーケットプレイスを追加
/plugin marketplace add iemong/agent-skills

# 個別のプラグインをインストール
/plugin install dig@iemong/agent-skills
/plugin install slack@iemong/agent-skills
```

### 直接インストール

```bash
/install-plugin iemong/agent-skills
```

### `npx skills add` でSkillsをインストール（Codex向け）

```bash
# iemong のスキル集を追加
npx skills add iemong/agent-skills
```

## License

MIT License - see [LICENSE](LICENSE) for details.
