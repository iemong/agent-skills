#!/usr/bin/env python3
"""Query/update Notion pages with optional filters."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

NOTION_API_BASE_URL = "https://api.notion.com/v1"
DEFAULT_NOTION_VERSION = "2022-06-28"
MARKDOWN_NOTION_VERSION = "2025-09-03"
MAX_PAGE_SIZE = 100


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def load_json_input(json_text: Optional[str], json_file: Optional[str], label: str) -> Optional[Any]:
    """Load JSON from CLI argument or file path."""
    if json_text and json_file:
        fail(f"--{label} と --{label}-file は同時に指定できません")

    if not json_text and not json_file:
        return None

    raw = json_text
    if json_file:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                raw = f.read()
        except OSError as exc:
            fail(f"{label} ファイルの読み込みに失敗しました: {exc}")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"{label} のJSONが不正です: {exc}")


def notion_request(
    endpoint: str,
    method: str,
    payload: Optional[Dict[str, Any]],
    notion_token: str,
    notion_version: str,
    query_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Call Notion API once."""
    url = f"{NOTION_API_BASE_URL}{endpoint}"
    if query_params:
        qs = urllib.parse.urlencode(query_params)
        url = f"{url}?{qs}"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": notion_version,
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        message = raw_body
        try:
            parsed = json.loads(raw_body)
            message = parsed.get("message", raw_body)
        except json.JSONDecodeError:
            pass
        fail(f"Notion APIエラー (HTTP {exc.code}): {message}")
    except urllib.error.URLError as exc:
        fail(f"Notion APIリクエストに失敗しました: {exc.reason}")

    try:
        parsed_response = json.loads(response_body)
    except json.JSONDecodeError as exc:
        fail(f"Notion APIレスポンスがJSONではありません: {exc}")

    if not isinstance(parsed_response, dict):
        fail("Notion APIレスポンス形式が不正です")

    if parsed_response.get("object") == "error":
        fail(f"Notion APIエラー: {parsed_response.get('message', 'unknown error')}")

    return parsed_response


def notion_query(
    target_id: str,
    target_type: str,
    payload: Dict[str, Any],
    notion_token: str,
    notion_version: str,
) -> Dict[str, Any]:
    """Call Notion query API once."""
    if target_type == "database":
        endpoint = f"/databases/{target_id}/query"
    else:
        endpoint = f"/data-sources/{target_id}/query"
    return notion_request(endpoint, "POST", payload, notion_token, notion_version)


def notion_update_page(
    page_id: str,
    payload: Dict[str, Any],
    notion_token: str,
    notion_version: str,
) -> Dict[str, Any]:
    """Call Notion update page API once."""
    endpoint = f"/pages/{page_id}"
    return notion_request(endpoint, "PATCH", payload, notion_token, notion_version)


def notion_get_page_markdown(
    page_id: str,
    notion_token: str,
    include_transcript: bool = False,
) -> Dict[str, Any]:
    """Retrieve page content as enhanced markdown."""
    endpoint = f"/pages/{page_id}/markdown"
    query_params: Optional[Dict[str, str]] = None
    if include_transcript:
        query_params = {"include_transcript": "true"}
    return notion_request(
        endpoint, "GET", None, notion_token, MARKDOWN_NOTION_VERSION,
        query_params=query_params,
    )


def query_with_pagination(
    target_id: str,
    target_type: str,
    notion_token: str,
    notion_version: str,
    page_size: int,
    max_items: int,
    start_cursor: Optional[str],
    filter_obj: Optional[Dict[str, Any]],
    sorts_obj: Optional[List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """Fetch multiple pages until max_items is reached or no more pages."""
    results: List[Dict[str, Any]] = []
    next_cursor = start_cursor
    has_more = True
    api_calls = 0

    while has_more and len(results) < max_items:
        remaining = max_items - len(results)
        current_page_size = min(page_size, remaining, MAX_PAGE_SIZE)

        payload: Dict[str, Any] = {"page_size": current_page_size}
        if filter_obj is not None:
            payload["filter"] = filter_obj
        if sorts_obj is not None:
            payload["sorts"] = sorts_obj
        if next_cursor:
            payload["start_cursor"] = next_cursor

        response = notion_query(target_id, target_type, payload, notion_token, notion_version)
        api_calls += 1
        page_results = response.get("results", [])
        if not isinstance(page_results, list):
            fail("Notion APIレスポンスの results が配列ではありません")

        results.extend(page_results)
        has_more = bool(response.get("has_more"))
        next_cursor = response.get("next_cursor")

    return {
        "results": results,
        "count": len(results),
        "has_more": has_more,
        "next_cursor": next_cursor,
        "api_calls": api_calls,
    }


def compact_page(page: Dict[str, Any]) -> Dict[str, Any]:
    """Return compact representation of a Notion page."""
    return {
        "id": page.get("id"),
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
        "properties": page.get("properties", {}),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query/update Notion database/data-source items."
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["query", "update-page", "get-markdown"],
        default="query",
        help="Operation type (default: query)",
    )

    target_group = parser.add_mutually_exclusive_group(required=False)
    target_group.add_argument("--database-id", help="Notion database ID")
    target_group.add_argument("--data-source-id", help="Notion data source ID")

    parser.add_argument("--filter", dest="filter_json", help="Filter JSON string")
    parser.add_argument("--filter-file", help="Filter JSON file path")
    parser.add_argument("--sorts", dest="sorts_json", help="Sorts JSON string")
    parser.add_argument("--sorts-file", help="Sorts JSON file path")
    parser.add_argument("--start-cursor", help="Start cursor for pagination")
    parser.add_argument("--page-size", type=int, default=100, help="Items per API call (1-100)")
    parser.add_argument("--max-items", type=int, default=100, help="Maximum total items to fetch")

    parser.add_argument("--page-id", help="Notion page ID (for update-page)")
    parser.add_argument("--properties", dest="properties_json", help="Page properties JSON string")
    parser.add_argument("--properties-file", help="Page properties JSON file path")
    parser.add_argument("--icon", dest="icon_json", help="Page icon JSON string")
    parser.add_argument("--icon-file", help="Page icon JSON file path")
    parser.add_argument("--cover", dest="cover_json", help="Page cover JSON string")
    parser.add_argument("--cover-file", help="Page cover JSON file path")

    archived_group = parser.add_mutually_exclusive_group(required=False)
    archived_group.add_argument("--archived", dest="archived", action="store_true", help="Set archived=true")
    archived_group.add_argument("--unarchive", dest="archived", action="store_false", help="Set archived=false")
    parser.set_defaults(archived=None)

    trash_group = parser.add_mutually_exclusive_group(required=False)
    trash_group.add_argument("--in-trash", dest="in_trash", action="store_true", help="Set in_trash=true")
    trash_group.add_argument(
        "--restore-from-trash",
        dest="in_trash",
        action="store_false",
        help="Set in_trash=false",
    )
    parser.set_defaults(in_trash=None)

    parser.add_argument("--include-transcript", action="store_true", help="Include meeting note transcripts (get-markdown)")
    parser.add_argument("--notion-version", default=os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION))
    parser.add_argument("--compact", action="store_true", help="Return compact page objects")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    notion_token = os.environ.get("CLAUDE_NOTION_TOKEN")
    if not notion_token:
        fail("CLAUDE_NOTION_TOKEN が設定されていません")

    if args.command == "update-page":
        if not args.page_id:
            fail("update-page では --page-id が必須です")

        properties_obj = load_json_input(args.properties_json, args.properties_file, "properties")
        if properties_obj is not None and not isinstance(properties_obj, dict):
            fail("--properties はJSONオブジェクトで指定してください")

        icon_obj = load_json_input(args.icon_json, args.icon_file, "icon")
        if icon_obj is not None and not isinstance(icon_obj, dict):
            fail("--icon はJSONオブジェクトで指定してください")

        cover_obj = load_json_input(args.cover_json, args.cover_file, "cover")
        if cover_obj is not None and not isinstance(cover_obj, dict):
            fail("--cover はJSONオブジェクトで指定してください")

        update_payload: Dict[str, Any] = {}
        if properties_obj is not None:
            update_payload["properties"] = properties_obj
        if icon_obj is not None:
            update_payload["icon"] = icon_obj
        if cover_obj is not None:
            update_payload["cover"] = cover_obj
        if args.archived is not None:
            update_payload["archived"] = args.archived
        if args.in_trash is not None:
            update_payload["in_trash"] = args.in_trash

        if not update_payload:
            fail("update-page では更新内容を1つ以上指定してください")

        updated_page = notion_update_page(
            page_id=args.page_id,
            payload=update_payload,
            notion_token=notion_token,
            notion_version=args.notion_version,
        )
        output_page = compact_page(updated_page) if args.compact else updated_page
        output = {
            "ok": True,
            "action": "update-page",
            "page": output_page,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.command == "get-markdown":
        if not args.page_id:
            fail("get-markdown では --page-id が必須です")

        result = notion_get_page_markdown(
            page_id=args.page_id,
            notion_token=notion_token,
            include_transcript=args.include_transcript,
        )
        output = {
            "ok": True,
            "action": "get-markdown",
            "page_id": result.get("id"),
            "markdown": result.get("markdown", ""),
            "truncated": result.get("truncated", False),
            "unknown_block_ids": result.get("unknown_block_ids", []),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.page_size < 1 or args.page_size > MAX_PAGE_SIZE:
        fail("--page-size は 1-100 の範囲で指定してください")
    if args.max_items < 1:
        fail("--max-items は 1 以上で指定してください")
    if bool(args.database_id) == bool(args.data_source_id):
        fail("query では --database-id か --data-source-id のどちらか一方が必須です")

    filter_obj = load_json_input(args.filter_json, args.filter_file, "filter")
    if filter_obj is not None and not isinstance(filter_obj, dict):
        fail("--filter はJSONオブジェクトで指定してください")

    sorts_obj = load_json_input(args.sorts_json, args.sorts_file, "sorts")
    if sorts_obj is not None and not isinstance(sorts_obj, list):
        fail("--sorts はJSON配列で指定してください")

    target_type = "database"
    target_id = args.database_id
    if args.data_source_id:
        target_type = "data-source"
        target_id = args.data_source_id

    query_result = query_with_pagination(
        target_id=target_id,
        target_type=target_type,
        notion_token=notion_token,
        notion_version=args.notion_version,
        page_size=args.page_size,
        max_items=args.max_items,
        start_cursor=args.start_cursor,
        filter_obj=filter_obj,
        sorts_obj=sorts_obj,
    )

    pages = query_result["results"]
    if args.compact:
        pages = [compact_page(page) for page in pages]

    output = {
        "ok": True,
        "action": "query",
        "target_type": target_type,
        "target_id": target_id,
        "count": query_result["count"],
        "has_more": query_result["has_more"],
        "next_cursor": query_result["next_cursor"],
        "api_calls": query_result["api_calls"],
        "results": pages,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
