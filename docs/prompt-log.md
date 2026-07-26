# Prompt Log

## Feature 1: Tags / Labels

### Prompt 1 (models)
> Now let's add the actual API endpoints to app/main.py... [full models prompt covering TaskCreate/TaskResponse/TaskUpdate with tags: list[str] and due_date: str | None fields, plus field_validators]

**What AI returned:** Correctly added `tags` and `due_date` fields with validators to `TaskCreate`, but on the first attempt, the validators were attached to the wrong class (`TaskUpdate`) which didn't even have the matching fields defined, causing a mismatch.

**Accepted/edited/rejected:** Rejected the first attempt. Replaced the entire `models.py` file with a corrected version where helper functions (`_validate_tags`, `_validate_due_date`) are shared across `TaskCreate` and `TaskUpdate`, both with their own field_validators referencing the shared logic.

### Prompt 2 (weak → strong rewrite)
**Weak prompt:** "add tags to the tasks"

**Why it's weak:** No detail on validation rules, storage format, or how filtering should work — would leave the AI guessing at scope.

**Strong prompt:** "Add a `tags: list[str]` field to TaskCreate/TaskResponse/TaskUpdate. Validate that each tag is trimmed and non-empty; drop blank tags silently rather than rejecting the whole request. Add an optional `tag` query parameter to GET /tasks that filters tasks containing that tag."

**What AI returned:** Correct implementation matching all three constraints.

**Accepted:** Yes, as written.

### Prompt 3 (endpoints)
> Add tag filtering to GET /tasks as an optional query parameter, checking tag membership in each task's tags list.

**What AI returned:** Correct `tag: str | None = None` parameter with `[task for task in result if tag in task.tags]` filter logic.

**Accepted:** Yes, verified via Swagger UI with `tag=backend` returning only matching tasks.

---

## Feature 2: Due Dates + Overdue Filter

### Prompt 1 (models + validation)
> Add a `due_date: str | None` field, validated to be in YYYY-MM-DD format via regex, raising a ValueError otherwise.

**What AI returned:** Correct regex-based validator (`^\d{4}-\d{2}-\d{2}$`).

**Accepted:** Yes.

### Prompt 2 (overdue computation)
> Add a function to compute whether a task is overdue: true if due_date is in the past AND status is not Done.

**What AI returned:** First draft only checked `due_date < today()`, ignoring status entirely.

**Corrected:** Added an explicit `if task.status == Status.Done: return False` check before the date comparison, since a completed task should never show as overdue regardless of due date.

### Prompt 3 (weak → strong rewrite)
**Weak prompt:** "let me filter overdue tasks"

**Why it's weak:** Doesn't specify how "overdue" should be determined, or how the filter parameter should be named/typed.

**Strong prompt:** "Add an optional `overdue: bool | None` query parameter to GET /tasks. When true, return only tasks where the computed is_overdue flag is true. Compute is_overdue at read-time (not stored), based on due_date being in the past and status not being Done."

**What AI returned:** Correct implementation, verified via Swagger UI with `overdue=true`.

**Accepted:** Yes.

### Prompt 4 (CORS bug fix)
> The frontend at file:// can't reach the backend at localhost:8000 — "Error loading tasks."

**What AI returned/diagnosis:** Correctly identified this as a CORS issue and suggested adding `CORSMiddleware` with permissive origins for local development.

**Accepted:** Yes, applied exactly as suggested, verified by reloading the frontend and confirming the board loaded tasks successfully.