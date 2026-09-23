# Lab 15-a — Mission Build: OpenAPI Docs & Replacing the Sprint 7 Stub (local, no Docker)

This is the local, **no-Docker** variant of Lab 15. It does exactly what Lab 15 does -
document the auth service's contract, then prove it can replace the stub for real - but
every piece runs as a **local process** instead of a Docker container. Use this when
Docker isn't available (Part 1 is identical to Lab 15; only Part 2's setup differs).

## Objectives

By the end of this lab you will have:

- Generated a live, browsable OpenAPI document for the auth service, continuing Sprint
  7's contract-first pattern into a second language and framework
- Completed an end-to-end integration test that proves a real token, issued by the
  NestJS auth service you have built since Module 8, authenticates a real, unmodified
  Spring Boot mission service route

## Setup

- **Node.js** (auth service) and **JDK 21 + Maven** (mission service) - no Docker.
- A **local Postgres** you can reach directly, with the `mission` database and the
  Sprint 3 enterprise schema (the same data the Docker lab assumed; you already have it
  from Sprint 3/6). Defaults: `localhost:5432`, db `mission`, user `postgres`, password
  `mission` - override with the `DB_*` env vars below if yours differ.
- A working checkout of your own Sprint 6/7 mission service (this lab does not include a
  copy of it - see `shared/mission-brief.md`). Point `MISSION_SERVICE_DIR` at it.
- Given, don't modify: `auth.service.ts`, `health.controller.ts`, `app.module.ts` (all
  unchanged since Module 14), and everything under your own mission service checkout -
  the mission service runs **exactly as-is**; the local script only overrides its
  datasource with the standard `SPRING_DATASOURCE_*` variables, just as the Docker
  version did with `-e SPRING_DATASOURCE_URL`.

## Part 1 — Complete the OpenAPI Documentation

Three `TODO`s, all about decorators - no behaviour changes:

1. **TODO 1 (`login.dto.ts`, `register.dto.ts`)** — add `@ApiProperty(...)` above each
   field, with an `example` and a short `description`.
2. **TODO 2 (`auth.controller.ts`)** — add `@ApiTags("auth")` above the class, and
   `@ApiOperation`/`@ApiResponse` above each route.
3. **TODO 3 (`main.ts`)** — build a `DocumentBuilder`, call
   `SwaggerModule.createDocument`, then `SwaggerModule.setup("api", app, document)`.

Run this now, before changing anything:

```bash
npm install
npm run build && npm start
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api
```

`404` - Swagger isn't wired up yet. That's the starting point.

### Verify

Complete the three TODOs, then rebuild and restart:

```bash
npm run build && npm start
```

Open `http://localhost:3000/api` in a browser - both routes should be documented, with
examples and response codes, not just bare paths. `GET /health` should NOT appear
(`@ApiExcludeController` on `HealthController` keeps operational plumbing out of the
public contract).

## Part 2 — Complete the Local Integration Test

`integration-test-local.sh` (macOS/Linux) and `integration-test-local.ps1` (Windows)
already contain the staging - config, a Postgres preflight, and starting **both services
as local processes** (`node dist/main.js` for auth, `mvn spring-boot:run` for the mission
service). Four `TODO`s remain - the same four as the Docker lab, now against local ports:

4. **Wait for both** to be ready - poll the auth service's `/health` and the mission
   service's `/accounts/1/orders`, the same retry-loop shape as Sprint 6.
5. **Smoke test**: a request with no token must return `401`.
6. **End-to-end**: log in against the *local* auth service, use the real token to submit
   a real order to the *local, completely unmodified* mission service.
7. **Confirm**: query your local Postgres directly (`psql`, not `docker exec`) to prove
   the order actually persisted.

Point `MISSION_SERVICE_DIR` at your own Sprint 6/7 checkout, then run the script for your
OS:

```bash
# macOS / Linux
export MISSION_SERVICE_DIR=/path/to/your/sprint6-or-7/mission-service
chmod +x integration-test-local.sh
./integration-test-local.sh
```

```powershell
# Windows (PowerShell)
$env:MISSION_SERVICE_DIR = "C:\path\to\your\sprint6-or-7\mission-service"
./integration-test-local.ps1
```

If your local Postgres differs from the defaults, override before running, e.g.
`DB_PORT=5433 DB_PASSWORD=secret ./integration-test-local.sh`.

Every stage should print `PASS`, ending with `== ALL STAGES PASSED ==`.

## The Point of This Lab

Nothing in your mission service changes. `SecurityConfig` validates a JWT's signature
against a shared secret - it has never cared which service issued the token. If this
script passes, you have proven the mission brief's central claim end to end, on a laptop
with no Docker at all - just two processes and a database.

## Deliverable

`main.ts`, `login.dto.ts`, `register.dto.ts`, and `auth.controller.ts` with OpenAPI
decorators added, plus `integration-test-local.sh` (or `.ps1`), fully implemented and
passing.

## Acceptance criteria

- `http://localhost:3000/api` shows both routes, documented, with `/health` excluded
- `./integration-test-local.sh` (or `.ps1`) exits `0` and prints `== ALL STAGES PASSED ==`
