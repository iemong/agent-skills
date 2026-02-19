#!/usr/bin/env python3
"""Slack Web API client script."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SLACK_API_BASE = "https://slack.com/api"

# Fields to keep in compact mode
COMPACT_MESSAGE_FIELDS = {"user", "text", "ts", "thread_ts", "reply_count", "reply_users_count"}

# Default max text length (0 = unlimited)
DEFAULT_MAX_TEXT_LENGTH = 500


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text if it exceeds max_length.

    Args:
        text: Original text
        max_length: Maximum length (0 = unlimited)

    Returns:
        Truncated text with suffix if truncated
    """
    if max_length <= 0 or len(text) <= max_length:
        return text
    remaining = len(text) - max_length
    return f"{text[:max_length]}\n(省略: 残り {remaining} 文字)"


def format_messages(messages: list, fmt: str, max_text_length: int = DEFAULT_MAX_TEXT_LENGTH) -> str:
    """Format messages based on output format.

    Args:
        messages: List of Slack messages
        fmt: Output format - 'text', 'compact', or 'full'
        max_text_length: Maximum text length per message (0 = unlimited)
    """
    if fmt == "full":
        return json.dumps({"ok": True, "messages": messages}, indent=2, ensure_ascii=False)

    if fmt == "text":
        lines = []
        for msg in messages:
            user = msg.get("user", "unknown")
            text = truncate_text(msg.get("text", ""), max_text_length)
            ts = msg.get("ts", "")
            lines.append(f"=== {user} ({ts}) ===")
            lines.append(text)
            lines.append("")
        return "\n".join(lines)

    # compact (default): filter fields and truncate text
    compact_messages = []
    for msg in messages:
        compact_msg = {k: v for k, v in msg.items() if k in COMPACT_MESSAGE_FIELDS}
        if "text" in compact_msg:
            compact_msg["text"] = truncate_text(compact_msg["text"], max_text_length)
        compact_messages.append(compact_msg)
    return json.dumps({"ok": True, "messages": compact_messages}, indent=2, ensure_ascii=False)


def get_token():
    """Get Slack token from environment variable."""
    token = os.environ.get("CLAUDE_SLACK_TOKEN")
    if not token:
        print("Error: CLAUDE_SLACK_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    return token


def slack_request(method: str, params: dict, use_get: bool = False) -> dict:
    """Make a Slack API request.

    Args:
        method: Slack API method name
        params: Request parameters
        use_get: If True, use GET request with query params (for conversations.* APIs)
    """
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    if use_get:
        query = urllib.parse.urlencode(params)
        url = f"{SLACK_API_BASE}/{method}?{query}"
        req = urllib.request.Request(url, headers=headers, method="GET")
    else:
        url = f"{SLACK_API_BASE}/{method}"
        data = json.dumps(params).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if not result.get("ok"):
                print(f"API Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
            return result
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)


def post_message(args):
    """Post a message to a channel."""
    params = {
        "channel": args.channel,
        "text": args.text,
    }
    if args.thread_ts:
        params["thread_ts"] = args.thread_ts
    if args.blocks:
        params["blocks"] = json.loads(args.blocks)
    
    result = slack_request("chat.postMessage", params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def dm_me(args):
    """Send a direct message to myself."""
    auth_result = slack_request("auth.test", {})
    if not auth_result.get("ok"):
        print(json.dumps(auth_result, indent=2, ensure_ascii=False))
        sys.exit(1)

    user_id = auth_result.get("user_id")
    if not user_id:
        print("API Error: user_id not found in auth.test response", file=sys.stderr)
        sys.exit(1)

    open_result = slack_request("conversations.open", {"users": user_id})
    if not open_result.get("ok"):
        print(json.dumps(open_result, indent=2, ensure_ascii=False))
        sys.exit(1)

    channel_id = open_result.get("channel", {}).get("id")
    if not channel_id:
        print("API Error: DM channel id not found in conversations.open response", file=sys.stderr)
        sys.exit(1)

    params = {
        "channel": channel_id,
        "text": args.text,
    }
    if args.blocks:
        params["blocks"] = json.loads(args.blocks)

    result = slack_request("chat.postMessage", params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def get_history(args):
    """Get channel message history."""
    params = {
        "channel": args.channel,
        "limit": args.limit,
    }
    if args.oldest:
        params["oldest"] = args.oldest
    if args.latest:
        params["latest"] = args.latest

    result = slack_request("conversations.history", params, use_get=True)
    if result.get("ok"):
        print(format_messages(result.get("messages", []), args.format, args.max_text_length))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def get_thread(args):
    """Get thread replies."""
    params = {
        "channel": args.channel,
        "ts": args.ts,
        "limit": args.limit,
    }

    result = slack_request("conversations.replies", params, use_get=True)
    if result.get("ok"):
        print(format_messages(result.get("messages", []), args.format, args.max_text_length))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def search_messages(args):
    """Search messages."""
    params = {
        "query": args.query,
        "count": args.count,
    }
    if args.sort:
        params["sort"] = args.sort
    if args.sort_dir:
        params["sort_dir"] = args.sort_dir
    if args.page:
        params["page"] = args.page

    result = slack_request("search.messages", params, use_get=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def my_posts(args):
    """Get my posts on a specific date."""
    query = f"from:me on:{args.date}"
    params = {
        "query": query,
        "count": args.count,
        "sort": "timestamp",
        "sort_dir": "asc",
    }

    result = slack_request("search.messages", params, use_get=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def get_user(args):
    """Get user info by ID."""
    params = {"user": args.user}
    result = slack_request("users.info", params, use_get=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Slack Web API client")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # post_message
    post_parser = subparsers.add_parser("post_message", help="Post a message")
    post_parser.add_argument("--channel", "-c", required=True, help="Channel name or ID (e.g. #general or C1234567890)")
    post_parser.add_argument("--text", "-t", required=True, help="Message text")
    post_parser.add_argument("--thread_ts", help="Thread timestamp for reply")
    post_parser.add_argument("--blocks", help="Block Kit blocks (JSON string)")
    post_parser.set_defaults(func=post_message)

    # dm_me
    dm_parser = subparsers.add_parser("dm_me", help="Send a DM to myself")
    dm_parser.add_argument("--text", "-t", required=True, help="Message text")
    dm_parser.add_argument("--blocks", help="Block Kit blocks (JSON string)")
    dm_parser.set_defaults(func=dm_me)
    
    # get_history
    history_parser = subparsers.add_parser("get_history", help="Get channel history")
    history_parser.add_argument("--channel", "-c", required=True, help="Channel ID")
    history_parser.add_argument("--limit", "-l", type=int, default=100, help="Number of messages")
    history_parser.add_argument("--oldest", help="Start of time range (timestamp)")
    history_parser.add_argument("--latest", help="End of time range (timestamp)")
    history_parser.add_argument("--format", "-f", choices=["text", "compact", "full"], default="compact",
                                help="Output format: text (minimal), compact (default), full (all fields)")
    history_parser.add_argument("--max-text-length", type=int, default=DEFAULT_MAX_TEXT_LENGTH,
                                help=f"Max text length per message (0=unlimited, default={DEFAULT_MAX_TEXT_LENGTH})")
    history_parser.set_defaults(func=get_history)

    # get_thread
    thread_parser = subparsers.add_parser("get_thread", help="Get thread replies")
    thread_parser.add_argument("--channel", "-c", required=True, help="Channel ID")
    thread_parser.add_argument("--ts", required=True, help="Thread timestamp")
    thread_parser.add_argument("--limit", "-l", type=int, default=100, help="Number of messages")
    thread_parser.add_argument("--format", "-f", choices=["text", "compact", "full"], default="compact",
                               help="Output format: text (minimal), compact (default), full (all fields)")
    thread_parser.add_argument("--max-text-length", type=int, default=DEFAULT_MAX_TEXT_LENGTH,
                               help=f"Max text length per message (0=unlimited, default={DEFAULT_MAX_TEXT_LENGTH})")
    thread_parser.set_defaults(func=get_thread)
    
    # search
    search_parser = subparsers.add_parser("search", help="Search messages")
    search_parser.add_argument("--query", "-q", required=True, help="Search query")
    search_parser.add_argument("--count", type=int, default=20, help="Number of results")
    search_parser.add_argument("--page", type=int, help="Page number")
    search_parser.add_argument("--sort", choices=["score", "timestamp"], help="Sort order")
    search_parser.add_argument("--sort_dir", choices=["asc", "desc"], help="Sort direction")
    search_parser.set_defaults(func=search_messages)
    
    # get_user
    user_parser = subparsers.add_parser("get_user", help="Get user info")
    user_parser.add_argument("--user", "-u", required=True, help="User ID (U1234567890)")
    user_parser.set_defaults(func=get_user)

    # my_posts
    my_posts_parser = subparsers.add_parser("my_posts", help="Get my posts on a specific date")
    my_posts_parser.add_argument("--date", "-d", required=True, help="Date (YYYY-MM-DD)")
    my_posts_parser.add_argument("--count", type=int, default=100, help="Number of results")
    my_posts_parser.set_defaults(func=my_posts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
