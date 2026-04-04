#!/bin/bash

set -u

ENV_DENY_REASON=".env 파일 접근이 차단되었습니다. .env.example은 허용됩니다."
PARSE_DENY_REASON="훅 입력을 해석할 수 없어 요청을 차단했습니다."

deny() {
  local reason="$1"
  printf '%s\n' "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"$reason\"}}"
  exit 0
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || deny "$PARSE_DENY_REASON"
}

trim_candidate() {
  printf '%s' "$1" | sed -E 's/^[[:space:]"'"'"'"'"'"'=`({\[,:;]+//; s/[[:space:]"'"'"'"'"'"'`)}\],;]+$//'
}

is_blocked_env_basename() {
  local name="$1"
  [[ "$name" == .env* && "$name" != ".env.example" ]]
}

path_is_blocked() {
  local raw="$1"
  local candidate=""
  local basename_value=""

  candidate=$(trim_candidate "$raw")
  [[ -z "$candidate" ]] || {
    candidate="${candidate#file://}"
    candidate="${candidate%%\?*}"
    candidate="${candidate%%\#*}"
    basename_value=$(basename -- "$candidate")
    if is_blocked_env_basename "$basename_value"; then
      return 0
    fi
  }

  if [[ "$raw" == *=* ]]; then
    candidate=$(trim_candidate "${raw##*=}")
    [[ -z "$candidate" ]] || {
      candidate="${candidate#file://}"
      candidate="${candidate%%\?*}"
      candidate="${candidate%%\#*}"
      basename_value=$(basename -- "$candidate")
      if is_blocked_env_basename "$basename_value"; then
        return 0
      fi
    }
  fi

  return 1
}

command_has_blocked_env_reference() {
  local command="$1"
  local match=""

  while IFS= read -r match; do
    [[ -z "$match" ]] && continue
    if path_is_blocked "$match"; then
      return 0
    fi
  done < <(
    printf '%s\n' "$command" | grep -oE '(^|[^[:alnum:]_./-])([^[:space:]"'"'"'"'"'"'|&;()<>]*\/)?\.env[^[:space:]"'"'"'"'"'"'|&;()<>]*' || true
  )

  return 1
}

require_command jq
require_command sed
require_command grep
require_command basename

INPUT=$(cat)
[[ -n "$INPUT" ]] || deny "$PARSE_DENY_REASON"

printf '%s' "$INPUT" | jq -e . >/dev/null 2>&1 || deny "$PARSE_DENY_REASON"

TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[[ -n "$TOOL" ]] || deny "$PARSE_DENY_REASON"

case "$TOOL" in
  *Bash*|*bash*)
    COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
    [[ -n "$COMMAND" ]] || deny "$PARSE_DENY_REASON"

    if command_has_blocked_env_reference "$COMMAND"; then
      deny "$ENV_DENY_REASON"
    fi
    ;;
  *)
    while IFS= read -r file_path; do
      [[ -z "$file_path" ]] && continue
      if path_is_blocked "$file_path"; then
        deny "$ENV_DENY_REASON"
      fi
    done < <(
      printf '%s' "$INPUT" | jq -r '
        .tool_input
        | .. | objects
        | to_entries[]
        | select(.key == "file_path" or .key == "path" or .key == "absolute_path")
        | .value
        | strings
      ' 2>/dev/null
    )
    ;;
esac

exit 0
