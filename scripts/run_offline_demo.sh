#!/bin/zsh

set -euo pipefail

if [[ $# -ne 3 ]]; then
  print -u2 "Usage: $0 DEMO_ROOT WIKI_BIN PYTHON_BIN"
  exit 2
fi

DEMO_ROOT="$1"
WIKI_BIN="$2"
PYTHON_BIN="$3"

if [[ ! -d "$DEMO_ROOT/vault/raw" ]]; then
  print -u2 "Demo root does not contain vault/raw: $DEMO_ROOT"
  exit 2
fi

if [[ ! -x "$WIKI_BIN" || ! -x "$PYTHON_BIN" ]]; then
  print -u2 "The wiki or Python executable is unavailable."
  exit 2
fi

export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_DISABLE_TELEMETRY=1
export PYTHONUNBUFFERED=1

cd "$DEMO_ROOT"

print '$ python network-isolation probe'
"$PYTHON_BIN" -c 'import socket
try:
    socket.create_connection(("example.com", 443), timeout=2)
except OSError as error:
    print(f"NETWORK_BLOCKED: {type(error).__name__}: {error}")
else:
    raise SystemExit("NETWORK_UNEXPECTEDLY_AVAILABLE")'

print '\n$ wiki --help'
"$WIKI_BIN" --help

print '\n$ /usr/bin/time -l wiki ingest ./vault/raw'
/usr/bin/time -l "$WIKI_BIN" ingest ./vault/raw

print '\n$ wiki ingest ./vault/raw'
"$WIKI_BIN" ingest ./vault/raw

print '\n$ wiki status'
"$WIKI_BIN" status

print '\n$ wiki ask "What are the two main parts of an AI agent?" --mode local'
"$WIKI_BIN" ask "What are the two main parts of an AI agent?" --mode local

print '\n$ wiki ask "How are context and memory defined in an agent system?" --mode local'
"$WIKI_BIN" ask "How are context and memory defined in an agent system?" --mode local

print '\n$ wiki ask "How can a team distinguish a model capability bottleneck from a harness design bottleneck?" --mode local'
"$WIKI_BIN" ask "How can a team distinguish a model capability bottleneck from a harness design bottleneck?" --mode local

print '\n$ wiki ask "What was the global revenue of the AI agent market in 2024?" --mode local'
"$WIKI_BIN" ask "What was the global revenue of the AI agent market in 2024?" --mode local

print '\n$ wiki chat --save  # capability, draft, and follow-up turns'
printf '%s\n' \
  'What can you help me with?' \
  'Draft a three-step plan for learning AI agents.' \
  'Make that shorter.' \
  '/exit' | "$WIKI_BIN" chat --save

print '\n$ wiki chat --save  # explicit note retrieval'
printf '%s\n' \
  'According to my notes, what are tools?' \
  '/exit' | "$WIKI_BIN" chat --save

print '\n$ wiki search "agent brain body tools" --save'
"$WIKI_BIN" search "agent brain body tools" --save

print '\n$ wiki chat --save  # temporary conversation fact'
printf '%s\n' \
  'My favorite color for this conversation is teal. Please remember it.' \
  'What color did I just mention?' \
  '/exit' | "$WIKI_BIN" chat --save

print '\n$ wiki ask "What is my favorite color?" --mode local'
"$WIKI_BIN" ask "What is my favorite color?" --mode local

print '\nOFFLINE_DEMO_COMPLETE'
