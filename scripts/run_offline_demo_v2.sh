#!/bin/zsh

set -euo pipefail

if [[ $# -ne 2 ]]; then
  print -u2 "Usage: $0 DEMO_ROOT PYTHON_BIN"
  exit 2
fi

DEMO_ROOT="$1"
PYTHON_BIN="$2"
RUN_MARKER="$DEMO_ROOT/.offline-demo-v2-start"

if [[ ! -d "$DEMO_ROOT/vault/raw" || ! -x "$PYTHON_BIN" ]]; then
  print -u2 "The demo root or Python executable is unavailable."
  exit 2
fi

export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_DISABLE_TELEMETRY=1
export PYTHONUNBUFFERED=1
export PYTHONPATH="$DEMO_ROOT/src"

cd "$DEMO_ROOT"
touch "$RUN_MARKER"

wiki() {
  "$PYTHON_BIN" -m personal_wiki.cli --project-root "$DEMO_ROOT" "$@"
}

print '=== DEVICE AND RUNTIME ==='
sw_vers
sysctl -n machdep.cpu.brand_string
sysctl -n hw.memsize
vm_stat | sed -n '1,8p'
df -h "$HOME"
"$PYTHON_BIN" --version
"$PYTHON_BIN" -m pip show mlx mlx-lm
print 'Model snapshots:'
find "$HOME/.cache/huggingface/hub/models--mlx-community--gemma-4-e4b-it-4bit/snapshots" \
  -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

print '\n=== INSIDE-SANDBOX NETWORK PROBES (BOTH MUST FAIL) ==='
"$PYTHON_BIN" - <<'PY'
import socket

try:
    socket.getaddrinfo("example.com", 443)
except OSError as error:
    print(f"INSIDE_DNS_BLOCKED: {type(error).__name__}: {error}")
else:
    raise SystemExit("INSIDE_DNS_UNEXPECTEDLY_AVAILABLE")

try:
    socket.create_connection(("1.1.1.1", 443), timeout=3)
except OSError as error:
    print(f"INSIDE_TCP_BLOCKED: {type(error).__name__}: {error}")
else:
    raise SystemExit("INSIDE_TCP_UNEXPECTEDLY_AVAILABLE")
PY

print '\n$ wiki --help'
wiki --help

print '\n$ /usr/bin/time -l wiki ingest ./vault/raw'
/usr/bin/time -l "$PYTHON_BIN" -m personal_wiki.cli --project-root "$DEMO_ROOT" ingest ./vault/raw

print '\n$ wiki ingest ./vault/raw'
wiki ingest ./vault/raw

print '\n$ wiki status'
wiki status

print '\n=== FOUR FIXED ASK QUESTIONS ==='
for question in \
  'What are the two main parts of an AI agent?' \
  'How are context and memory defined in an agent system?' \
  'How can a team distinguish a model capability bottleneck from a harness design bottleneck?' \
  'What was the global revenue of the AI agent market in 2024?'; do
  print "\n$ /usr/bin/time -l wiki ask \"$question\" --mode local"
  /usr/bin/time -l "$PYTHON_BIN" -m personal_wiki.cli --project-root "$DEMO_ROOT" \
    ask "$question" --mode local
done

print '\n=== CHAT MODE CHECKS ==='
chat_messages=(
  'What can we do?'
  'What can you help me with?'
  'Draft a three-step plan for learning AI agents.'
  'Make that shorter.'
  'Explain the model swap experiment.'
  'According to my notes, what are tools?'
)
for message in "${chat_messages[@]}"; do
  print "you> $message"
done
printf '%s\n' "${chat_messages[@]}" '/exit' | wiki chat --save

print '\n=== FORCED /notes CHECK ==='
print 'you> /notes context and memory'
printf '%s\n' '/notes context and memory' '/exit' | wiki chat --save

print '\n$ wiki search "agent brain body tools" --save'
wiki search "agent brain body tools" --save

print '\n=== CHAT FACT AND ASK SEPARATION ==='
print 'you> My favorite color for this conversation is teal. Please remember it.'
print 'you> What color did I just mention?'
printf '%s\n' \
  'My favorite color for this conversation is teal. Please remember it.' \
  'What color did I just mention?' \
  '/exit' | wiki chat --save
print '$ wiki ask "What is my favorite color?" --mode local'
wiki ask "What is my favorite color?" --mode local

print '\n=== CHANGED-SOURCE RE-INGEST IN THROWAWAY CLONE ==='
print '\nOffline demo change marker.' >> 'vault/raw/AI Agent Fundamentals.md'
wiki ingest ./vault/raw
print 'Wiki notes after changed-source ingest:'
find vault/wiki -name '*.md' | sort
print 'Drafts after changed-source ingest:'
find data/drafts -name '*.md' | sort
git checkout -- 'vault/raw/AI Agent Fundamentals.md'
print 'Source restored; re-ingesting restored bytes:'
wiki ingest ./vault/raw

mkdir -p evidence/ingest-drafts-v2 evidence/offline-demo-v2/runs
cp data/drafts/*.md evidence/ingest-drafts-v2/
find evidence/runs -type f -newer "$RUN_MARKER" -exec cp {} evidence/offline-demo-v2/runs/ \;

print '\nOFFLINE_DEMO_V2_COMPLETE'
