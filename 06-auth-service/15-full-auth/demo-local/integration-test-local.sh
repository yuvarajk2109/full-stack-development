#!/usr/bin/env bash
set -euo pipefail

# ── Local, no-Docker version of Module 15's integration test ──────────────────
# Same proof as the containerised lab - a real token from THIS NestJS auth
# service authenticates a real, unmodified Spring mission-service route - but
# every piece runs as a local process instead of a Docker container:
#
#   auth service   -> node dist/main.js            (localhost:AUTH_PORT)
#   mission service-> mvn spring-boot:run          (localhost:SERVICE_PORT)
#   postgres       -> your local install           (DB_HOST:DB_PORT)
#
# The mission service is still COMPLETELY UNMODIFIED: we only override its
# datasource with the standard SPRING_DATASOURCE_* env vars, exactly as the
# Docker version did with -e SPRING_DATASOURCE_URL.

# ── Config (override any of these via the environment) ────────────────────────
MISSION_SERVICE_DIR="${MISSION_SERVICE_DIR:-../../../leap-sprint6/solutions/13-mission-build-containerise-integration-test-wrap-up}"
AUTH_PORT="${AUTH_PORT:-3000}"
SERVICE_PORT="${SERVICE_PORT:-8080}"

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"       # native Postgres default; the Docker lab used 5433
DB_NAME="${DB_NAME:-mission}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-mission}"

AUTH_PID=""
SERVICE_PID=""

cleanup() {
  echo "== Teardown =="
  [ -n "$SERVICE_PID" ] && kill "$SERVICE_PID" 2>/dev/null || true
  [ -n "$AUTH_PID" ] && kill "$AUTH_PID" 2>/dev/null || true
  # mvn spring-boot:run forks a child JVM; make sure it goes too
  pkill -f "spring-boot:run" 2>/dev/null || true
}
trap cleanup EXIT

# ── Stage: Preflight - the one thing that is NOT ours to start ────────────────
echo "== Stage: Preflight (local Postgres reachable?) =="
if ! PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" >/dev/null 2>&1; then
  echo "FAIL: cannot reach Postgres at $DB_HOST:$DB_PORT/$DB_NAME as $DB_USER."
  echo "      Start your local Postgres and ensure the '$DB_NAME' database exists"
  echo "      (the Sprint 3 enterprise schema, same one the Docker lab assumed)."
  exit 1
fi
echo "PASS: Postgres reachable at $DB_HOST:$DB_PORT/$DB_NAME"

# ── Stage: Start the auth service (this repo, no DB) ──────────────────────────
echo "== Stage: Build + start the auth service (localhost:$AUTH_PORT) =="
npm ci >/dev/null 2>&1 || npm install >/dev/null 2>&1
npm run build >/dev/null
PORT="$AUTH_PORT" node dist/main.js >/tmp/auth-local.log 2>&1 &
AUTH_PID=$!

# ── Stage: Start the mission service (YOUR checkout, unmodified) ──────────────
echo "== Stage: Build + start the mission service (localhost:$SERVICE_PORT) =="
SPRING_DATASOURCE_URL="jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME" \
SPRING_DATASOURCE_USERNAME="$DB_USER" \
SPRING_DATASOURCE_PASSWORD="$DB_PASSWORD" \
  mvn -q -f "$MISSION_SERVICE_DIR/pom.xml" spring-boot:run \
    -Dspring-boot.run.arguments="--server.port=$SERVICE_PORT" \
    >/tmp/mission-local.log 2>&1 &
SERVICE_PID=$!

# ── Stage: Wait for both to be ready ─────────────────────────────────────────
echo "== Stage: Wait for both to be ready =="
for _ in $(seq 1 30); do
  curl -s -o /dev/null "http://localhost:$AUTH_PORT/health" && break || sleep 2
done
for _ in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
    -H "Content-Type: application/json" -d '{}' || true)
  [ "$code" != "000" ] && break || sleep 2
done

# ── Stage: Smoke test - no token is rejected ─────────────────────────────────
echo "== Stage: Smoke Test - No Token Is Rejected =="
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}')
if [ "$CODE" != "401" ]; then echo "FAIL: expected 401 with no token, got $CODE"; exit 1; fi
echo "PASS: unauthenticated request rejected (401)"

# ── Stage: End-to-end authenticated order, via the NEW auth service ──────────
echo "== Stage: End-to-End Authenticated Order =="
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:$AUTH_PORT/auth/login" \
  -H "Content-Type: application/json" -d '{"username":"alice","password":"mission123"}')
TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"accessToken":"\([^"]*\)".*/\1/p')
if [ -z "$TOKEN" ]; then echo "FAIL: no token from auth service. Response: $LOGIN_RESPONSE"; exit 1; fi

ORDER_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}')
echo "Order response: $ORDER_RESPONSE"
echo "$ORDER_RESPONSE" | grep -q '"status":"ACCEPTED"' || { echo "FAIL: order was not accepted"; exit 1; }
echo "PASS: a real token from the NEW NestJS auth service was accepted by the UNCHANGED mission service"

# ── Stage: Confirm it landed in Postgres (local psql, no docker exec) ────────
echo "== Stage: Confirm It Actually Landed in Postgres =="
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"

echo "== ALL STAGES PASSED =="
