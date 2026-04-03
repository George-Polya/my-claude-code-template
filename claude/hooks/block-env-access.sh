#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=""

if [[ "$TOOL" == "Bash" ]]; then
  COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
  if echo "$COMMAND" | grep -qE '\.env(\s|$|\.|\.local|\.production|\.staging|\.development|\*)' \
     && ! echo "$COMMAND" | grep -qE '\.env\.example'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":".env 파일 접근이 차단되었습니다. .env.example은 허용됩니다."}}'
    exit 0
  fi
else
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
  BASENAME=$(basename "$FILE_PATH")
  if [[ "$BASENAME" == .env* && "$BASENAME" != ".env.example" ]]; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":".env 파일 접근이 차단되었습니다. .env.example은 허용됩니다."}}'
    exit 0
  fi
fi

exit 0
