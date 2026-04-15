## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-046
- Status: accepted
- Date: 2026-04-18
- Parent: DOA-IDEA-004

---

## Title

Formalize fixed_snapshot as a first-class document type

## Context

- **DOA-FSN-001** (`docs/fixed_snapshot/DOA-FSN-001_boundary_pre_controlled_phase.md`) was authored as the **first** `fixed_snapshot` — a **boundary artifact** between **legacy** (frozen T01 path set) and **controlled** documentation, per **DOA-IDEA-004** and **DOA-DEC-045**.
- An **external architecture audit** (**DOA-AUD-010**) identified a **governance gap**: the `fixed_snapshot` **doc_type** was used in the repository **before** it was introduced through **decision_log**, registered in **naming convention** (**DOA-ARCH-008**), or listed among **supported doc_types** in project governance rules.
- DocOps relies on explicit definitions: if a type is not part of the agreed model, tooling, prompts, and humans cannot treat it as canonical — risking **policy drift** and inconsistent validation.

## Problem

- **`fixed_snapshot` was in use but not formally defined** in the system’s governance artifacts (no prior **decision_log** for the type; no **TYPE** mapping in **DOA-ARCH-008**; no canonical **supported doc_types** entry).
- That sequence **breaks planning-first / explicit-decisions discipline**: a new artifact class appeared without a recorded decision that the system as a whole accepts it.
- **Risk:** validators, gates, templates, and future documents may treat **DOA-FSN-001** as non-canonical or undefined, undermining the boundary model in **DOA-IDEA-004**.

## Alternatives considered

1. **Leave as informal convention** — rejected: perpetuates the governance gap and weakens “if not defined, it does not exist.”
2. **Fold `fixed_snapshot` into `implementation_snapshot`** — rejected: **DOA-IDEA-004** and **DOA-FSN-001** assign different roles — **implementation_snapshot** records execution/runs; **fixed_snapshot** declares **epoch boundaries** and **reference policy** between legacy and controlled zones.

## Decision

1. **`fixed_snapshot` is a first-class `doc_type`** in DocOps Agent.
2. **ID prefix:** **FSN** — canonical IDs: **`DOA-FSN-<NNN>`** (three-digit numeric suffix, same family pattern as other types).
3. **Storage:** canonical path prefix **`docs/fixed_snapshot/`** for `fixed_snapshot` Markdown artifacts.
4. **Nature of the type:**
   - **Boundary artifact** — declares system/corpus boundary state and rules between **legacy** and **controlled** phases.
   - **Immutable in place** — accepted snapshots are **not rewritten**; any material change requires a **new** `fixed_snapshot` document with a **new** ID (**create-only** evolution).
   - **Reference anchor** — the **sole sanctioned aggregate bridge** for controlled work to ground pre-boundary context, per **DOA-FSN-001** / **DOA-IDEA-004**.
5. **`fixed_snapshot` is an allowed `Parent` and reference target** for documents in the **controlled zone**, alongside other post-boundary artifacts permitted by boundary policy.

## Doc_type contract

| Aspect | `fixed_snapshot` | `implementation_snapshot` |
|--------|------------------|----------------------------|
| **Primary purpose** | Declare **boundary**, legacy vs controlled rules, and frozen **declarative** system/corpus understanding at a cut point | Record **what was executed**, tool runs, campaign steps, baselines for implementation |
| **Lifecycle** | New snapshot for each boundary revision; prior snapshots remain historical | New snapshot per execution slice / run as needed |
| **Immutability** | Accepted content is **stable**; corrections flow through **new** FSN docs | Same create-only discipline; focus is operational evidence |
| **Coupling to policy** | Tightly coupled to **reference boundary** and **zone** semantics | Coupled to **operational_plan** tasks and tooling outputs |
| **Typical Parent** | May reference **decision_log** or **idea_to_mvp** that authorized boundary approach (e.g. **DOA-DEC-045**, **DOA-IDEA-004**) | Often **operational_plan** or related planning artifact |

**Constraints**

- Do **not** use `fixed_snapshot` for routine implementation progress — use **`implementation_snapshot`**.
- Do **not** edit accepted `fixed_snapshot` bodies to “patch” state — author **DOA-FSN-00N+1** (or next free ID) and link forward.

## Consequences

### Positive

- **Closes the governance gap** around **DOA-FSN-001** and any future **DOA-FSN-*** artifacts.
- **Aligns** doc model, naming, and future **validator/gate** work with an explicit type.
- **Reduces policy drift** by making the type a first-class citizen of the documented system.

### Negative

- **Surface area increases** — another `doc_type` to teach, template, validate, and maintain.
- **Follow-on edits are required** in architecture and tooling artifacts (listed below); until done, some automation may still treat `fixed_snapshot` as unknown.

## Follow-ups

- Update **DOA-ARCH-008** — add **`fixed_snapshot` → FSN** to the doc_type ↔ TYPE mapping table and any validation narrative that lists supported types.
- Update **project governance / supported doc_types lists** (e.g. `.cursor/rules/docops-auto-doc.mdc` and any parallel canonical lists) to include **`fixed_snapshot`** and directory **`docs/fixed_snapshot/`**.
- Extend **validator** and **document gate** policy so **`fixed_snapshot`** is recognized, and (when dual-zone work lands) **legacy vs controlled** semantics can key off **DOA-FSN-*** boundaries.
- Define **fixed snapshot chain** — how a successor **DOA-FSN-002** supersedes or extends **DOA-FSN-001** (supersedes field, explicit “replaces” pattern, or operational plan slice) — in **architecture_draft** / **operational_plan** as appropriate.

## Traceability

- **Boundary artifact:** **DOA-FSN-001** — first `fixed_snapshot`; legitimized retroactively by this decision for governance purposes; content unchanged by this decision.
- **Policy:** **DOA-DEC-045** — snapshot-as-is over legacy.
- **Audit prompt / request:** **DOA-AUD-010** — external architecture audit after first snapshot.
- **Concept origin:** **DOA-IDEA-004** — `fixed_snapshot` + document index + reference boundary.
