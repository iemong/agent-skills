#!/usr/bin/env bash
# daily-commits.sh - 指定日のコミットを日報向けに集計
# Usage:
#   ./daily-commits.sh [YYYY-MM-DD] [options]
#
# Options:
#   --no-pr          PR取得（gh）をスキップ
#   --raw            その日のコミットログを“全部”そのまま表示（pretty=fuller + --stat）
#   --all-refs        refs/stash等も含めて全参照から取得（git log --all）
#   --all-authors    著者フィルタを無効化（全員分を対象）
#   --author <pat>   著者フィルタ（git log --author のパターン）
#   -h, --help       ヘルプ

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./daily-commits.sh [YYYY-MM-DD] [options]

Options:
  --no-pr          PR取得（gh）をスキップ
  --raw            その日のコミットログを“全部”そのまま表示（pretty=fuller + --stat）
  --all-refs        refs/stash等も含めて全参照から取得（git log --all）
  --all-authors    著者フィルタを無効化（全員分を対象）
  --author <pat>   著者フィルタ（git log --author のパターン）
  -h, --help       ヘルプ

Examples:
  ./daily-commits.sh
  ./daily-commits.sh 2026-01-16
  ./daily-commits.sh 2026-01-16 --no-pr
  ./daily-commits.sh 2026-01-16 --raw --all-authors
EOF
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

is_iso_date() {
  [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]
}

next_date() {
  local target_date="$1"

  if date -d "${target_date} +1 day" "+%Y-%m-%d" >/dev/null 2>&1; then
    date -d "${target_date} +1 day" "+%Y-%m-%d"
    return 0
  fi

  if date -j -f "%Y-%m-%d" "${target_date}" "+%Y-%m-%d" >/dev/null 2>&1; then
    date -j -v+1d -f "%Y-%m-%d" "${target_date}" "+%Y-%m-%d"
    return 0
  fi

  die "日付の計算に失敗しました（dateコマンド非対応）: ${target_date}"
}

TARGET_DATE="$(date +%Y-%m-%d)"
SKIP_PR=false
RAW_MODE=false
ALL_REFS=false
ALL_AUTHORS=false
AUTHOR_PATTERN=""
SEEN_DATE_ARG=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --no-pr)
      SKIP_PR=true
      shift
      ;;
    --raw)
      RAW_MODE=true
      shift
      ;;
    --all-refs)
      ALL_REFS=true
      shift
      ;;
    --all-authors)
      ALL_AUTHORS=true
      shift
      ;;
    --author)
      shift
      [[ $# -gt 0 ]] || die "--author には値が必要です"
      AUTHOR_PATTERN="$1"
      shift
      ;;
    --)
      shift
      break
      ;;
    -*)
      die "不明なオプション: $1"
      ;;
    *)
      if [[ "${SEEN_DATE_ARG}" == "true" ]]; then
        die "日付は1つだけ指定してください: 追加引数=$1"
      fi
      TARGET_DATE="$1"
      SEEN_DATE_ARG=true
      shift
      ;;
  esac
done

is_iso_date "${TARGET_DATE}" || die "日付は YYYY-MM-DD 形式で指定してください: ${TARGET_DATE}"

git rev-parse --show-toplevel >/dev/null 2>&1 || die "Gitリポジトリ内で実行してください: $(pwd)"

REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
NEXT_DATE="$(next_date "${TARGET_DATE}")"

CURRENT_BRANCH="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
LOG_REFS=(--branches --remotes)
if [[ "${ALL_REFS}" == "true" ]]; then
  LOG_REFS=(--all)
fi

if [[ "${ALL_AUTHORS}" == "false" ]]; then
  if [[ -z "${AUTHOR_PATTERN}" ]]; then
    AUTHOR_PATTERN="$(git config user.name 2>/dev/null || true)"
    if [[ -z "${AUTHOR_PATTERN}" ]]; then
      ALL_AUTHORS=true
    fi
  fi
fi

AUTHOR_ARGS=()
if [[ "${ALL_AUTHORS}" == "false" ]] && [[ -n "${AUTHOR_PATTERN}" ]]; then
  AUTHOR_ARGS+=(--author="${AUTHOR_PATTERN}")
fi

if [[ "${RAW_MODE}" == "true" ]]; then
  echo "## ${TARGET_DATE} のコミットログ（${REPO_NAME}）"
  echo ""
  echo '```text'
  git log "${LOG_REFS[@]}" \
    "${AUTHOR_ARGS[@]}" \
    --since="${TARGET_DATE} 00:00:00" \
    --until="${NEXT_DATE} 00:00:00" \
    --reverse \
    --date=iso-strict \
    --pretty=fuller \
    --stat
  echo '```'
  exit 0
fi

TMPDIR_CACHE="$(mktemp -d)"
trap 'rm -rf "${TMPDIR_CACHE}"' EXIT

COMMITS_FILE="${TMPDIR_CACHE}/commits"
git log "${LOG_REFS[@]}" \
  "${AUTHOR_ARGS[@]}" \
  --since="${TARGET_DATE} 00:00:00" \
  --until="${NEXT_DATE} 00:00:00" \
  --pretty=format:"%ct%x1f%cd%x1f%H%x1f%s" \
  --date=format-local:"%H:%M" \
  > "${COMMITS_FILE}"

LC_ALL=C sort -t $'\037' -k1,1n "${COMMITS_FILE}" -o "${COMMITS_FILE}"

COMMIT_COUNT="$(wc -l < "${COMMITS_FILE}" | tr -d ' ')"

if [[ "${COMMIT_COUNT}" -eq 0 ]]; then
  echo "## ${TARGET_DATE} のコミット一覧（${REPO_NAME}）"
  echo ""
  echo "_コミットはありません_"
  exit 0
fi

HASHES_FILE="${TMPDIR_CACHE}/hashes"
cut -d $'\037' -f3 "${COMMITS_FILE}" > "${HASHES_FILE}"

NAME_REV_FILE="${TMPDIR_CACHE}/name_rev"
: > "${NAME_REV_FILE}"

# xargs でまとめて name-rev（コミットごとの `git branch --contains` を廃止）
if [[ -s "${HASHES_FILE}" ]]; then
  < "${HASHES_FILE}" xargs -n 200 git name-rev \
    --refs='refs/heads/*' \
    --refs='refs/remotes/*' \
    2>/dev/null > "${NAME_REV_FILE}" || true
fi

BRANCH_CACHE="${TMPDIR_CACHE}/branches"
UNIQUE_BRANCHES_FILE="${TMPDIR_CACHE}/unique_branches"
: > "${BRANCH_CACHE}"
: > "${UNIQUE_BRANCHES_FILE}"

while read -r hash name; do
  [[ -n "${hash}" ]] || continue
  [[ -n "${name}" ]] || continue
  [[ "${name}" == "undefined" ]] && continue

  base="${name%%[~^]*}"
  base="${base#remotes/}"

  [[ -z "${base}" ]] && continue
  [[ "${base}" == "HEAD" ]] && continue

  echo "${hash}=${base}" >> "${BRANCH_CACHE}"
  clean_branch="${base#origin/}"
  [[ -n "${clean_branch}" ]] && echo "${clean_branch}" >> "${UNIQUE_BRANCHES_FILE}"
done < "${NAME_REV_FILE}"

UNIQUE_BRANCHES_SORTED="${TMPDIR_CACHE}/unique_branches.sorted"
sort -u "${UNIQUE_BRANCHES_FILE}" > "${UNIQUE_BRANCHES_SORTED}"
BRANCH_COUNT="$(wc -l < "${UNIQUE_BRANCHES_SORTED}" | tr -d ' ')"

PR_CACHE="${TMPDIR_CACHE}/prs"
: > "${PR_CACHE}"
if [[ "${SKIP_PR}" == "false" ]] && command -v gh >/dev/null 2>&1; then
  gh pr list --state all --limit 500 --json number,headRefName \
    --jq '.[] | "\(.headRefName)=#\(.number)"' \
    > "${PR_CACHE}" 2>/dev/null || true
fi

echo "## ${TARGET_DATE} のコミット一覧（${REPO_NAME}）"
echo ""
echo "| 時間 | ブランチ/PR | コミット内容 |"
echo "|------|------------|-------------|"

awk \
  -v branch_cache="${BRANCH_CACHE}" \
  -v pr_cache="${PR_CACHE}" \
  -v current_branch="${CURRENT_BRANCH}" \
  'BEGIN {
    FS="\037"
    while ((getline line < branch_cache) > 0) {
      split(line, a, "=")
      if (a[1] != "") branch[a[1]] = a[2]
    }
    while ((getline line < pr_cache) > 0) {
      split(line, a, "=")
      if (a[1] != "") pr[a[1]] = a[2]
    }
  }
  NF >= 4 {
    epoch=$1
    time=$2
    hash=$3
    subject=$4

    b = branch[hash]
    if (b == "") b = current_branch

    clean = b
    sub(/^origin\//, "", clean)

    prinfo = pr[clean]
    if (prinfo == "") prinfo = b
    if (prinfo == "") prinfo = "unknown"

    gsub(/\|/, "\\|", subject)
    printf "| %s | %s | %s |\n", time, prinfo, subject
  }' "${COMMITS_FILE}"

echo ""
echo "---"
echo "_集計時刻: $(date '+%Y-%m-%d %H:%M') / ブランチ数: ${BRANCH_COUNT} / コミット数: ${COMMIT_COUNT}_"
