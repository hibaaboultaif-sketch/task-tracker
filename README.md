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

See `docs/midcourse/` for user stories, ADR, prompt log, verification evidence, and reflection.