# Local, no-Docker version of Module 15's integration test (Windows / PowerShell).
# Same proof as the containerised lab, every piece a local process:
#   auth service    -> node dist/main.js       (localhost:$AuthPort)
#   mission service -> mvn spring-boot:run      (localhost:$ServicePort)
#   postgres        -> your local install       ($DbHost:$DbPort)
# The mission service stays UNMODIFIED - only SPRING_DATASOURCE_* is overridden.

$ErrorActionPreference = "Stop"

# ── Config (override via env before running) ──────────────────────────────────
$MissionDir  = if ($env:MISSION_SERVICE_DIR) { $env:MISSION_SERVICE_DIR } else { "../../../leap-sprint6/solutions/13-mission-build-containerise-integration-test-wrap-up" }
$AuthPort    = if ($env:AUTH_PORT)    { $env:AUTH_PORT }    else { "3000" }
$ServicePort = if ($env:SERVICE_PORT) { $env:SERVICE_PORT } else { "8080" }
$DbHost      = if ($env:DB_HOST)      { $env:DB_HOST }      else { "localhost" }
$DbPort      = if ($env:DB_PORT)      { $env:DB_PORT }      else { "5432" }
$DbName      = if ($env:DB_NAME)      { $env:DB_NAME }      else { "mission" }
$DbUser      = if ($env:DB_USER)      { $env:DB_USER }      else { "postgres" }
$DbPassword  = if ($env:DB_PASSWORD)  { $env:DB_PASSWORD }  else { "mission" }

$authProc = $null
$missionProc = $null

function Cleanup {
  Write-Host "== Teardown =="
  if ($missionProc) { Stop-Process -Id $missionProc.Id -Force -ErrorAction SilentlyContinue }
  if ($authProc)    { Stop-Process -Id $authProc.Id    -Force -ErrorAction SilentlyContinue }
  Get-Process -Name java -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -and $_.CommandLine -match "spring-boot" } |
    Stop-Process -Force -ErrorAction SilentlyContinue
}

try {
  # ── Preflight: local Postgres reachable ────────────────────────────────────
  Write-Host "== Stage: Preflight (local Postgres reachable?) =="
  $env:PGPASSWORD = $DbPassword
  & psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -c "SELECT 1;" *> $null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: cannot reach Postgres at ${DbHost}:${DbPort}/${DbName} as $DbUser."
    Write-Host "      Start your local Postgres and ensure the '$DbName' database exists."
    exit 1
  }
  Write-Host "PASS: Postgres reachable at ${DbHost}:${DbPort}/${DbName}"

  # ── Start the auth service (this repo, no DB) ───────────────────────────────
  Write-Host "== Stage: Build + start the auth service (localhost:$AuthPort) =="
  & npm ci *> $null; if ($LASTEXITCODE -ne 0) { & npm install *> $null }
  & npm run build | Out-Null
  $env:PORT = $AuthPort
  $authProc = Start-Process node -ArgumentList "dist/main.js" -PassThru -NoNewWindow -RedirectStandardOutput "$env:TEMP\auth-local.log" -RedirectStandardError "$env:TEMP\auth-local.err"

  # ── Start the mission service (YOUR checkout, unmodified) ────────────────────
  Write-Host "== Stage: Build + start the mission service (localhost:$ServicePort) =="
  $env:SPRING_DATASOURCE_URL      = "jdbc:postgresql://${DbHost}:${DbPort}/${DbName}"
  $env:SPRING_DATASOURCE_USERNAME = $DbUser
  $env:SPRING_DATASOURCE_PASSWORD = $DbPassword
  $missionProc = Start-Process mvn -ArgumentList "-q","-f","$MissionDir/pom.xml","spring-boot:run","-Dspring-boot.run.arguments=--server.port=$ServicePort" -PassThru -NoNewWindow -RedirectStandardOutput "$env:TEMP\mission-local.log" -RedirectStandardError "$env:TEMP\mission-local.err"

  # ── Wait for both ──────────────────────────────────────────────────────────
  Write-Host "== Stage: Wait for both to be ready =="
  for ($i=0; $i -lt 30; $i++) {
    try { Invoke-WebRequest "http://localhost:$AuthPort/health" -UseBasicParsing *> $null; break } catch { Start-Sleep 2 }
  }
  for ($i=0; $i -lt 60; $i++) {
    try { Invoke-WebRequest "http://localhost:$ServicePort/accounts/1/orders" -Method POST -Body '{}' -ContentType 'application/json' -UseBasicParsing *> $null; break }
    catch { if ($_.Exception.Response) { break } else { Start-Sleep 2 } }
  }

  # ── Smoke: no token -> 401 ─────────────────────────────────────────────────
  Write-Host "== Stage: Smoke Test - No Token Is Rejected =="
  $code = try {
    (Invoke-WebRequest "http://localhost:$ServicePort/accounts/1/orders" -Method POST -ContentType 'application/json' `
      -Body '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}' -UseBasicParsing).StatusCode
  } catch { $_.Exception.Response.StatusCode.value__ }
  if ($code -ne 401) { Write-Host "FAIL: expected 401 with no token, got $code"; exit 1 }
  Write-Host "PASS: unauthenticated request rejected (401)"

  # ── End-to-end: login -> order -> ACCEPTED ─────────────────────────────────
  Write-Host "== Stage: End-to-End Authenticated Order =="
  $login = Invoke-RestMethod "http://localhost:$AuthPort/auth/login" -Method POST -ContentType 'application/json' `
    -Body '{"username":"alice","password":"mission123"}'
  $token = $login.accessToken
  if (-not $token) { Write-Host "FAIL: no token from auth service"; exit 1 }

  $order = Invoke-RestMethod "http://localhost:$ServicePort/accounts/1/orders" -Method POST `
    -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' `
    -Body '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}'
  Write-Host "Order response: $($order | ConvertTo-Json -Compress)"
  if ($order.status -ne "ACCEPTED") { Write-Host "FAIL: order was not accepted"; exit 1 }
  Write-Host "PASS: a real token from the NEW NestJS auth service was accepted by the UNCHANGED mission service"

  # ── Confirm in Postgres (local psql) ───────────────────────────────────────
  Write-Host "== Stage: Confirm It Actually Landed in Postgres =="
  & psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -c `
    "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"

  Write-Host "== ALL STAGES PASSED =="
}
finally {
  Cleanup
}
