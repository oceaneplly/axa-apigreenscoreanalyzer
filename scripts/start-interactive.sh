#!/usr/bin/env bash
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1 && python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,0) else 1)' >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3 is required" >&2
  exit 1
fi
python3() {
  "$PYTHON_BIN" "$@"
}
# start-interactive.sh
# Convenience launcher for the interactive Green API analyzer dashboard.
# Starts the local Python bridge (greenapianalyzer-server.py) and opens
# the workflow page in the default browser.
#
# Usage:
#   bash scripts/start-interactive.sh                # http://127.0.0.1:8765
#   bash scripts/start-interactive.sh --port 9000
#   bash scripts/start-interactive.sh --no-open

set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PORT=8765
HOST=127.0.0.1
OPEN_FLAG="--open"

while [ $# -gt 0 ]; do
  case "$1" in
    --port)    PORT="${2:-8765}";       shift 2 ;;
    --host)    HOST="${2:-127.0.0.1}";  shift 2 ;;
    --no-open) OPEN_FLAG="";            shift ;;
    -h|--help) sed -n '1,12p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

SERVER="$ROOT/scripts/greenapianalyzer-server.py"
if [ ! -f "$SERVER" ]; then
  echo "Bridge server not found: $SERVER" >&2
  exit 1
fi

echo "Starting interactive Green API analyzer on http://${HOST}:${PORT}/"
echo "  ROOT:   $ROOT"
echo "  SERVER: $SERVER"
echo "  (Ctrl+C to stop)"

if [ -n "$OPEN_FLAG" ]; then
  exec python3 "$SERVER" --host "$HOST" --port "$PORT" --open
else
  exec python3 "$SERVER" --host "$HOST" --port "$PORT"
fi

