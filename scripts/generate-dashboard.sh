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
set -euo pipefail

GREEN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPORT_FILE=${1:-"$GREEN_DIR/reports/latest-report.json"}
TEMPLATE_FILE=${2:-"$GREEN_DIR/dashboard/index.save.html"}
OUT_FILE=${3:-"$GREEN_DIR/dashboard/index.html"}
CREEDENGO_REPORT=${4:-""}

# Build optional args
EXTRA_ARGS=""
if [ -f "$CREEDENGO_REPORT" ]; then
  EXTRA_ARGS="--creedengo-report $CREEDENGO_REPORT"
fi

python3 "$GREEN_DIR/scripts/generate-dashboard.py" --report "$REPORT_FILE" --template "$TEMPLATE_FILE" --output "$OUT_FILE" $EXTRA_ARGS
