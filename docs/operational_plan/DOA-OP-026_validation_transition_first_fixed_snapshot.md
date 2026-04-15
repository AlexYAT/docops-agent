# operational_plan — DOA-OP-026

## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-026
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IDEA-004

_Create-only: a new operational cycle uses a new OP document; extend this plan with new entries rather than rewriting closed work._

---

## Title / Summary

**Validation transition for the first fixed snapshot** — an executable, planning-first path from the **current document corpus** through **full corpus validation** to **readiness to author the first `fixed_snapshot`**, including **transition requirements** for a future **document index** and a pragmatic **legacy classification** stance. This plan does **not** create the snapshot, change validators or gates, or finalize index mechanics.

## Goal

Produce a **controlled transition**: a validated view of the existing corpus, a clear **validation corpus definition**, resolved or explicitly parked **legacy inconsistencies**, and a **small, checkable checklist** of inputs and acceptance signals so the **first `fixed_snapshot`** can be created in a follow-on step **only after** this plan’s outcomes are satisfied—aligned with **DOA-IDEA-004** (fixed snapshot as its own `doc_type`, reference boundary after snapshot, index as existence rule).

## Context

- **DOA-IDEA-004** defines the target discipline: post–fixed-snapshot documents may reference **only** the snapshot and documents **created after** it; a **document index** will later make existence explicit for validators, gates, and managed prompts.
- The present corpus may contain **pre-boundary** material: uneven metadata, naming edge cases, or link/parent drift.
- This phase is **operational preparation**, not architecture delivery: stabilize what exists **before** declaring a fixed boundary.

## Scope

- **Full corpus validation campaign** for the **current** validation set (inventory, scope, link/metadata/naming review).
- **Readiness package** for the first **`fixed_snapshot`**: required inputs, minimal content expectations, and “green to draft snapshot” criteria—**without** authoring the snapshot in this plan.
- **Document index transition**: capture **initial requirements** and how the corpus inventory feeds the future index—**without** implementing the index.
- **Legacy classification**: interim rules for old, problematic, or partially aligned documents so they can be treated consistently until a snapshot exists.

## Non-goals

- Final **architecture_draft** for `fixed_snapshot` or index storage (may follow from findings).
- **Implementation** of validator changes, gate changes, or index automation.
- **Creating** the first `fixed_snapshot` or approving a final index schema.
- **Relaxing** post-snapshot reference rules or defining exceptions.

## Preconditions

- **DOA-IDEA-004** available as the conceptual anchor (Parent link).
- Ability to run **existing** validation tooling (e.g. link/id checks, document gate) as-is for baseline runs—no requirement to extend tools within this OP.
- Agreement that **planning-first** applies: snapshot work after this OP is **scheduled from** this OP’s outputs, not ad hoc.

## Tasks

### T01 — Inventory the current corpus

- Enumerate Markdown artifacts under `docs/` (and any other agreed roots) that are **in play** for DocOps.
- Record path, nominal `doc_type` (from directory), and **declared ID** from metadata where present.
- Output: a single **inventory table or list** (spreadsheet or section in working notes is fine) owned by this cycle.

### T02 — Define the validation corpus

- Decide explicitly which paths and file patterns constitute the **validation corpus** for this campaign (e.g. all `docs/**` vs. exclusions such as `reports/`).
- Document **inclusions, exclusions, and rationale** in one short subsection.
- Output: **validation scope statement** referenced by all later tasks.

### T03 — Review metadata consistency

- Against the inventory, check **required metadata fields** (Project, Doc type, ID, Status, Date, Parent) and flag missing or inconsistent values.
- Classify findings: **blocking** vs. **deferrable pre-snapshot** (deferrals must be listed explicitly).
- Output: **metadata review checklist** with item status.

### T04 — Review naming consistency

- Verify filenames and IDs follow the project’s **`DOA-<TYPE>-<NNN>`** conventions where applicable; note collisions or gaps.
- Output: **naming review notes** linked to inventory rows.

### T05 — Review links and parent/reference integrity

- Run existing link/id validation and gate (as applicable); collect **errors and warnings**.
- Manually spot-check **Parent** and cross-doc references for the highest-risk docs (bootstrap chain, audits, plans).
- Output: **link and integrity report summary** (pointer to machine reports plus a human triage list).

### T06 — Identify unresolved legacy issues

- Tag documents or clusters as: **aligned**, **legacy-candidate** (historical / low alignment), or **blocked** (must fix before snapshot readiness).
- Record **temporary policy**: legacy-candidate material remains in the tree but is **not** treated as the preferred dependency target for new work until after snapshot boundary rules apply.
- Output: **legacy classification appendix** (short list, not a full rewrite of history).

### T07 — Define minimal requirements for the first fixed snapshot

- List **mandatory sections and inputs** the first snapshot must contain (declarative state: structure, roadmap context, open steps, known gaps—per **DOA-IDEA-004**).
- Define **readiness gates**: e.g. “no blocking validator errors,” “metadata triage complete,” “legacy list acknowledged.”
- Output: **first fixed snapshot readiness brief** (bullet checklist, one page max).

### T08 — Define initial requirements for the document index

- Specify what the index must **represent** (existence, doc_type, path, ID) and **how** new docs will be registered once the index exists (process-level only).
- Explicitly state MVP stance: **transition goal** is a written spec, not a file format commitment.
- Output: **document index requirements draft** (short).

### T09 — Prepare next decision points

- List decisions that **must** be taken before implementation (e.g. index location, snapshot template ownership, whether multiple snapshots chain).
- Assign each to a likely artifact (**decision_log** / **architecture_draft**) without creating those artifacts here.
- Output: **decision backlog** for follow-up.

## Done criteria

- **Inventory** and **validation corpus** definition exist and are mutually consistent.
- **Metadata**, **naming**, and **link/parent** reviews are completed with a clear **blocking vs. deferred** posture.
- **Legacy classification** is written down; nothing is silently “assumed aligned.”
- **First fixed snapshot readiness brief** and **document index requirements draft** exist and are **reviewable in under ~15 minutes** each.
- **Decision backlog** points to the next planned artifacts; **no** snapshot and **no** index implementation attempted under this OP.

## Risks

- **Scope creep** into architecture or tool implementation—mitigate by strict non-goals.
- **Inventory drift** if the corpus changes during the campaign—mitigate with a dated snapshot of the inventory and re-run diff before closing.
- **False “green”** if gate/validator configs exclude real files—mitigate by aligning T02 with actual tool roots.

## Expected outputs

- Corpus **inventory** + **validation scope** statement.
- Consolidated **review artifacts** (metadata, naming, links/parents) with triage status.
- **Legacy classification** appendix.
- **First fixed snapshot readiness brief** (inputs + acceptance signals only).
- **Document index requirements draft** (behavioral / structural, not code).
- **Decision backlog** for subsequent planning or design artifacts.

## Follow-up

- Execute **implementation_snapshot** or other recording only if the team’s workflow requires a mid-cycle artifact after T05–T06 (optional; not part of this OP’s mandatory outputs).
- After this OP’s **Done criteria** are met: schedule **authoring the first `fixed_snapshot`** under a **new** operational_plan or an explicitly referenced execution slice—**not** by expanding this document against create-only discipline.
- Traceability: conceptual source **DOA-IDEA-004**; execution parent **DOA-IDEA-004** in metadata.
