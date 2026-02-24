# Notion Filter Examples

## Status equals

```json
{
  "property": "Status",
  "status": {
    "equals": "Done"
  }
}
```

## Date on or after

```json
{
  "property": "Due",
  "date": {
    "on_or_after": "2026-02-24"
  }
}
```

## Checkbox is true

```json
{
  "property": "Published",
  "checkbox": {
    "equals": true
  }
}
```

## Compound filter (and/or)

```json
{
  "and": [
    {
      "property": "Status",
      "status": {
        "does_not_equal": "Archived"
      }
    },
    {
      "or": [
        {
          "property": "Priority",
          "select": {
            "equals": "High"
          }
        },
        {
          "property": "Priority",
          "select": {
            "equals": "Urgent"
          }
        }
      ]
    }
  ]
}
```

## Sorts example

```json
[
  {
    "property": "Due",
    "direction": "ascending"
  },
  {
    "timestamp": "created_time",
    "direction": "descending"
  }
]
```
