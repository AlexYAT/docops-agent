# Validation corpus definition (T02 / DOA-OP-027)

Technical supporting artifact. Defines which Markdown files under `docs/` constitute the **validation corpus** for **DOA-OP-027** T03 and downstream validation steps, until superseded by a new T01 inventory + T02 pair.

## Source inventory artifact

| Field | Value |
|-------|-------|
| Path | `reports/doa_corpus_inventory_t01_op027.md` |
| Role | T01 inventory table (`Path \| doc_type \| ID \| Notes`) produced under **DOA-IMP-023** |
| Path rows (data lines) | **125** |

## Included set

**All** repository-relative paths listed in the **Path** column of the T01 inventory table (every table row whose Path begins with `docs/`).

Equivalently: **validation corpus = full T01 inventory** — no path from that table is excluded.

## Excluded set

**None.** No `docs/**/*.md` paths from the T01 inventory are excluded.

## Outside-`docs/` inclusions

**None.** Templates (`templates/`), root Markdown (`README.md`, `WORKFLOW.md`), and `reports/` are not part of this validation corpus (unchanged from **DOA-OP-027** T01 default).

## Effective date

**2026-04-16** — date from which this definition is authoritative for **DOA-OP-027** T03.

## Rationale

- The T01 inventory contains **only** canonical `docs/**/*.md` paths; there are **no** generated-only Markdown trees or duplicate mirrors under `docs/` that would justify exclusions.
- A **full-corpus** scope maximizes consistency checks before a future fixed snapshot and matches the recommended default in **DOA-OP-027** T02.
- **T03** must use this frozen path set so metadata review does not drift onto ad-hoc file discovery.

## Limitation

Paths added under `docs/` **after** the T01 inventory artifact was produced are **not** listed there and therefore are **not** in this validation corpus until a new T01 inventory is generated and T02 is re-run or superseded.
