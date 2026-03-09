# Storage Schema v2 (Opportunity Record)

## Purpose

This document defines the canonical opportunity record used by ART-OPP-2026Q2.

## Required fields

- `id` (string): unique identifier (example: `opp_001`)
- `title` (string): opportunity title
- `source` (string): source system/site name
- `deadline` (string, date-time): submission deadline in ISO-8601
- `city` (string): city/location label
- `discipline` (string): artistic discipline (painting, mixed media, etc.)
- `fee_usd` (number): submission fee in USD
- `status` (enum): `new | approved | rejected | skipped`

## Optional fields

- `url` (string, uri): source listing URL
- `tags` (string[]): lightweight labels
- `notes` (string): freeform notes
- `score_total` (number): aggregate score from scoring engine
- `score_breakdown` (object): per-rule score contributions
- `created_at` / `updated_at` (string, date-time)

## Status transitions (intended)

- `new -> approved | rejected | skipped`
- `skipped -> approved | rejected`
- `approved/rejected` are terminal unless manually overridden by admin tooling.

## Compatibility

v2 introduces explicit `score_breakdown` and standardized status enum.
