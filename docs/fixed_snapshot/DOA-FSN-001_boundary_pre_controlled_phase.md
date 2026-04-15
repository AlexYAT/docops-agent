# fixed_snapshot — DOA-FSN-001

## Metadata

- Project: DOA
- Doc type: fixed_snapshot
- ID: DOA-FSN-001
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-045

---

## Title

First fixed snapshot — pre–controlled-phase boundary (legacy vs controlled)

## Purpose

This artifact is the **first system boundary** for DocOps Agent documentation: it **declaratively freezes** the understood state of the corpus at boundary time, **separates legacy from controlled work**, and becomes the **canonical baseline** for all **new** documents created **after** it. It is **not** a retroactive cleanup and **not** a claim of historical perfection.

## System state

| Dimension | Declared state |
|-----------|----------------|
| Corpus size (paths under `docs/**/*.md` at T01) | **125** documents |
| Validation corpus | **Full** inventory — no exclusions (T02) |
| Metadata review (T03) | **45** blocking issue rows, **0** deferred, **81** clean paths, **44** paths with ≥1 issue |
| Legacy posture | Defects are **known and recorded** (see T03 artifact); **no** mass remediation applied before this boundary |

## Sources of truth

The following artifacts ground this snapshot (read together; none are superseded by prose here):

| Role | Artifact |
|------|----------|
| T01 inventory | `reports/doa_corpus_inventory_t01_op027.md` |
| T02 validation corpus | `reports/doa_validation_corpus_t02_op027.md` |
| T03 metadata review | `reports/doa_metadata_issues_t03_op027.md` |
| Policy — snapshot as-is | **DOA-DEC-045** |
| Concept | **DOA-IDEA-004** |
| Execution chain | **DOA-OP-026**, **DOA-OP-027**; **DOA-IMP-023**, **DOA-IMP-024**, **DOA-IMP-025** |

## Legacy zone

- **Definition (frozen path set):** exactly the **125** paths listed in `reports/doa_corpus_inventory_t01_op027.md` — the validation corpus from **T01/T02**. That set is the **legacy / historical** documentation layer for **direct-reference** purposes from the controlled zone.
- **Boundary artifact:** **DOA-FSN-001** itself is **not** part of that 125-path inventory; it is the **boundary document**, not legacy content.
- **Permitted condition:** legacy documents **may** lack `## Metadata`, use non-canonical keys, or violate current machine rules; that is **accepted and recorded**, not hidden.
- **Role:** historical / pre-boundary evidence; **not** a direct link target from new controlled documents.

## Controlled zone

- **Starts:** with the first **new** document created **after** **DOA-FSN-001** is accepted and present in the repository (and for all subsequent new documents).
- **Requirements for new documents:** **full** canonical **metadata** (Project, Doc type, ID, Status, Date, Parent), compliance with **validator / gate** policy as it applies to controlled artifacts, and **strict adherence** to **Boundary rules** below.

## Boundary rules

1. **No direct controlled → legacy links:** a document in the **controlled zone** **must not** reference legacy paths (pre-boundary inventory rows) **directly** in its link graph or citation practice intended as normative dependencies.
2. **Single bridge:** **DOA-FSN-001** is the **only** sanctioned aggregate bridge for understanding pre-boundary context; new work should treat this snapshot (and post-boundary docs) as the navigational baseline.
3. **Permitted references from controlled zone:** **only** (a) **DOA-FSN-001**, and/or (b) other documents **created after** **DOA-FSN-001** under controlled rules.
4. **Baseline:** future significant planning or architecture SHOULD cite **DOA-FSN-001** when grounding assumptions about system state at boundary time.

## Role of this snapshot

- **Not** an assertion of ideal or fully canonical history — it is a **fixed system point**.
- **Is** the declarative **baseline** for “what was known and accepted” at boundary time, including **honest** legacy limitations.
- **Is** the **sole sanctioned bridge** for normative understanding of pre-boundary context when writing new controlled documents.

## Known limitations

- **Metadata** across legacy is **not** normalized; T03 blocking rows remain unless remediated later under separate work.
- **Historical structure** is uneven (e.g. misplaced filenames, duplicate numeric IDs across files — see T03 observations).
- This snapshot **does not** perform **retroactive** cleanup; it **records** boundary and policy intent (**DOA-DEC-045**).

## Consequences

- Forward documentation work is **architecturally** in a **controlled phase** relative to legacy, subject to this contract.
- Legacy remediation, validator/gate layering for legacy vs controlled, and **document index** implementation remain **follow-on** engineering and documentation tasks — **out of scope** of this file.

## Next steps

- Implement or extend **architecture_draft** / tooling so validator–gate behavior matches **legacy vs controlled** semantics.
- Introduce **document index** and enforcement paths per **DOA-IDEA-004**.
- Continue **DOA-OP-026** slices (naming, links, legacy classification) as **evidence and hygiene**, not as a prerequisite to treat this boundary as void.

## Traceability

- **Parent:** **DOA-DEC-045** (snapshot-as-is policy).
- **Upstream concept:** **DOA-IDEA-004**.
- **Evidence:** T01–T03 reports under `reports/doa_*_op027.md` and **DOA-IMP-023**–**DOA-IMP-025**.
