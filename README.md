# Task Tracker

A FastAPI backend + vanilla JS Kanban frontend, extended with Tags/Labels and Due Dates/Overdue filtering.

## Running the backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

## Running the frontend

Open `frontend/index.html` directly in a browser (e.g. via `file://` path), with the backend running. CORS is enabled for local development.

## Running tests

```bash
source .venv/bin/activate
pytest tests/test_tasks.py -v
```

## Documentation

See `docs/` for user stories, ADR, prompt log, verification evidence, and reflection. markdown
## Final Project
Branch reviewed: final-project

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with /health returning 200.
- AI review, security, and ownership evidence is in docs/.

### How to run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

### How to run tests
pytest -v

### How to run with Docker
[to be filled in during Part B]

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary
AI helped draft or review: CI / Docker / docs / security / debugging.
I verified the work by: running pytest, checking /health, manually testing the frontend create/edit flow.
One AI suggestion I rejected or corrected: [to be filled in during Part C]
