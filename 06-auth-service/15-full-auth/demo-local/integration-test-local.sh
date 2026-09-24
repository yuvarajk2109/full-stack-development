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
MISSION_SERVICE_DIR="${MISSION_SERVICE_DIR:-C:/Users/Administrator/Documents/GitHub/full-stack-exercises/04-enterprise-java/mission-service}"
AUTH_PORT="${AUTH_PORT:-3000}"
SERVICE_PORT="${SERVICE_PORT:-8080}"

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"       # native Postgres default; the Docker lab used 5433
DB_NAME="${DB_NAME:-paysprint_wealth}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-n3u3d4!}"

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
mkdir -p /tmp
AUTH_LOG="/tmp/auth-local.log"
echo "Starting auth service, logs -> $AUTH_LOG"
PORT="$AUTH_PORT" node dist/main.js >"$AUTH_LOG" 2>&1 &
AUTH_PID=$!
echo "Auth service PID: $AUTH_PID"
sleep 1
echo "Auth service initial logs (first 40 lines):"
sed -n '1,40p' "$AUTH_LOG" || true

# ── Stage: Start the mission service (YOUR checkout, unmodified) ──────────────
echo "== Stage: Build + start the mission service (localhost:$SERVICE_PORT) =="
MISSION_LOG="/tmp/mission-local.log"
echo "Starting mission service, logs -> $MISSION_LOG"
MAVEN_RUN_ARGS="--server.port=$SERVICE_PORT --debug --spring.datasource.url=jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME --spring.datasource.username=$DB_USER --spring.datasource.password=$DB_PASSWORD"
echo "Invoking Maven with explicit JVM system properties to ensure Spring sees the DB settings"
mvn -q -f "$MISSION_SERVICE_DIR/pom.xml" \
  -Dspring.datasource.url="jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME" \
  -Dspring.datasource.username="$DB_USER" \
  -Dspring.datasource.password="$DB_PASSWORD" \
  -DskipTests \
  spring-boot:run \
  -Dspring-boot.run.arguments="$MAVEN_RUN_ARGS" \
  >"$MISSION_LOG" 2>&1 &
SERVICE_PID=$!
echo "Mission service PID: $SERVICE_PID"
sleep 1
echo "Mission service initial logs (first 40 lines):"
sed -n '1,40p' "$MISSION_LOG" || true

# ── Stage: Wait for both to be ready ─────────────────────────────────────────
echo "== Stage: Wait for both to be ready =="
AUTH_LOG_TAIL_LINES=30
MISSION_LOG_TAIL_LINES=30
for i in $(seq 1 30); do
  if curl -s -o /dev/null "http://localhost:$AUTH_PORT/health"; then
    echo "Auth service responded on attempt $i"
    break
  else
    echo "Auth not ready (attempt $i). Tail of $AUTH_LOG:"
    tail -n "$AUTH_LOG_TAIL_LINES" "$AUTH_LOG" || true
    sleep 2
  fi
done
for i in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
    -H "Content-Type: application/json" -d '{}' || true)
  if [ "$code" != "000" ]; then
    echo "Mission service responded with http code $code on attempt $i"
    break
  else
    echo "Mission not ready (attempt $i). Tail of $MISSION_LOG:"
    tail -n "$MISSION_LOG_TAIL_LINES" "$MISSION_LOG" || true
    sleep 2
  fi
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
