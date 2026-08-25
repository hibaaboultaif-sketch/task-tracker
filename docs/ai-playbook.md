# My AI Playbook

## When I reach for AI first
- Scaffolding boilerplate (Dockerfiles, CI workflow YAML, test file skeletons)
- Debugging error messages I don't recognize
- Explaining unfamiliar syntax or library behavior
- Drafting documentation from an outline I already have

## When I do not reach for AI first
- Deciding what business rules the app should actually enforce
- Grading whether a review comment is actually worth acting on
- Anything touching real user data or credentials
- When I don't understand the existing code well enough to judge if an AI suggestion is safe

## My non-negotiables
- Never paste real secrets, tokens, or personal/customer data into any AI tool.
- Never accept a code change I can't explain in my own words afterward.
- Always run the actual command (tests, curl, docker build) myself instead of trusting an AI's description of the result.
- Keep AI-suggested changes small and reviewable, not sweeping rewrites.

## My review rules
- Read the full diff before accepting, not just the summary.
- Run the test suite after every AI-suggested change, before and after.
- Grade AI review comments individually (Useful/Noise/Wrong) rather than accepting the whole batch.
- If an AI comment is technically correct but doesn't matter for how the app is actually used, I mark it Noise instead of "fixing" it for the sake of fixing it.

## What I am still figuring out
- Where exactly the line is between "small bug fix" and "new feature" when a fix touches more than one file.
- How much to trust AI-generated security findings versus doing a fully manual pass myself.

## Decision Card
- New feature: default to NOT using AI to decide scope; I decide what's in scope, AI can help implement once scope is fixed.
- Code review: use AI to get a first pass of comments, but grade every single one myself.
- Debugging: AI first for unfamiliar errors, but reproduce the fix locally before trusting it.
- Infrastructure (CI/Docker): AI drafts, I verify every command actually runs before accepting.
- Never-paste: real secrets, tokens, .env files, or any personal/customer data.
- One rule: if I can't explain why a change is correct, I don't ship it.
