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
I manually verified the status-transition guardrail by hand rather than relying only on the automated test suite. I ran the API locally, created a task, and used curl to send a PATCH request attempting to move it directly from ToDo to Done (skipping InProgress): curl -X PATCH http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"status":"Done"}'. The API correctly rejected this with a 422 status code and a clear error message, matching the behavior documented in docs/verification.md's Break Test 1 (where this same rule was deliberately broken and confirmed to fail loudly, then restored). This confirms the business-rule guardrail actually holds at the API boundary, not just inside the test suite.

## One AI output I rejected or corrected
During tonight's security review, AI flagged that next_task_id (a global counter incremented in create_task) is not atomic and could theoretically produce duplicate task IDs under concurrent requests. I did not accept this as an actionable finding. I graded it Noise rather than Valid: this app runs as a single-developer local/demo service with in-memory storage, not a concurrent production system, so the realistic risk of two requests racing is effectively zero. Rather than "fixing" it with unnecessary locking complexity that the project scope does not call for, I documented the tradeoff and left the code as-is, which is itself a form of correcting the AI's implicit suggestion that this needed a code change.

## Three AI usage rules
1. Never paste: real credentials, API keys, .env contents, or production data into any AI tool or prompt.
2. Always verify: run the actual command (tests, curl, docker build) myself rather than trusting an AI's claim that something works.
3. Record AI contributions by: noting what AI helped draft or review in commit messages and in docs/final-ai-review.md, so there is always a paper trail distinguishing AI-suggested from human-verified work.

## Ownership statement
I am comfortable submitting this repository as my own work because every claim in it is backed by evidence I generated and checked myself tonight: the baseline was captured by actually running the API, hitting /health, and running the full pytest suite before any changes were made. The Docker image was built and run locally, with /health verified against the live container, not just assumed from the Dockerfile. The CI workflow's green run is a real GitHub Actions result I can link to, not a claim. The AI code review and security review above contain genuine findings from AI, each one graded and reasoned through by me, including deliberately grading two items as Noise where I judged the AI's concern to be technically correct but not practically significant. Where AI suggested a change I disagreed with, I documented why I left the code as-is instead of applying it blindly.
