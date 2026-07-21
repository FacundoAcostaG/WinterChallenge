#!/usr/bin/env bash
# Corre las tres suites del challenge: API (Playwright), Performance (k6) y E2E (Behave + Playwright).
# Uso: ./run-tests.sh [api|performance|e2e]   -> sin argumentos corre todo

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

RUN_API=false
RUN_PERFORMANCE=false
RUN_E2E=false

case "${1:-all}" in
  all) RUN_API=true; RUN_PERFORMANCE=true; RUN_E2E=true ;;
  api) RUN_API=true ;;
  performance) RUN_PERFORMANCE=true ;;
  e2e) RUN_E2E=true ;;
  *)
    echo "Uso: $0 [api|performance|e2e]" >&2
    exit 1
    ;;
esac

FAILED=0

run_step() {
  local name="$1"
  shift
  echo ""
  echo "==> ${name}"
  if ! "$@"; then
    echo "!! ${name} falló"
    FAILED=1
  fi
}

if $RUN_API || $RUN_PERFORMANCE; then
  if [ ! -d node_modules ]; then
    echo "==> Instalando dependencias de npm"
    npm install
  fi
fi

if $RUN_API; then
  run_step "Tests de API (Playwright)" npm run test:api
fi

if $RUN_PERFORMANCE; then
  if ! command -v k6 >/dev/null 2>&1; then
    echo "!! k6 no está instalado. Instalalo con: brew install k6"
    FAILED=1
  else
    run_step "Tests de Performance (k6)" npm run test:performance
  fi
fi

if $RUN_E2E; then
  if [ ! -d e2e/.venv ]; then
    echo "==> Creando entorno virtual para e2e"
    python3 -m venv e2e/.venv
    # shellcheck disable=SC1091
    source e2e/.venv/bin/activate
    pip install -r e2e/requirements.txt
    playwright install chromium
  else
    # shellcheck disable=SC1091
    source e2e/.venv/bin/activate
  fi

  if [ ! -f e2e/.env ]; then
    cp e2e/.env.example e2e/.env
  fi

  run_step "Tests E2E (Behave + Playwright)" bash -c "cd e2e && behave"
  deactivate 2>/dev/null || true
fi

echo ""
if [ "$FAILED" -eq 0 ]; then
  echo "Todo OK"
else
  echo "Hubo fallas, revisá el detalle arriba"
fi
exit "$FAILED"
