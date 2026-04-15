# implementation_snapshot — DOA-IMP-026

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-026
- Status: draft
- Date: 2026-04-18
- Parent: DOA-OP-028

---

## Title / Summary

**MVP dual-mode validator and gate** — first rollout implementing **DOA-ARCH-021** / **DOA-DEC-047**: Git-derived **legacy / boundary / controlled** zones, **zone-tagged findings**, **cross-zone** detection for **controlled → legacy** markdown links, and a separate **`gate_status_controlled`** verdict in the document gate.

## Context

- **DOA-OP-028** — operational plan for this slice.
- **DOA-ARCH-021** — architecture contract.
- **DOA-DEC-047** — `boundary_commit` and zone rules; **DOA-FSN-001** — reference policy.

## What changed (code)

| Path | Change |
|------|--------|
| `scripts/doa_link_id_validator.py` | Git `first_commit` + zone classification; `FSN` ID family; `cross_zone_violations`; `dual_mode` summary; `source_zone` on findings; controlled→legacy link scan |
| `scripts/doa_document_gate.py` | Normalize cross-zone findings; `assign_severity` for `controlled_reference_to_legacy`; **`gate_status_controlled`**; **`dual_mode_counts`**; extended gate report schema label |

## Artifact created

| Artifact | Path |
|----------|------|
| First dual-mode gate report | `reports/doa_document_gate_run_003_dual_mode.json` |

## What works (MVP)

- **Zones:** each `docs/**/*.md` path classified **`legacy`**, **`boundary`**, or **`controlled`** using **`boundary_commit`** `d94a7d7…` and **`DOA-FSN-001`** path per **DOA-DEC-047**.
- **Findings:** `canonical_violations` and `legacy_findings` receive **`source_zone`** (POSIX path normalization for Windows).
- **Cross-zone:** controlled markdown links to **`.md`** files under `docs/` with target zone **`legacy`** emit **`controlled_reference_to_legacy`** (empty on current `main` after sample run).
- **Gate:** **`gate_status`** still reflects all findings (e.g. **REJECT** when legacy canonical errors exist); **`gate_status_controlled`** isolates **controlled + boundary** sources and **cross-zone** only — sample run: **`ACCEPT`** while overall **`REJECT`**.
- **Counts:** `dual_mode_counts` in gate JSON (`legacy_findings_count`, `controlled_findings_count`, `cross_zone_violations_count`, `other_zone_findings_count`).

## Limitations (MVP)

- **Git required:** zone classification calls `git` per path on each validator run — slow on large corpora; **shallow clones** may yield wrong or empty `first_commit` (noted in validator `dual_mode.note`).
- **Link scope:** only **relative** markdown links to existing `docs/**/*.md` targets are evaluated for cross-zone (same scope as extended link logic).
- **No document index**, no snapshot chain automation, no policy JSON file for `boundary_commit` yet — constant in validator is **MVP binding** until config work lands.
- **`gate_status`** unchanged semantically for backward compatibility; consumers should adopt **`gate_status_controlled`** for post-boundary health.

## Sample run (this commit)

- Command: `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_003_dual_mode.json --dry-run`
- Observed: **`gate_status=REJECT`**, **`gate_status_controlled=ACCEPT`** (legacy-heavy corpus; no blocking controlled-only defects in MVP slice).

## Next step

- Wire **optional cached zone map** for CI speed (**DOA-OP-028** follow-up).
- Tighten **cross-zone** coverage (e.g. bare `DOA-*` references in prose) if policy demands.
- Align **Policy Contract** / report schema versioning with **DOA-ARCH-020** when dual-mode fields stabilize.

## Traceability

- **Parent:** **DOA-OP-028**
- **Architecture:** **DOA-ARCH-021**
- **Boundary SoT:** **DOA-DEC-047**, **DOA-FSN-001**
