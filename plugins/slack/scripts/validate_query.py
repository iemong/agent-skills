#!/usr/bin/env python3
"""Validate Slack search query syntax."""

import argparse
import re
import sys

# Search Query Syntax based on https://docs.slack.dev/reference/
VALID_MODIFIERS = {
    "from": r"@?[\w.]+",        # from:@username or from:irie.s - 特定ユーザーの投稿
    "in": r"#?[\w-]+",          # in:#channel or in:channel-name - 特定チャンネル内
    "to": r"@?[\w.]+",          # to:@me or to:user.name - 自分宛てのDM
    "has": r"(link|emoji|pin|reaction|star|attachment)",  # has:link, has:emoji, has:pin
    "is": r"(thread|saved|starred)",  # is:thread, is:saved - 特定状態
    "before": r"\d{4}-\d{2}-\d{2}",    # before:2024-01-01 - 指定日より前
    "after": r"\d{4}-\d{2}-\d{2}",     # after:2024-01-01 - 指定日より後
    "on": r"\d{4}-\d{2}-\d{2}",        # on:2024-01-15 - 指定日
    "during": r"(today|yesterday|week|month|year|"  # during:january - 指定期間
              r"january|february|march|april|may|june|"
              r"july|august|september|october|november|december)",
}


def validate_query(query: str) -> tuple[bool, list[str]]:
    """Validate search query and return (is_valid, errors)."""
    errors = []
    
    # Extract modifiers (key:value patterns)
    modifier_pattern = r"(\w+):(\S+)"
    matches = re.findall(modifier_pattern, query)
    
    for key, value in matches:
        if key not in VALID_MODIFIERS:
            errors.append(f"Unknown modifier: {key}")
            continue
        
        pattern = VALID_MODIFIERS[key]
        if not re.fullmatch(pattern, value):
            errors.append(f"Invalid value for {key}: {value} (expected: {pattern})")
    
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Validate Slack search query")
    parser.add_argument("query", help="Search query to validate")
    args = parser.parse_args()
    
    is_valid, errors = validate_query(args.query)
    
    if is_valid:
        print("✓ Valid query")
    else:
        print("✗ Invalid query:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
