# idea_to_mvp — DOA-IDEA-004

## Metadata

- Project: DOA
- Doc type: idea_to_mvp
- ID: DOA-IDEA-004
- Status: draft
- Date: 2026-04-15
- Parent: null

_Create-only: after publication, create a new file with a new ID; do not rewrite approved versions._

---

## Title / Summary

**Fixed Snapshot** as a first-class document type and **Document Index** as the explicit existence rule for project artifacts—together they close a validation phase, draw a hard reference boundary between legacy and controlled DocOps work, and keep the system disciplined for a single-user MVP without requiring a heavy auto-scan pipeline in the first iteration.

## Problem

- Without a declared cut line, “what is canonical now?” drifts: new docs can silently depend on pre-boundary material, validators lose a stable baseline, and mental load grows.
- Bringing an **in-flight** project into DocOps needs a way to park everything before the boundary as **history/legacy** while still allowing forward work under strict rules.
- File presence alone is ambiguous: tools and prompts need a single list that defines **which documents exist for the system**.

## Why now

The document gate and validator tracks are maturing; the next failure mode is **graph chaos** (uncontrolled backlinks across eras) and **implicit corpora** (files not indexed but treated as real). This idea defines the minimum architecture to prevent that before the corpus grows further.

## Idea

Introduce two coordinated concepts:

1. **`fixed_snapshot`** — a **separate** `doc_type` (not a subtype or alias of `implementation_snapshot`). It is the **only allowed bridge** into the pre-boundary zone for documents created after it.
2. **Project document index** — an internal, authoritative enumeration of documents. **If a document is not in the index, it does not exist for the system**; validators, gates, and managed prompts should treat the index as the corpus boundary.

## Core mechanism

1. **Validation phase closure** — After a full validation pass over the current document set, a **fixed snapshot** artifact is created. It becomes the **canonical baseline** for the next phase of work.
2. **Reference boundary** — Documents created **after** the fixed snapshot may reference **only**:
   - the fixed snapshot itself, and/or
   - other documents also created **after** that snapshot.
   **Direct references to documents created before the snapshot are forbidden** (legacy/history zone is not a direct link target for new controlled docs).
3. **Declarative state** — The fixed snapshot holds a **full declarative description** of system/project state at the freeze point (structure, roadmap context, unfinished steps, known gaps, etc.). Later documents may treat the snapshot as an **aggregated source of truth** instead of fanning out to many legacy files.
4. **Index-driven existence** — New documents introduced through a gate or a **managed** prompt path must be **registered in the index**. Validators and gates use the index as the operational set of artifacts.

## Fixed snapshot role

- **Separate `doc_type`:** `fixed_snapshot` is its own type, distinct from `implementation_snapshot`.
- **Artifact closure:** It marks the end of the **current validation phase** and freezes the validated view into one durable artifact.
- **Baseline for the next phase:** All forward-controlled work is interpreted relative to this snapshot unless superseded by a later fixed snapshot (future evolution; not required for this MVP idea doc).

## Reference boundary rule

- **Strict by design:** uniformity, fewer mistakes, less chaos—acceptable for a **single-user** system in MVP.
- **One bridge:** Only the fixed snapshot may anchor understanding of the legacy zone; **no direct edges** from new controlled docs into pre-snapshot documents.
- **Possible liberalization** may be discussed later; it is **explicitly out of scope** for the current MVP framing.

## Project import / adoption scenario

- An existing codebase or doc tree is onboarded: everything **before** the first fixed snapshot is classified as **legacy/history zone**.
- Everything **after** the snapshot is the **controlled DocOps zone** governed by index + boundary rules.
- This supports “greenfield” and “brownfield” adoption with the same mechanical story: the snapshot is the hinge.

## Validation-closure scenario

1. Run corpus validation over the indexed document set for the phase.
2. Resolve or formally accept residual items per policy.
3. Author and publish **`fixed_snapshot`** capturing declarative full state.
4. Begin the next phase: new docs comply with the reference boundary and index rules.

## Document index concept

- **Internal project index** listing documents the system recognizes.
- **Existence rule:** absence from the index ⇒ **non-existence** for validators, gates, and prompt-based flows that are supposed to be managed.
- **Operational use:** the index is the backbone for “what to validate,” “what to allow in prompts,” and “what the gate may assume is in scope.”
- **Ingestion:** any new document created through the gate or a controlled prompt path **must** be appended (or otherwise registered) in the index.

## Expected benefits

- Clear **epoch boundary** between legacy and controlled work.
- **One** sanctioned path to historical context (the snapshot), reducing accidental dependency webs.
- **Explicit corpus** for automation—fewer “surprise” files and fewer stale links in policy.
- Repeatable **phase closure** after validation.

## Risks

- **Rigidity:** legitimate need to cite a specific legacy decision might force awkward indirection via snapshot summaries.
- **Index drift:** if registration is manual or semi-manual, the index can desync from the filesystem unless the process is enforced.
- **Snapshot authoring cost:** a “full declarative” snapshot is only as good as the discipline of what is written into it.

## Trade-offs

- **Intentional harshness** of rules vs. ergonomic linking—MVP favors the former for a single operator.
- **Declarative snapshot** vs. automated inventory—MVP does **not** require a complex auto-scan as a **mandatory** property of the snapshot document itself; depth can grow in later iterations.

## MVP scope

### In

- Conceptual definition of **`fixed_snapshot`** as its own `doc_type`.
- **Reference boundary** rule as stated (snapshot + post-snapshot docs only).
- **Validation phase closure** using a fixed snapshot as the pivot artifact.
- **Document index** as the existence criterion for system-recognized docs.
- **Onboarding** story for existing projects via legacy vs. controlled zones.
- **Declarative** snapshot content model (human-authored structured sections), without prescribing a specific auto-scan implementation.

### Out of scope

- Liberalized linking policies or exceptions machinery.
- Full automation for building the snapshot from repository scans (may exist later; not a hard MVP requirement for the snapshot concept itself).
- Multi-user ACL or workflow roles tied to snapshot approval.

## Open questions

- Exact **schema** for `fixed_snapshot` (sections, metadata fields, relationship to `Parent`).
- **Physical representation** of the document index (single file vs. generated artifact vs. embedded section in a known doc).
- Whether multiple fixed snapshots over time form a **chain** and how supersession is declared.
- How **strictly** “created after” is determined (Git time, metadata `Date`, or explicit manifest in the snapshot).

## Next steps

- Capture **`fixed_snapshot`** and **index** in **`architecture_draft`** (doc model, validator hooks, gate checks).
- Add **`decision_log`** entries once representation and enforcement level are chosen.
- Extend **`operational_plan`** / **`implementation_snapshot`** when implementation work is scheduled—without conflating `fixed_snapshot` with `implementation_snapshot`.
