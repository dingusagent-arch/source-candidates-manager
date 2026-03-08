# HEARTBEAT.md

# Active project: art-catalog hardening + backlog execution

On each heartbeat (unless user says stop), do exactly one focused work block on
`/home/dingus/Projects/art-catalog-2025` and report concise progress if anything changed.

Priority queue:
1. CSRF hardening end-to-end (backend enforcement + frontend header + tests)
2. Auth/session and destructive-flow test expansion
3. Delete/rebuild safety improvements (reduce partial-failure risk)
4. Frontend/backend pagination parity for large catalogs
5. Produce/update backlog report in `memory/90_inbox/`

Rules:
- Prefer direct implementation.
- Do not use Reason Agent unless Mark explicitly approves in that session.
- If blocked by secrets/sudo/external installs, report blocker clearly.
- If no actionable change is possible, reply HEARTBEAT_OK.
