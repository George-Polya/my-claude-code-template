#!/bin/bash

read -p "복사할 대상 폴더 경로를 입력하세요 [기본값: ~/.claude/]: " TARGET_DIR
TARGET_DIR="${TARGET_DIR:-$HOME/.claude/}"

mkdir -p "$TARGET_DIR"

cp -r ./* "$TARGET_DIR"

echo "파일이 '$TARGET_DIR'(으)로 복사되었습니다."
unset ANTHROPIC_AUTH_TOKEN
echo "ANTHROPIC_AUTH_TOKEN이 해제되었습니다."

ANTHROPIC_BASE_URL="https://api.anthropic.com"

nvm install 24
