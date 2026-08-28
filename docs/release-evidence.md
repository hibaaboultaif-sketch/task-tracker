# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-25
- Local app run command: `uvicorn app.main:app --reload`
- /health result: `GET http://127.0.0.1:8000/health` -> `{"status":"ok"}`
- Frontend check: Opened frontend/index.html directly in Safari; Kanban board (ToDo/InProgress/Done) loaded and creating a new task via "+ New Task" worked, task appeared in ToDo column.
- Test command: `pytest -v`
- Test result: 14 passed, 1 warning in 0.18s (warning is a pre-existing httpx/starlette TestClient deprecation notice, unrelated to final-project changes)

## CI evidence
- Workflow file: .github/workflows/ci.yml
- Latest run link or note: GitHub Actions run for commit 9ff583e on final-project branch, passed with green checkmark (View at: https://github.com/hibaaboultaif-sketch/task-tracker/actions)
- Test command used by CI: pytest -v
- Shortcut check: no continue-on-error / no || true / pytest is not skipped.

## Docker evidence
- Build command: `docker build -t task-tracker .`
- Run command: `docker run -p 8000:8000 task-tracker`
- /health check: `curl http://127.0.0.1:8000/health` -> `{"status":"ok"}`, confirmed 200 OK in container logs
- Non-root check, if implemented: Yes - Dockerfile creates and switches to non-root user (appuser) via useradd and USER instruction
- No-baked-secrets check: Yes - .dockerignore excludes .env, .git, docs, tests; only app/ and requirements.txt are copied into the image

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README claims interactive API docs are available at http://127.0.0.1:8000/docs | Started the API and opened http://127.0.0.1:8000/docs in browser | Confirmed - Swagger UI loaded showing all 7 endpoints (root, health, POST/GET/PATCH/DELETE tasks) | None needed |
| README/AGENTS.md claim CORS is enabled for local development | Opened app/main.py, checked lines 10-16 | Confirmed - CORSMiddleware present with allow_origins=["*"], allow_credentials=True | None needed |
| Docs claim the test suite has 14 tests, all passing | Ran pytest -v | Confirmed - output shows "collected 14 items" and "14 passed, 1 warning in 0.16s" | None needed - warning is a pre-existing httpx/starlette deprecation notice unrelated to app logic
