# implementation_snapshot — DOA-IMP-023

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-023
- Status: draft
- Date: 2026-04-15
- Parent: DOA-OP-027

---

## Title / Summary

**T01 corpus inventory** for **DOA-OP-027** (execution slice **DOA-OP-026** T01–T03): a machine-assisted listing of every `docs/**/*.md` file with `doc_type` (first segment under `docs/`), declared `ID` from metadata when parseable, and **Notes** for gaps. No documents were modified.

## Context

- **DOA-OP-027** defines **T01 → T02 → T03** for the validation transition; this snapshot closes **T01** only.
- **DOA-OP-026** / **DOA-IDEA-004** provide the wider transition framing; they are not executed here.

## Executed scope

- Enumerate **all** `*.md` files under `docs/` recursively.
- For each file: **Path** (POSIX, repo-relative), **doc_type** (first path segment after `docs/`), **ID** (`- ID:` under a `## Metadata` section), **Notes** (`no metadata block` if `## Metadata` absent; `no ID line` if metadata present but no `- ID:` line; `ID blank` if ID empty).
- **Create-only:** no fixes to source markdown, no validator/gate runs required for this step.

## Artifact created

| Artifact | Path |
|----------|------|
| T01 inventory (Markdown table) | `reports/doa_corpus_inventory_t01_op027.md` |

T02 and T03 must **reference** this file as the inventory source of truth rather than re-deriving the file list ad hoc.

## Corpus coverage

| Metric | Value |
|--------|-------|
| Markdown files under `docs/` | **125** (includes this snapshot file in the inventory table) |
| Distinct `doc_type` roots (first-level folders) | **9** — `architecture_draft`, `audit_check`, `decision_log`, `idea_to_mvp`, `implementation_snapshot`, `longterm_plan`, `midterm_plan`, `operational_plan`, `rules` |
| Rows with `no metadata block` (per inventory Notes) | **43** |

All other inventoried rows (**82** of **125**) have a non-empty **ID** field in the table (metadata block with `- ID:` present and non-blank).

## Observations

- **Naming / placement anomaly:** `docs/implementation_snapshot/DOA-OP-017.md` lives under `implementation_snapshot` but uses an **OP** prefix and has **no metadata block** — visible at a glance in the inventory; not corrected (out of scope).
- **Duplicate IMP sequence:** two distinct files share the **IMP-014** numeric (`DOA-IMP-014_validator_hardening_baseline_pre_impl.md`, `DOA-IMP-014_validator_v02_planning_baseline.md`); inventory lists both as separate paths with valid IDs — flagged for later naming/T04 work, not fixed here.
- **Early ARCH files:** `DOA-ARCH-001` and `DOA-ARCH-002` show `no metadata block` in the inventory, consistent with older layout.

## Limitations

- **Scope:** only `docs/**/*.md` — excludes `templates/`, root `README.md`, `WORKFLOW.md`, and `reports/` (aligned with **DOA-OP-027** T01 default).
- **Parsing:** ID detection is line-based (`^- ID:`); unusual metadata layouts may require human review in **T03**, not in this snapshot.
- **Not executed:** **T02** (validation corpus definition), **T03** (metadata consistency classification), naming review, link validation, metadata remediation, **fixed_snapshot**, **document index**.

## Next step

- **DOA-OP-027 T02** — write the **validation corpus definition** (defaults, inclusions/exclusions, effective date) using this inventory as the authoritative path set.

## Traceability

- **Parent:** `DOA-OP-027` (`DOA-OP-027_op026_execution_slice_t01_t03.md`).
- **Upstream context:** `DOA-OP-026`, `DOA-IDEA-004` (concept only).
- **Supporting artifact:** `reports/doa_corpus_inventory_t01_op027.md`.
