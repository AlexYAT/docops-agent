# operational_plan — DOA-OP-027

## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-027
- Status: draft
- Date: 2026-04-15
- Parent: DOA-OP-026

_Create-only: new slice, new file; do not rewrite closed execution records._

---

## Title / Summary

**Execution slice (DOA-OP-026 T01–T03)** — ordered, zero-interpretation steps to produce (1) a corpus **inventory**, (2) a written **validation corpus scope**, and (3) a **classified metadata issues list**. This document does not execute T04+ from **DOA-OP-026**.

## Goal

Complete **T01 → T02 → T03** of **DOA-OP-026** so later tasks have a fixed set of files to validate and a triaged metadata posture.

## Context

- Parent plan: **DOA-OP-026** (`DOA-OP-026_validation_transition_first_fixed_snapshot`) — strategic transition **full corpus validation → first fixed snapshot preparation**.
- This file is a **tactical execution slice** covering only **T01–T03** of that parent.

## Scope

### In scope

- **T01** — Inventory the current corpus.
- **T02** — Define the validation corpus (inclusions/exclusions).
- **T03** — Review metadata consistency (required fields + classification).

### Out of scope

- **DOA-OP-026 T04+** (naming, links, legacy, snapshot readiness, index, decisions).
- Architecture decisions, validator/gate changes, authoring **fixed_snapshot**, implementing **document index**.

## Execution Order

1. **T01 — Inventory**  
2. **T02 — Validation scope definition**  
3. **T03 — Metadata review**

**Rationale**

- **T03 must not run before T01:** metadata review needs a **closed row set** (every file row is either in or out). Without an inventory, reviewers guess scope and repeat work when files are discovered later.
- **T02 before T03:** field checks apply only to files **in** the validation corpus. Scope must be explicit first so T03 does not report false “missing metadata” on intentionally excluded paths (e.g. generated `reports/`) or miss mandatory inclusions.

## Tasks

### T01 — Inventory the current corpus

| Step | Action |
|------|--------|
| 1.1 | **Where to look:** repository root; include **every `*.md` file** under `docs/` **recursively** (all subfolders). |
| 1.2 | **What to record per file:** relative path (POSIX-style, e.g. `docs/idea_to_mvp/DOA-IDEA-004_…md`); **nominal `doc_type`** = first-level folder name under `docs/` (segment after `docs/`); **declared `ID`** from the document’s metadata block (`- ID:` line) if present; **Notes** (empty or “no metadata block / no ID line”). |
| 1.3 | **Do not** in this task change any file; list-only. |
| 1.4 | **Result format (minimum):** one Markdown file **or** one CSV owned by this cycle, containing a **table** with columns **Path | doc_type | ID | Notes**. Filename is executor’s choice; path must be cited in T02/T03 (e.g. in a short “Artifacts” line). |

### T02 — Define the validation corpus

| Step | Action |
|------|--------|
| 2.1 | **Inputs:** completed T01 table (authoritative file list under `docs/`). |
| 2.2 | **Default validation corpus:** **all rows** from T01 (entire `docs/**/*.md` tree) unless a row is explicitly excluded in 2.3. |
| 2.3 | **Exclusions (if any):** list each excluded **Path** pattern or literal path and **one-line rationale** (e.g. generated-only, non-canonical mirror). If nothing is excluded, state: **“No exclusions; validation corpus = full T01 inventory.”** |
| 2.4 | **Inclusions outside `docs/`:** only if explicitly added here (path glob + rationale). Default = **none**. |
| 2.5 | **Where it is fixed:** append a subsection **“Validation corpus definition”** to the same artifact as T01 **or** a sibling artifact in the same working location; the subsection must contain **Included**, **Excluded** (or “None”), and **Effective date** (YYYY-MM-DD). |

### T03 — Review metadata consistency

| Step | Action |
|------|--------|
| 3.1 | **Inputs:** T01 table + T02 “Validation corpus definition” (only rows **included** in scope). |
| 3.2 | **Fields checked** (each included file): **Project**, **Doc type**, **ID**, **Status**, **Date**, **Parent** — each must appear as a `- <Field>:` line in a **Metadata** section (heading may be `## Metadata` or equivalent agreed in repo). |
| 3.3 | **Per field rules:** value non-empty after colon (whitespace-trimmed); **Doc type** must equal the folder’s canonical `doc_type` for that path; **ID** must equal the canonical document ID for that file if the repo convention assigns one in metadata. |
| 3.4 | **Classification (every issue):** **blocking** — prevents trustworthy validation or contradicts corpus identity (e.g. missing ID, wrong `doc_type`, Doc type mismatch vs path); **deferred** — cosmetic, optional field, or fix scheduled after snapshot prep (document rationale in one phrase). |
| 3.5 | **Output:** **metadata issues list** — table or bullet list: **Path | Field | Problem | Class (blocking / deferred) | Rationale (if deferred)**. |

## Outputs

1. **Inventory artifact** — T01 table (Path | doc_type | ID | Notes) covering all `docs/**/*.md`.  
2. **Validation scope definition** — T02 subsection: included set, excluded set (or explicit none), optional non-`docs/` inclusions, effective date.  
3. **Metadata issues list** — T03 classified findings for in-scope files only.

## Done Criteria

- [ ] Inventory artifact **exists** and includes **every** `docs/**/*.md` path present at T01 completion time.  
- [ ] Validation corpus is **explicitly documented**; every T01 row is **either** included **or** excluded with rationale.  
- [ ] Metadata issues list **exists**; each in-scope file has been **visited**; each listed issue has **blocking** or **deferred** classification.  
- [ ] Every **in-scope** path appears in the metadata issues list **either** with ≥1 issue row **or** on an attached **clean paths** list (same artifact or clearly linked).  
- [ ] No edits to **DOA-OP-026** and no implementation work outside this slice’s scope.

## Risks

- **Filesystem churn** between T01 and T03 — mitigate by noting inventory **timestamp** and re-diffing if many files move.  
- **Ambiguous metadata blocks** — mitigate by T03 rule: if no Metadata section, record one **blocking** row per missing block.

## Notes

- Traceability: **Parent = DOA-OP-026**; next execution slice for **DOA-OP-026** should reference outputs of **DOA-OP-027** by path/ID, not by rewriting this file.
