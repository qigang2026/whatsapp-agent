#!/usr/bin/env bash
# WhatsApp Agent · Cloudflare Pages 发布
# 直接把 publish/ 目录部署到 Pages（publish/ 已是 source of truth）

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUB="$ROOT/publish"
PROJECT_NAME="${1:-whatsapp-agent}"

if [[ ! -d "$PUB" ]]; then
  echo "ERROR: $PUB 不存在"
  exit 1
fi

echo "=== publish tree ==="
find "$PUB" -type f | sort
echo ""
echo "=== deploying to $PROJECT_NAME ==="
echo "  → Production URL: https://$PROJECT_NAME-30c.pages.dev"
echo "  → 本次部署 hash: 见下方 'Deployment complete' 链接"
echo ""
cd "$PUB"
wrangler pages deploy . --project-name="$PROJECT_NAME" --branch=main --commit-dirty=true
