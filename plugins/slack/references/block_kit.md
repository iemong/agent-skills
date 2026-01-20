# Block Kit Reference

> Based on https://docs.slack.dev/reference/block-kit

Block Kitは視覚的にリッチでインタラクティブなメッセージを構築するためのUIフレームワーク。

## Block Types

| Block | Description |
|-------|-------------|
| `section` | テキストとアクセサリー |
| `divider` | 水平区切り線 |
| `header` | 大きな太字テキスト |
| `context` | 小さな補足テキスト・画像 |
| `image` | 画像表示 |
| `actions` | インタラクティブ要素の配置 |
| `input` | フォーム入力（モーダル用） |
| `rich_text` | リッチテキスト |
| `video` | 動画埋め込み |
| `file` | ファイル表示 |
| `table` | テーブル表示 |

**制限:** メッセージは最大50ブロック、モーダル/ホームタブは最大100ブロック

---

## Block Details

### Section Block

最も汎用的なブロック。テキストとオプショナルなアクセサリーを表示。

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Title*\nDescription text"
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "Click" },
    "action_id": "button_click"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"section"` |
| text | Conditional | テキストオブジェクト (max 3000 chars) |
| block_id | No | ブロック識別子 (max 255 chars) |
| fields | No | テキストオブジェクトの配列 (max 10, 各2000 chars) |
| accessory | No | 右側に配置する要素 |

### Header Block

大きな太字のプレーンテキストを表示。

```json
{
  "type": "header",
  "text": {
    "type": "plain_text",
    "text": "Header Text"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"header"` |
| text | Yes | plain_textオブジェクト (max 150 chars) |
| block_id | No | ブロック識別子 |

### Divider Block

水平線で視覚的に区切る。

```json
{
  "type": "divider"
}
```

### Context Block

補足情報を小さなテキスト/画像で表示。

```json
{
  "type": "context",
  "elements": [
    {
      "type": "image",
      "image_url": "https://example.com/icon.png",
      "alt_text": "icon"
    },
    {
      "type": "mrkdwn",
      "text": "Additional context"
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"context"` |
| elements | Yes | image/textオブジェクトの配列 (max 10) |
| block_id | No | ブロック識別子 |

### Image Block

画像を表示。

```json
{
  "type": "image",
  "image_url": "https://example.com/image.png",
  "alt_text": "Description",
  "title": {
    "type": "plain_text",
    "text": "Image Title"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"image"` |
| image_url | Yes | 画像URL (max 3000 chars) |
| alt_text | Yes | 代替テキスト (max 2000 chars) |
| title | No | タイトル (max 2000 chars) |
| block_id | No | ブロック識別子 |

### Actions Block

インタラクティブ要素を横に並べる。

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Approve" },
      "style": "primary",
      "action_id": "approve"
    },
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Reject" },
      "style": "danger",
      "action_id": "reject"
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"actions"` |
| elements | Yes | インタラクティブ要素の配列 (max 25) |
| block_id | No | ブロック識別子 |

### Input Block

モーダル/ホームタブ用のフォーム入力。

```json
{
  "type": "input",
  "label": {
    "type": "plain_text",
    "text": "Title"
  },
  "element": {
    "type": "plain_text_input",
    "action_id": "title_input",
    "placeholder": {
      "type": "plain_text",
      "text": "Enter title"
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"input"` |
| label | Yes | ラベル (max 2000 chars) |
| element | Yes | 入力要素 |
| block_id | No | ブロック識別子 |
| hint | No | ヒントテキスト (max 2000 chars) |
| optional | No | 任意入力か (default: false) |
| dispatch_action | No | 入力時にアクション送信 |

### Video Block

動画を埋め込む。

```json
{
  "type": "video",
  "title": {
    "type": "plain_text",
    "text": "Video Title"
  },
  "video_url": "https://example.com/video.mp4",
  "thumbnail_url": "https://example.com/thumb.png",
  "alt_text": "Video description"
}
```

---

## Block Elements (Interactive)

### Button

```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click Me" },
  "action_id": "button_action",
  "style": "primary",
  "value": "click_value",
  "url": "https://example.com",
  "confirm": { ... }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"button"` |
| text | Yes | ボタンテキスト (max 75 chars) |
| action_id | Yes | アクション識別子 (max 255 chars) |
| style | No | `"primary"` (緑) / `"danger"` (赤) |
| value | No | ペイロード値 (max 2000 chars) |
| url | No | クリック時にURLを開く |
| confirm | No | 確認ダイアログ |
| accessibility_label | No | スクリーンリーダー用 (max 75 chars) |

### Static Select

```json
{
  "type": "static_select",
  "action_id": "select_action",
  "placeholder": { "type": "plain_text", "text": "Select" },
  "options": [
    {
      "text": { "type": "plain_text", "text": "Option 1" },
      "value": "option_1"
    }
  ],
  "initial_option": { ... }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| type | Yes | `"static_select"` |
| action_id | Yes | アクション識別子 |
| placeholder | No | プレースホルダー (max 150 chars) |
| options | Conditional | 選択肢 (max 100) |
| option_groups | Conditional | グループ化した選択肢 (max 100) |
| initial_option | No | 初期選択値 |
| confirm | No | 確認ダイアログ |

### External Select

外部データソースから選択肢を取得。

```json
{
  "type": "external_select",
  "action_id": "external_action",
  "placeholder": { "type": "plain_text", "text": "Search" },
  "min_query_length": 3
}
```

### Users Select

ワークスペースのユーザーを選択。

```json
{
  "type": "users_select",
  "action_id": "user_select",
  "placeholder": { "type": "plain_text", "text": "Select user" },
  "initial_user": "U0123456789"
}
```

### Conversations Select

チャンネル/DMを選択。

```json
{
  "type": "conversations_select",
  "action_id": "conversation_select",
  "placeholder": { "type": "plain_text", "text": "Select channel" },
  "initial_conversation": "C0123456789",
  "filter": {
    "include": ["public", "private"],
    "exclude_bot_users": true
  }
}
```

### Multi Select Variants

複数選択版。max_selected_itemsで選択数制限可能。

- `multi_static_select`
- `multi_external_select`
- `multi_users_select`
- `multi_conversations_select`
- `multi_channels_select`

### Date/Time Pickers

```json
{
  "type": "datepicker",
  "action_id": "date_action",
  "initial_date": "2024-01-15",
  "placeholder": { "type": "plain_text", "text": "Select date" }
}
```

```json
{
  "type": "timepicker",
  "action_id": "time_action",
  "initial_time": "14:30",
  "placeholder": { "type": "plain_text", "text": "Select time" }
}
```

```json
{
  "type": "datetimepicker",
  "action_id": "datetime_action",
  "initial_date_time": 1628633820
}
```

### Plain Text Input

```json
{
  "type": "plain_text_input",
  "action_id": "text_input",
  "placeholder": { "type": "plain_text", "text": "Enter text" },
  "initial_value": "Default text",
  "multiline": true,
  "min_length": 10,
  "max_length": 500
}
```

### Number Input

```json
{
  "type": "number_input",
  "action_id": "number_action",
  "is_decimal_allowed": true,
  "min_value": "0",
  "max_value": "100",
  "initial_value": "50"
}
```

### Radio Buttons

```json
{
  "type": "radio_buttons",
  "action_id": "radio_action",
  "options": [
    {
      "text": { "type": "plain_text", "text": "Option A" },
      "value": "A"
    },
    {
      "text": { "type": "plain_text", "text": "Option B" },
      "value": "B"
    }
  ],
  "initial_option": { ... }
}
```

### Checkboxes

```json
{
  "type": "checkboxes",
  "action_id": "checkbox_action",
  "options": [
    {
      "text": { "type": "plain_text", "text": "Check 1" },
      "value": "check_1"
    }
  ],
  "initial_options": [ ... ]
}
```

### Overflow Menu

「...」メニュー。最大5つのアクション。

```json
{
  "type": "overflow",
  "action_id": "overflow_action",
  "options": [
    {
      "text": { "type": "plain_text", "text": "Edit" },
      "value": "edit"
    },
    {
      "text": { "type": "plain_text", "text": "Delete" },
      "value": "delete"
    }
  ]
}
```

---

## Composition Objects

### Text Object

```json
{
  "type": "mrkdwn",
  "text": "*Bold* and _italic_"
}
```

```json
{
  "type": "plain_text",
  "text": "Plain text",
  "emoji": true
}
```

| Type | Description |
|------|-------------|
| `plain_text` | プレーンテキスト、絵文字対応 |
| `mrkdwn` | Slack独自のマークダウン形式 |

### Confirm Dialog

ユーザーアクション前に確認を求める。

```json
{
  "title": { "type": "plain_text", "text": "Confirm" },
  "text": { "type": "mrkdwn", "text": "Are you sure?" },
  "confirm": { "type": "plain_text", "text": "Yes" },
  "deny": { "type": "plain_text", "text": "No" },
  "style": "danger"
}
```

### Option Object

```json
{
  "text": { "type": "plain_text", "text": "Option" },
  "value": "option_value",
  "description": { "type": "plain_text", "text": "Description" }
}
```

### Option Group

```json
{
  "label": { "type": "plain_text", "text": "Group Label" },
  "options": [ ... ]
}
```

### Filter Object

conversations_selectで使用。

```json
{
  "include": ["public", "private", "mpim", "im"],
  "exclude_external_shared_channels": true,
  "exclude_bot_users": true
}
```

---

## mrkdwn Syntax

| Syntax | Result |
|--------|--------|
| `*bold*` | **bold** |
| `_italic_` | _italic_ |
| `~strike~` | ~~strike~~ |
| `` `code` `` | `code` |
| ` ```code block``` ` | コードブロック |
| `>quote` | 引用 |
| `<https://example.com\|Link>` | リンク |
| `<@U0123456789>` | ユーザーメンション |
| `<#C0123456789>` | チャンネルメンション |
| `<!here>` | @here |
| `<!channel>` | @channel |
| `:emoji_name:` | 絵文字 |

---

## References

- [Block Kit Overview](https://docs.slack.dev/reference/block-kit)
- [Blocks](https://docs.slack.dev/reference/block-kit/blocks)
- [Block Elements](https://docs.slack.dev/reference/block-kit/block-elements)
- [Composition Objects](https://docs.slack.dev/reference/block-kit/composition-objects)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
