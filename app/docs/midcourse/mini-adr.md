# Mini Architecture Decision Record

## Context
The existing Task Tracker (Modules 1-3) had a working FastAPI backend with CRUD endpoints, status-transition rules, and a vanilla JS Kanban frontend. For this project, we added two features: **Tags/Labels** and **Due Dates + Overdue Filter**.

## Decision

### Tags
- Implemented as a `list[str]` field on `TaskCreate`/`TaskResponse`/`TaskUpdate`, validated via a `field_validator` that strips whitespace and drops empty entries.
- Filtering is done via an optional `tag` query parameter on `GET /tasks`, checked with simple Python `in` membership against each task's tag list.
- Rejected alternative: storing tags as a single comma-separated string. This was the AI's first suggestion, but it complicates filtering (would require string-splitting on every request) and doesn't map cleanly to the frontend's chip-rendering needs.

### Due Dates + Overdue
- `due_date` stored as a plain ISO-format string (`YYYY-MM-DD`), validated with a regex-based `field_validator`.
- `is_overdue` is **not** stored — it's computed on every read (`compute_is_overdue`), comparing `due_date` against `date.today()`, and returning `False` automatically for any task with status `Done`.
- Rejected alternative: storing `is_overdue` as a persisted field that gets updated on writes. This was considered but rejected as unnecessarily stateful — since overdue status changes purely with the passage of time (not user action), computing it at read-time keeps the in-memory model simple and avoids stale flags if the app runs across a date boundary without a write happening.
- An `overdue` boolean query parameter on `GET /tasks` filters using this same computed value.

### Frontend
- Both features were added to the existing single-file `frontend/index.html` (vanilla JS), consistent with the Module 3 approach, rather than introducing a new framework or build step, which would be out of scope for the timeframe.
- Rejected: a separate due-date picker library. A native HTML `<input type="date">` was used instead, sufficient for this project's scope.

### CORS
- Added `CORSMiddleware` with permissive settings (`allow_origins=["*"]`) since this is a local development project, not a production deployment. This directly follows the Module 3 lecture notes on the CORS issue that arises when serving the frontend via `file://` while the backend runs on `localhost:8000`.

## Consequences
- In-memory storage remains a limitation carried over from Module 2: all tasks (and their tags/due dates) reset when the server restarts. This is acceptable for the scope of this course project.
- The permissive CORS policy is not production-appropriate and would need to be locked down to a specific origin before any real deployment.