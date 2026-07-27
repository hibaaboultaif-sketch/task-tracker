markdown
# Verification

## Baseline Check (before starting)
Confirmed the Module 1/2 skeleton ran correctly before adding new features:
- `GET /` → `{"message": "Task Tracker API is running"}`
- `GET /health` → `{"status": "ok"}`
- Existing 6 pytest tests (Module 2) all passing.

## Backend Test Results
Full suite after adding both features:
14 passed, 1 warning in 0.15s
Breakdown:
- 6 original tests (create, blank title, 404, valid/invalid status transitions, delete) — all PASSED
- 8 new tests covering Tags and Due Dates/Overdue — all PASSED:
  - test_create_task_with_tags
  - test_create_task_blank_tag_is_dropped
  - test_update_tags_preserved_after_unrelated_update
  - test_filter_tasks_by_tag
  - test_create_task_invalid_due_date_format_fails
  - test_overdue_detection
  - test_future_due_date_not_overdue
  - test_filter_overdue_only

## Manual Browser/Swagger Checks
- Created a task via Swagger UI with `tags: ["backend", "urgent"]` and `due_date: "2026-01-01"` → response correctly showed `is_overdue: true`.
- Filtered `GET /tasks?tag=backend&overdue=true` → correctly returned only the matching task.
- Opened `frontend/index.html` in the browser → initially failed with "Error loading tasks" due to a CORS block between `file://` and `localhost:8000`. Fixed by adding `CORSMiddleware`. After the fix, the board loaded successfully and displayed tasks with tag chips.
- Created a task through the actual UI ("+ New Task" modal) with a due date and tags → confirmed via the Edit modal that the due date and tags were saved and returned correctly by the API.

## Behavior Contract (informal, before/after adding features)
| Behavior | Before | After |
|---|---|---|
| GET /, /health | Working | Working (unchanged) |
| 5 CRUD endpoints | Working | Working (unchanged, extended with tags/due_date fields) |
| Status-transition rule (ToDo→InProgress→Done only) | Working | Working (unchanged) |
| Tag filter on GET /tasks | N/A | Working |
| Overdue filter on GET /tasks | N/A | Working |
| Frontend Kanban board | N/A (built this session) | Working, displays tags as chips |

## Break Test Evidence

**Break Test 1 — Status transition rule (reused from Module 2):**
1. Commented out the `raise HTTPException(...)` call inside `validate_status_transition`, replacing it with `pass`.
2. Ran `pytest tests/test_tasks.py -v` → `test_invalid_status_transition_rejected` FAILED with `assert 200 == 422`, confirming the test correctly detects when the business rule is broken.
3. Reverted the change (restored the `raise HTTPException(...)` block).
4. Re-ran the suite → all 14 tests PASSED again.

**Break Test 2 — Overdue detection:**
1. Modified `compute_is_overdue` to always `return False` regardless of the due date comparison.
2. Ran `pytest tests/test_tasks.py -v` and observed the actual failure:
FAILED tests/test_tasks.py::test_overdue_detection - assert False is True
FAILED tests/test_tasks.py::test_filter_overdue_only - assert 0 == 1
2 failed, 12 passed, 1 warning in 0.24s
3. Reverted the change back to `return due < date.today()`.
4. Re-ran the suite and confirmed all tests passed again: