#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/validate-skill.sh <skill-dir> [<skill-dir> ...]" >&2
  exit 2
fi

validate_one() {
  local skill_dir="$1"
  local errors=0

  echo "Validating: ${skill_dir}"

  if command -v skills-ref >/dev/null 2>&1; then
    echo "  Using skills-ref"
    if skills-ref validate "$skill_dir"; then
      echo "  OK"
      return 0
    fi
    return 1
  fi

  if [ ! -e "$skill_dir" ]; then
    echo "  - Path does not exist: ${skill_dir}" >&2
    return 1
  fi

  if [ ! -d "$skill_dir" ]; then
    echo "  - Not a directory: ${skill_dir}" >&2
    return 1
  fi

  local skill_md="${skill_dir%/}/SKILL.md"
  if [ ! -f "$skill_md" ]; then
    echo "  - Missing required file: SKILL.md" >&2
    return 1
  fi

  local first_line
  first_line=$(head -n 1 "$skill_md" || true)
  if [ "$first_line" != "---" ]; then
    echo "  - SKILL.md must start with YAML frontmatter (---)" >&2
    return 1
  fi

  local frontmatter_count
  frontmatter_count=$(awk '$0=="---"{c++} END{print c+0}' "$skill_md")
  if [ "$frontmatter_count" -lt 2 ]; then
    echo "  - YAML frontmatter is not closed with a second ---" >&2
    return 1
  fi

  local frontmatter
  frontmatter=$(awk 'BEGIN{in=0} {if($0=="---"){if(in==0){in=1;next}else{exit}} if(in==1){print}}' "$skill_md")

  local allowed_fields="name description license allowed-tools metadata compatibility"
  local found_fields
  found_fields=$(printf "%s\n" "$frontmatter" | awk -F: '/^[A-Za-z0-9_-]+[[:space:]]*:/ {gsub(/[[:space:]]+$/, "", $1); print $1}')

  local field
  for field in $found_fields; do
    if ! printf "%s\n" "$allowed_fields" | awk -v f="$field" '{for(i=1;i<=NF;i++) if($i==f) found=1} END{exit found?0:1}'; then
      echo "  - Unexpected field in frontmatter: ${field}" >&2
      errors=1
    fi
  done

  get_value() {
    local key="$1"
    printf "%s\n" "$frontmatter" | awk -F: -v k="$key" '
      $0 ~ "^[[:space:]]*"k"[[:space:]]*:" {
        sub("^[^:]*:[[:space:]]*", "", $0)
        print $0
        exit
      }'
  }

  local name
  name=$(get_value "name")
  name=${name%%#*}
  name=$(printf "%s" "$name" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')
  name=${name#\"}
  name=${name%\"}
  name=${name#\'}
  name=${name%\'}

  if [ -z "$name" ]; then
    echo "  - Missing required field in frontmatter: name" >&2
    errors=1
  else
    local name_len
    name_len=$(printf "%s" "$name" | wc -m | tr -d ' ')
    if [ "$name_len" -gt 64 ]; then
      echo "  - Skill name exceeds 64 characters (${name_len})" >&2
      errors=1
    fi
    if [ "$name" != "${name,,}" ]; then
      echo "  - Skill name must be lowercase" >&2
      errors=1
    fi
    if [[ "$name" == -* || "$name" == *- ]]; then
      echo "  - Skill name cannot start or end with a hyphen" >&2
      errors=1
    fi
    if [[ "$name" == *"--"* ]]; then
      echo "  - Skill name cannot contain consecutive hyphens" >&2
      errors=1
    fi
    if ! printf "%s" "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
      echo "  - Skill name contains invalid characters (ASCII validator only)" >&2
      errors=1
    fi
    local dir_name
    dir_name=$(basename "$skill_dir")
    if [ "$dir_name" != "$name" ]; then
      echo "  - Directory name must match skill name (${dir_name} != ${name})" >&2
      errors=1
    fi
  fi

  local description
  description=$(get_value "description")
  description=${description%%#*}
  description=$(printf "%s" "$description" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')
  description=${description#\"}
  description=${description%\"}
  description=${description#\'}
  description=${description%\'}

  if [ -z "$description" ]; then
    echo "  - Missing required field in frontmatter: description" >&2
    errors=1
  else
    if [ "$description" = "|" ] || [ "$description" = ">" ]; then
      echo "  - Multiline YAML is not supported by this validator; use skills-ref" >&2
      errors=1
    fi
    local desc_len
    desc_len=$(printf "%s" "$description" | wc -m | tr -d ' ')
    if [ "$desc_len" -gt 1024 ]; then
      echo "  - Description exceeds 1024 characters (${desc_len})" >&2
      errors=1
    fi
  fi

  local compatibility
  compatibility=$(get_value "compatibility")
  compatibility=${compatibility%%#*}
  compatibility=$(printf "%s" "$compatibility" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')
  compatibility=${compatibility#\"}
  compatibility=${compatibility%\"}
  compatibility=${compatibility#\'}
  compatibility=${compatibility%\'}

  if [ -n "$compatibility" ]; then
    if [ "$compatibility" = "|" ] || [ "$compatibility" = ">" ]; then
      echo "  - Multiline YAML is not supported by this validator; use skills-ref" >&2
      errors=1
    fi
    local comp_len
    comp_len=$(printf "%s" "$compatibility" | wc -m | tr -d ' ')
    if [ "$comp_len" -gt 500 ]; then
      echo "  - Compatibility exceeds 500 characters (${comp_len})" >&2
      errors=1
    fi
  fi

  if [ "$errors" -eq 0 ]; then
    echo "  OK"
    return 0
  fi

  return 1
}

status=0
for skill_dir in "$@"; do
  if ! validate_one "$skill_dir"; then
    status=1
  fi
  echo
done

exit "$status"
