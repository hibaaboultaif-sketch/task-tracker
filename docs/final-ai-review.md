# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| CORS is configured with allow_origins=["*"] and allow_credentials=True at the same time in app/main.py. This combination is a known anti-pattern; wildcard origins should not be paired with credentialed requests. | Useful | No auth exists yet so current risk is low, but this should be fixed before any authentication is added to avoid a real cross-origin credential exposure later. | Did not change the code (no auth exists yet to be at risk), but flagged it as a known issue to revisit if auth is ever added. Documented here as evidence of review. |
| next_task_id is a plain module-level integer incremented in create_task(). Under concurrent requests this increment is not atomic, so two simultaneous POST /tasks calls could theoretically read the same ID before either increments it. | Noise | This app runs as a single-developer local/demo service with in-memory storage; the race window is real in theory but has effectively zero chance of triggering in this context. | Verified by reading the code path; no fix applied since it does not affect actual usage of this project. |
| update_task() uses task_update.model_dump(exclude_unset=True) before applying updates, which correctly avoids overwriting fields the client did not send. | Useful | Confirms the PATCH endpoint follows correct partial-update semantics; no bug found, but worth verifying since this is an easy mistake to make. | Verified by reading the code and cross-checking against test_update_tags_preserved_after_unrelated_update in tests/test_tasks.py, which passes. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| No API endpoint requires authentication or authorization; anyone who can reach the API can create, read, update, or delete any task. | app/main.py - no auth dependency on any route (@app.get, @app.post, @app.patch, @app.delete) | Valid | This is a real and significant gap. The final project brief explicitly forbids adding new features like auth, so this is documented as a known limitation rather than fixed. | No code change made (out of scope per project rules). Documented here as evidence the gap was identified and consciously deferred, not missed. |
| TaskCreate/TaskUpdate place no max length on title, description, assignee, or tag strings, and no max count on the tags list, while storage is an in-memory dict with no eviction. | app/models.py - TaskCreate/TaskUpdate field definitions; app/main.py - tasks: dict[int, TaskResponse] = {} | Valid | Real gap, but low severity given this runs as a single-developer local/demo service, not a public production deployment. | No code change made; noted as a limitation worth addressing if this app were ever deployed for real multi-user use. |
| _validate_due_date() only checks the due_date string matches the YYYY-MM-DD pattern via regex, not that it is a real calendar date (e.g. 2024-02-30 passes). compute_is_overdue() later fails silently on invalid dates via a caught ValueError. | app/models.py - _validate_due_date(); app/main.py - compute_is_overdue() try/except | Noise | Real behavior quirk but not a security issue - nothing is exploitable and no data is exposed, worst case is an incorrect is_overdue flag on one task. | No action needed; documented for completeness since it was found during review, not because it requires a fix.

## Manual security check
[To be completed]

## One AI output I rejected or corrected
[To be completed]

## Three AI usage rules
1. Never paste:
2. Always verify:
3. Record AI contributions by:

## Ownership statement
[To be completed]
