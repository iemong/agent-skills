# Notion Update Examples

## Status更新

```json
{
  "Status": {
    "status": {
      "name": "Done"
    }
  }
}
```

## Select更新

```json
{
  "Priority": {
    "select": {
      "name": "High"
    }
  }
}
```

## Number更新

```json
{
  "Estimate": {
    "number": 5
  }
}
```

## Rich text更新

```json
{
  "Requirements": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "要件を更新"
        }
      }
    ]
  }
}
```

## タイトル更新

```json
{
  "Title": {
    "title": [
      {
        "type": "text",
        "text": {
          "content": "新しいタイトル"
        }
      }
    ]
  }
}
```

## アイコン更新（emoji）

```json
{
  "type": "emoji",
  "emoji": "📝"
}
```

## カバー更新（external）

```json
{
  "type": "external",
  "external": {
    "url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
  }
}
```
