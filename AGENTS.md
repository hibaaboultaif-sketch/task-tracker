# AGENTS.md

This file gives AI coding agents (Cursor, Claude Code, Copilot, etc.) the
context they need to work safely in this repository.

## Stack
- Backend: FastAPI (Python 3.12)
- Testing: pytest
- Frontend: vanilla HTML/JS (single file, frontend/index.html)
- CI: GitHub Actions (.github/workflows/ci.yml)
- Containerization: Docker

## Commands
- Install dependencies: `pip install -r requirements.txt`
- Run the API locally: `uvicorn app.main:app --reload`
- Run tests: `pytest -v`
- Build Docker image: `docker build -t task-tracker .`
- Run Docker container: `docker run -p 8000:8000 task-tracker`
- Health check: `curl http://127.0.0.1:8000/health`

## Project rules
- This is the FINAL COURSE PROJECT branch (final-project). Do NOT add new
  product features (no auth, no notifications, no production database,
  no new UI sections).
- Only change files in app/ or frontend/ for a small, explainable bug fix,
  security fix, or documentation-supported correction. Any such change
  MUST be explained in docs/final-ai-review.md.
- Never commit real secrets, API keys, tokens, .env files, or personal/
  customer data.
- All 14 existing tests in tests/test_tasks.py must continue to pass.
  If a change breaks a test, either the change is wrong or the test
  needs an explicitly justified update — never silently skip or delete
  a test to make it pass.

## Read-first guardrail
Before proposing or making any code change, read:
1. README.md (for current setup/run/test commands)
2. docs/release-evidence.md (for the current known-good baseline)
3. The specific file(s) being touched, in full, before editing them

Do not assume

 file contents or project structure from memory or naming
conventions alone.

## Ownership
All AI-suggested changes in this repo have been reviewed by a human
before being accepted. See docs/final-ai-review.md for the review log,
security findings, and rejected/corrected AI suggestions.
