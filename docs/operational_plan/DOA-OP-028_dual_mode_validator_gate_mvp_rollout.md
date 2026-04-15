# operational_plan — DOA-OP-028

## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-028
- Status: draft
- Date: 2026-04-18
- Parent: DOA-ARCH-021

_Create-only: new operational cycle — new OP document; extend via successor plans rather than rewriting closed work._

---

## Title / Summary

**MVP rollout — dual-mode validator and gate** for **legacy / boundary / controlled** zones: move from architecture contract (**DOA-ARCH-021**) plus Git boundary SoT (**DOA-DEC-047**) to a **working** pipeline that emits **zone-tagged findings**, a **controlled-only gate verdict**, **informational legacy aggregation**, and **reject-level** detection of **controlled → legacy** references. This plan does **not** replace **DOA-OP-026**; it opens a **new implementation phase** after **DOA-FSN-001**.

## Goal

Deliver a **minimal end-to-end** dual-mode behavior in the existing **validator → gate → JSON report** path so operators can:

1. Classify each scanned `docs/**/*.md` path as **`legacy`**, **`boundary`**, or **`controlled`** using **`boundary_commit`** and **`first_commit(path)`** per **DOA-DEC-047**.
2. See **legacy** findings **separately** and **not** have them **block** the **controlled-zone verdict** by default.
3. Fail the **controlled verdict** on **controlled → legacy** direct reference violations, per **DOA-FSN-001** / **DOA-ARCH-021**.

## Context

- **DOA-ARCH-021** defines the dual-mode architecture (classification, partitioned findings, gate semantics, reporting model).
- **DOA-DEC-047** fixes **Git** as the authoritative boundary mechanism; **DOA-DEC-046** formalizes **`fixed_snapshot`**; **DOA-FSN-001** states reference boundary rules; **DOA-DEC-045** explains snapshot-as-is posture over imperfect legacy.
- Prior validation campaign (**DOA-OP-026** / **DOA-OP-027**, **DOA-IMP-023–025**, `reports/doa_*_op027.md`) established inventory and metadata noise facts; dual-mode is the **control-plane** response so new work is not drowned by legacy.

## Scope

### In scope (MVP slice)

- **Git-based zone classification** integrated into the validator/gate pipeline (read `boundary_commit` from agreed policy source — initially constants aligned with **DOA-DEC-047**).
- **Zone context on every finding** (`legacy` / `boundary` / `controlled` source zone).
- **Partitioned aggregation** in gate: `legacy_findings`, `controlled_findings`, `cross_zone_violations`, and **`gate_status_controlled`**.
- **Default policy:** legacy-sourced findings are **informational** for `gate_status_controlled` unless **strict legacy audit mode** is explicitly enabled.
- **Cross-zone rule:** **controlled → legacy** reference ⇒ **error** / **REJECT** for `gate_status_controlled`.
- **Minimal machine-readable report** extensions (top-level fields or nested object) sufficient for consumers to read dual verdicts — **without** mandating a full schema rewrite beyond what is necessary.
- **First dual-mode dry run** on the repository and **one** `implementation_snapshot` recording the outcome.

### Non-goals

- **Document index** design or implementation.
- **Fixed snapshot chain** (`DOA-FSN-002+`) policy or automation.
- **Full legacy remediation** or mass metadata repair.
- **Complete validator redesign** unrelated to zone tagging, cross-zone detection, and gate partitioning.
- **Gate UI** redesign or new client features (thin shell work stays out unless already trivially compatible with new JSON).
- **Broad refactors** outside `scripts/doa_link_id_validator.py`, `scripts/doa_document_gate.py`, and narrowly related report types.

## Preconditions

- **DOA-ARCH-021** accepted as the architecture contract for this slice (this OP’s **Parent**).
- **DOA-DEC-047** boundary hash and classification rules treated as normative inputs for MVP constants/configuration.
- Non-shallow Git history available for authoritative classification runs (document in snapshot if CI uses shallow clones).

## Tasks

### T01 — Slice boundary and ownership

- **Description:** Freeze MVP scope textually (this OP + **DOA-ARCH-021** sections §Validator / §Gate / §Reporting); list files/components allowed to change (`validator`, `gate`, minimal report consumer docs if any).
- **Done when:** A short **“MVP touch list”** subsection exists in working notes or is appended to this OP’s execution notes (optional) — or team agreement recorded in **implementation_snapshot** at end.

### T02 — Git classification hook

- **Description:** Implement **`first_commit(path)`** and **`boundary_commit`** lookup in the validator pipeline; attach **`zone`** to each scanned path before rule evaluation.
- **Done when:** A dev run logs or prints **zone** for a sample of known paths (`legacy`, **DOA-FSN-001** as `boundary`, a post-047 file as `controlled`) matching **DOA-DEC-047**.

### T03 — Zone-tagged findings

- **Description:** Extend validator emission so every finding includes **`source_zone`** (and reserves fields for future `target_zone` where applicable).
- **Done when:** JSON output shows **`source_zone`** populated for an existing rule class (e.g. metadata) on both legacy and controlled files.

### T04 — Cross-zone reference rule

- **Description:** After link/ID resolution, if **source** is `controlled` and **resolved target** is `legacy`, emit dedicated **`cross_zone_violation`** finding at **error** severity.
- **Done when:** A synthetic or temporarily allowed test case (e.g. fixture branch or isolated test doc — removed before merge if policy forbids) demonstrates **one** deterministic violation; or a documented manual proof on a throwaway branch referenced in snapshot.

### T05 — Gate aggregation (controlled verdict)

- **Description:** Gate computes **`gate_status_controlled`** from **controlled** + **cross_zone** (+ **boundary** if needed) only; legacy bucket does not flip controlled verdict by default.
- **Done when:** A run with **only** legacy metadata gaps yields **`gate_status_controlled` = ACCEPT** while legacy section remains non-empty; a controlled metadata error still **REJECTs** controlled verdict.

### T06 — Report contract + first dual-mode run

- **Description:** Document minimal JSON fields for dual outputs; run gate in **dry-run** (or agreed safe mode) on `main` with new code; store report under `reports/` with a new distinctive name pattern (e.g. `doa_document_gate_run_*_dual.json`).
- **Done when:** At least **one** committed report artifact in `reports/` demonstrates partitioned findings + **`gate_status_controlled`**.

### T07 — Implementation snapshot

- **Description:** Record the first successful dual-mode run and pointers to artifacts in a new **`implementation_snapshot`** (create-only).
- **Done when:** **`DOA-IMP-*`** exists describing T02–T06 outcomes and links to the dual-mode report path(s).

## Done criteria

- [ ] **Classification:** For an agreed sample set, **zones** match **DOA-DEC-047** (including **`boundary`** for **DOA-FSN-001**).
- [ ] **Controlled verdict isolation:** **`gate_status_controlled`** exists and **ignores** legacy-only defects **by default**.
- [ ] **Visibility:** Legacy findings appear in a **separate** list/section in machine output (not silently dropped).
- [ ] **Enforcement:** A **controlled → legacy** reference produces a **cross_zone** finding that **forces** **`gate_status_controlled` = REJECT** (or equivalent terminal state per gate vocabulary).
- [ ] **Evidence:** At least **one** dual-mode gate/validator JSON artifact is committed under `reports/` **or** attached path is cited in **T07** snapshot if policy stores reports elsewhere.
- [ ] **Traceability:** **DOA-IMP-*** snapshot links **DOA-OP-028**, **DOA-ARCH-021**, **DOA-DEC-047**, **DOA-FSN-001**.

## Risks

- **Shallow CI clones** break `first_commit` — mitigate with documented CI settings or cached zone map follow-up.
- **False positives** in cross-zone detection if resolution misses aliases — mitigate with tests on known good controlled→boundary and controlled→controlled links.
- **Scope creep** into index or snapshot chain — blocked by Non-goals.

## Expected outputs

- Updated **validator/gate** behavior and **at least one** new **dual-mode** JSON report under `reports/`.
- **`implementation_snapshot`** capturing the first dual-mode rollout (**T07**).
- Optional short note in **README** / **WORKFLOW** only if already required by repo policy (not mandatory for this OP).

## Follow-up

- **Document index** rollout under separate **operational_plan** once index architecture is decided (**DOA-IDEA-004**).
- **DOA-OP-026** remaining tasks (naming T04, links T05, …) may proceed **in parallel** as hygiene/evidence — not prerequisites for dual-mode MVP if this OP’s Done criteria are met.
- Future **architecture_draft** only if gate/report schema needs a versioned bump beyond MVP minimal fields.

## Traceability

- **Implements:** **DOA-ARCH-021**
- **Depends on:** **DOA-DEC-047** (Git boundary), **DOA-DEC-046** (`fixed_snapshot` type), **DOA-FSN-001** (reference rules), **DOA-DEC-045** (legacy posture)
- **Related evidence:** **DOA-OP-026**, **DOA-OP-027**, **DOA-IMP-023–025**, `reports/doa_*_op027.md`
- **Does not replace:** **DOA-OP-026** — new phase after boundary
