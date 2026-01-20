#!/bin/bash
# Arc Browser History to Markdown
# Usage: get_history.sh [limit] [date] [profile]
# date: YYYY-MM-DD format (optional, filters to that day)

LIMIT=${1:-100}
DATE=${2:-}
PROFILE=${3:-Default}
ARC_DIR="$HOME/Library/Application Support/Arc/User Data"
HISTORY_DB="$ARC_DIR/$PROFILE/History"
TMP_DB="/tmp/arc_history_$$.db"

if [ ! -f "$HISTORY_DB" ]; then
    echo "Error: History DB not found at $HISTORY_DB" >&2
    exit 1
fi

cp "$HISTORY_DB" "$TMP_DB"

# Build WHERE clause
WHERE_CLAUSE="WHERE hidden = 0"
if [ -n "$DATE" ]; then
    # Convert date to WebKit timestamp range (JST)
    # WebKit epoch offset: 11644473600 seconds
    START_TS=$(date -d "$DATE 00:00:00" "+%s" 2>/dev/null)
    END_TS=$(date -d "$DATE 23:59:59" "+%s" 2>/dev/null)

    if [ -n "$START_TS" ] && [ -n "$END_TS" ]; then
        # Adjust for JST (+9h = 32400s) and convert to WebKit microseconds
        START_WEBKIT=$(( (START_TS + 11644473600 - 32400) * 1000000 ))
        END_WEBKIT=$(( (END_TS + 11644473600 - 32400) * 1000000 ))
        WHERE_CLAUSE="$WHERE_CLAUSE AND last_visit_time BETWEEN $START_WEBKIT AND $END_WEBKIT"
    else
        echo "Error: Invalid date format. Use YYYY-MM-DD" >&2
        rm -f "$TMP_DB"
        exit 1
    fi
fi

sqlite3 -separator '|' "$TMP_DB" "
SELECT
    datetime((last_visit_time/1000000)-11644473600, 'unixepoch', '+9 hours') as visit_time,
    title,
    url
FROM urls
$WHERE_CLAUSE
ORDER BY last_visit_time DESC
LIMIT $LIMIT;
" | awk -F'|' '
BEGIN {
    print "| 日時 | タイトル | URL |"
    print "|------|----------|-----|"
}
{
    gsub(/\|/, "\\|", $2)
    printf "| %s | %s | %s |\n", $1, $2, $3
}'

rm -f "$TMP_DB"
