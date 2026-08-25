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
- Workflow file:
- Latest run link or note:
- Test command used by CI:
- Shortcut check: no continue-on-error / no || true / pytest is not skipped.

## Docker evidence
- Build command:
- Run command:
- /health check:
- Non-root check, if implemented:
- No-baked-secrets check:

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
