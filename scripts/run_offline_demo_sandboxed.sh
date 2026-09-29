#!/bin/zsh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
TRANSCRIPT="$PROJECT_ROOT/evidence/recordings/offline-full-session-v2.txt"
DEMO_PARENT="$(mktemp -d -t personal-wiki-offline-v2)"
DEMO_ROOT="$DEMO_PARENT/repository"
COMMIT="$(git -C "$PROJECT_ROOT" rev-parse HEAD)"

if [[ ! -x "$PYTHON_BIN" ]]; then
  print -u2 "Python is unavailable at $PYTHON_BIN"
  exit 2
fi

git -C "$PROJECT_ROOT" clone --quiet --no-hardlinks "$PROJECT_ROOT" "$DEMO_ROOT"
git -C "$DEMO_ROOT" checkout --quiet "$COMMIT"
mkdir -p "$(dirname "$TRANSCRIPT")"

copy_artifacts() {
  mkdir -p "$PROJECT_ROOT/evidence/offline-demo-v2/runs" "$PROJECT_ROOT/evidence/ingest-drafts-v2"
  if [[ -d "$DEMO_ROOT/evidence/offline-demo-v2/runs" ]]; then
    cp -R "$DEMO_ROOT/evidence/offline-demo-v2/runs/." "$PROJECT_ROOT/evidence/offline-demo-v2/runs/"
  fi
  if [[ -d "$DEMO_ROOT/evidence/ingest-drafts-v2" ]]; then
    cp -R "$DEMO_ROOT/evidence/ingest-drafts-v2/." "$PROJECT_ROOT/evidence/ingest-drafts-v2/"
  fi
}
trap copy_artifacts EXIT

{
  print "UTC_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  print "GIT_COMMIT=$COMMIT"
  print "OUTER_COMMAND=/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' /bin/zsh [isolated-demo-root]/scripts/run_offline_demo_v2.sh [isolated-demo-root] [project-root]/.venv/bin/python"
  print '\n=== OUTSIDE-SANDBOX CONTROL PROBES (BOTH MUST SUCCEED) ==='
  "$PYTHON_BIN" - <<'PY'
import socket

addresses = socket.getaddrinfo("example.com", 443)
print(f"OUTSIDE_DNS_OK: {len(addresses)} address records")
with socket.create_connection(("1.1.1.1", 443), timeout=5):
    print("OUTSIDE_TCP_OK: connected to 1.1.1.1:443")
PY
  print '\n=== SANDBOXED DEMONSTRATION ==='
  /usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' \
    /usr/bin/env \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_DISABLE_TELEMETRY=1 \
    /bin/zsh "$DEMO_ROOT/scripts/run_offline_demo_v2.sh" "$DEMO_ROOT" "$PYTHON_BIN"
} 2>&1 | sed -e "s|$DEMO_ROOT|[isolated-demo-root]|g" -e "s|$PROJECT_ROOT|[project-root]|g" | tee "$TRANSCRIPT"
