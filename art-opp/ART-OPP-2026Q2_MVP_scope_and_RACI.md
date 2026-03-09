ART-OPP-2026Q2 — MVP Scope & RACI

MVP Goal
- Keyboard-first local app that ingests raw opportunity leads, applies a simple relevance score, and surfaces a triage queue for human reviewers.

Core Features (priority order)
1. Import & storage (local)
  - Import CSV / paste / watch-folder ingestion
  - Local encrypted archive option (opt-in)
  - Storage schema v2 (annotated fields + tags)
2. Tagging & Profile Integration
  - Canonical tag list and mapping to artist profiles
  - Import tags from memory/art-business profiles
3. Relevance scoring & filtering
  - Baseline scoring engine (rule-based)
  - Filters: location radius, fee range, deadline window
4. Triage UI (keyboard-first)
  - Single-item view with approve/reject/skip + quick-note
  - Bulk selection & bulk-approve with confirmation
  - Keyboard shortcuts (j/k, a, r, s, Ctrl+N for note)
5. Audit & backup
  - Audit log of actions
  - Snapshot backup and manual restore
6. CSV export (DeepSeek-compatible format)
7. Nightly encrypted ZIP backup (optional)

MVP Out-of-Scope
- ML-based ranking, cloud sync, complex workflows, third-party integrations beyond CSV.

Short RACI
- PO (Jane D.): Approve scoring formula, finalize MVP scope, stakeholder sign-off — R
- UX (Alex R.): Design triage flows, keyboard cheat sheet, Figma prototypes — A
- Arch (Sam T.): Locking & backup design, ADR — C
- Eng (team): Implement import/storage, scoring, triage UI, export — A/R
- QA: Acceptance criteria, test cases, pilot QA — C/R
- Security: Approve encryption/backup approach — C
