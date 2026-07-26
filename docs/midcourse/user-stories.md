# User Stories

## Feature 1: Tags / Labels

**Story 1**
As a user, I want to add tags to a task so that I can categorize it by topic (e.g. "backend", "urgent").
- Acceptance criteria: POST /tasks accepts an optional `tags` list; blank/whitespace-only tags are silently dropped; valid tags are trimmed and stored.

**Story 2**
As a user, I want to filter my task list by tag so that I can quickly find related tasks.
- Acceptance criteria: GET /tasks?tag=<tag> returns only tasks containing that tag; no matches returns 200 with an empty list.

**Story 3**
As a user, I want my tags to remain unchanged when I update an unrelated field (like priority) so that I don't lose my categorization by accident.
- Acceptance criteria: PATCH /tasks/{id} with a payload that omits `tags` leaves existing tags untouched.

**Story 4**
As a user, I want to see my tags displayed as chips on each task card so that I can visually scan categories at a glance.
- Acceptance criteria: Each Kanban card renders a chip per tag under the task title.

**AI assumption corrected:** The AI initially proposed storing tags as a single comma-separated string field. I corrected this to a proper `list[str]` field in the Pydantic model, since a list is easier to filter and validate per-tag, and matches how the frontend needed to render individual chips.

---

## Feature 2: Due Dates + Overdue Filter

**Story 1**
As a user, I want to set a due date on a task so that I know when it needs to be completed.
- Acceptance criteria: POST /tasks and PATCH /tasks/{id} accept an optional `due_date` in YYYY-MM-DD format; invalid formats return 422.

**Story 2**
As a user, I want the system to tell me if a task is overdue so that I can prioritize it.
- Acceptance criteria: A task with a due_date in the past and a status other than "Done" is flagged `is_overdue: true` in API responses.

**Story 3**
As a user, I want a task marked "Done" to never show as overdue, even if its due date has passed, so that completed work doesn't clutter my overdue view.
- Acceptance criteria: `compute_is_overdue` returns False whenever status is Done, regardless of due_date.

**Story 4**
As a user, I want to filter my task list to show only overdue tasks so that I can focus on what's urgent.
- Acceptance criteria: GET /tasks?overdue=true returns only tasks where is_overdue is true.

**AI assumption corrected:** The AI's first draft computed "overdue" purely by comparing due_date to today's date, without considering task status. I corrected this so that Done tasks are never flagged overdue, since a completed task shouldn't be treated as behind schedule.