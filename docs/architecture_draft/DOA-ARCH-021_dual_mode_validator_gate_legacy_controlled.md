# architecture_draft — DOA-ARCH-021

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-021
- Status: draft
- Date: 2026-04-18
- Parent: DOA-DEC-047

---

## Title

Dual-mode validator and gate architecture for legacy vs controlled zones

## Overview

This document defines an **MVP control-plane architecture** for DocOps Agent after the first fixed snapshot (**DOA-FSN-001**): the **validator** and **document gate** operate in **dual mode**, classifying each Markdown path into **`legacy`**, **`boundary`**, or **`controlled`** using the **Git-based boundary model** (**DOA-DEC-047**), then applying **different policy semantics** so that:

- **legacy** noise does **not** mask **controlled** health by default, and  
- **controlled → legacy** direct references become **machine-detectable architectural violations** at **reject** severity.

The architecture is a **contract** for the next implementation phase. It does **not** prescribe code structure beyond responsibilities and reporting semantics.

## Problem

- A **boundary** exists (**DOA-FSN-001**) and **zone policy** is stated, but **validator/gate** historically treated the corpus **uniformly**.
- After **DOA-DEC-045** / **T03** evidence (`reports/doa_metadata_issues_t03_op027.md`), legacy metadata gaps produce **large blocking-equivalent noise**, obscuring whether **new controlled work** is healthy.
- Without zone-aware enforcement, the rule “**controlled MUST NOT reference legacy directly**” cannot be checked reliably — a core gap raised in **DOA-AUD-010**.

## Architectural goals

1. **Computability:** zone membership is derived from **Git** per **DOA-DEC-047**, not from informal prose.
2. **Signal separation:** gate output MUST expose a **controlled-zone verdict** distinct from legacy informational findings.
3. **Enforcement:** **controlled → legacy** reference violations MUST be **errors** that can fail the controlled gate.
4. **Pragmatism:** MVP scope — minimal modes, minimal new concepts, no full rewrite of legacy corpus.
5. **Compatibility:** remain aligned with **Policy Contract binding** philosophy (**DOA-ARCH-018** / **DOA-ARCH-020**): validator and gate still share one policy contract; this document adds **zone context** to interpretation, not a second policy source.

## Zone model

Three classes for every analyzed path `p` under configured roots (default: `docs/**/*.md`):

| Zone | Definition (normative) |
|------|-------------------------|
| **`legacy`** | `first_commit(p) ≺ boundary_commit` (strict ancestor), per **DOA-DEC-047** |
| **`boundary`** | `first_commit(p) == boundary_commit` **and** `p` is the designated **`DOA-FSN-001`** path |
| **`controlled`** | `boundary_commit ≺ first_commit(p)` **or** (`first_commit(p) == boundary_commit` **and** `p` is **not** the boundary file — rare; default controlled) |

**Active boundary:** for the current epoch, **`boundary_commit`** is the hash fixed in **DOA-DEC-047** (introducing **DOA-FSN-001**). Future **DOA-FSN-00N** epochs MUST declare their own `boundary_commit_N` in policy before tooling switches.

## Classification model

**Inputs**

- Repository Git history (non-shallow for authoritative runs; see Open questions).
- Resolved repository-relative paths for each file under scan.
- Optional cache file (implementation detail) MAY precompute `(path → zone)` for CI speed — cache MUST be reproducible from Git inputs.

**Output (per path)**

- `zone ∈ {legacy, boundary, controlled}`
- `first_commit` (OID) and `boundary_commit` (OID) for auditability in reports.

**Minimal processing flow**

1. Load active `boundary_commit` from policy (currently **DOA-DEC-047**).
2. For each candidate path `p`, compute `first_commit(p)`.
3. Assign `zone` using the Zone model table.
4. Run structural checks (metadata, links, IDs, …) as today, but **attach `zone` to every finding**.

**Example classification outcomes**

- `docs/decision_log/DOA-DEC-005.md` introduced before `boundary_commit` → **`legacy`**
- `docs/fixed_snapshot/DOA-FSN-001_boundary_pre_controlled_phase.md` introduced at `boundary_commit` → **`boundary`**
- `docs/decision_log/DOA-DEC-047_boundary_determination_git_model.md` introduced after `boundary_commit` → **`controlled`**

## Validator architecture

**Responsibilities**

1. **Classify** each scanned path into `legacy` / `boundary` / `controlled` before or alongside rule evaluation.
2. **Emit findings** with mandatory fields:
   - `finding.zone` — one of the three zones (source file zone).
   - `finding.rule_id` — unchanged from current validator vocabulary.
   - `finding.severity_base` — raw severity from rule.
3. **Evaluate cross-reference rules** using **target resolution**:
   - From a reference in source file `S`, resolve target artifact identity (canonical ID and/or path).
   - Classify target `T` zone.
4. **Emit boundary-rule findings** when `zone(S) == controlled` and reference targets `T` with `zone(T) == legacy`:
   - Dedicated rule family, e.g. `controlled_reference_to_legacy` — **error** (reject-level).

**Finding buckets (conceptual)**

- `legacy_findings` — `finding.zone == legacy` (and optionally legacy-targeted informational rules).
- `controlled_findings` — `finding.zone == controlled`.
- `boundary_findings` — violations tied to misuse of **boundary** artifacts (e.g., treating **DOA-FSN-001** as legacy target) — expected empty if classification is correct; still reserved for future boundary-chain rules.

## Gate architecture

**Responsibilities**

1. **Ingest** validator JSON (or equivalent structured stream) unchanged in schema version terms; **interpret** with zone context.
2. **Partition** findings into `legacy_findings`, `controlled_findings`, `boundary_findings`, and **`cross_zone`** (reference violations where source is controlled and target legacy).
3. **Compute verdicts**
   - **`gate_status_controlled`**: derived **only** from `controlled_findings` ∪ `cross_zone` (and optional `boundary_findings` if any are defined as blocking — default: **cross_zone** is blocking; ordinary `boundary` zone file issues should be none if boundary file is clean).
   - **`gate_status_overall`** (optional but recommended): MAY include informational legacy summary without failing controlled health.

**Default aggregation policy (MVP)**

- **`legacy_findings`**: **informational** for `gate_status_controlled` — they **MUST NOT** flip controlled verdict to **REJECT** unless an explicit **“strict legacy audit mode”** flag is enabled.
- **`controlled_findings`**: existing severity mapping applies unchanged for controlled health.
- **`cross_zone` (controlled → legacy reference)**: **REJECT** for `gate_status_controlled`.

**Example gate behaviors**

1. **Only legacy metadata missing** in legacy files → `gate_status_controlled` = **ACCEPT** (or **ACCEPT_WITH_WARNINGS** if controlled files have only infos), legacy section lists noise.
2. **Controlled file missing required metadata** → `gate_status_controlled` = **REJECT** (blocking controlled defect).
3. **Controlled file links directly to legacy DEC** → `cross_zone` violation → `gate_status_controlled` = **REJECT**.

## Boundary enforcement model

### Rule

A **`controlled`** document **MUST NOT** reference any **`legacy`** document **directly** (normative dependency links / canonical ID references as defined by the link contract — same resolution rules the validator already uses for ID/path integrity).

### Permitted references from controlled

- **`boundary`**: **DOA-FSN-001** (and future designated boundary files for an epoch).
- **`controlled`**: any post-boundary artifact with `zone == controlled` (and the boundary exception above).

### Enforcement basis

- **Source zone** from classification of the referencing file.
- **Target zone** from classification of the resolved target artifact.
- Violation when `zone(source) == controlled` **and** `zone(target) == legacy`.

### Severity

- **Error / reject-level** for `gate_status_controlled` (architectural violation).

## Reporting model

Gate and validator reports SHOULD expose (names indicative; exact JSON keys are implementation):

| Aggregate | Meaning |
|-----------|---------|
| `legacy_findings[]` | Issues whose **source** path is `legacy` |
| `controlled_findings[]` | Issues whose **source** path is `controlled` |
| `boundary_findings[]` | Issues tied to boundary artifact misuse (reserved / usually empty in MVP) |
| `cross_zone_violations[]` | Controlled → legacy reference violations |
| `gate_status_controlled` | Verdict for forward work health |
| `gate_status_overall` | Optional umbrella including informational legacy posture |

**UI / human operator story:** show **controlled verdict prominently**; collapse legacy findings under an **informational** fold unless auditing legacy.

## Relationship to document index

- **Document index** (**DOA-IDEA-004**) remains a **follow-on** artifact for explicit existence and managed prompt scope.
- **Dual-mode validator/gate** SHOULD be designed **now** without waiting for the index: Git classification is sufficient for MVP zone split.
- When an index exists, it **augments** scope selection and existence checks but **does not replace** Git boundary classification (**DOA-DEC-047**).

## Non-goals

- Implementing or modifying **validator code**, **gate code**, or CI wiring in this document.
- Defining **document index** schema or ingestion protocol.
- Defining **fixed snapshot chain** mechanics beyond acknowledging future `boundary_commit_N`.
- Mandating **full legacy remediation** or bulk edits to historical Markdown.

## Risks

- **Git assumptions:** shallow clones, rewritten history, or non-linear workflows can break `first_commit` / ancestor logic — operational risk, not a reason to abandon Git SoT, but MUST be documented for runners.
- **False negatives in reference detection:** if link resolution is incomplete, boundary violations could slip through — mitigation belongs to implementation but the architecture assumes **the same resolution pipeline** as current link checks.
- **Dual policy complexity:** operators must understand two verdicts — training and report UX become part of adoption cost.

## Open questions

- Whether **merge commits** require **first-parent** traversal only for `first_commit` stability across branches (**DOA-DEC-047** leaves operational detail open).
- How **overlay / alias registries** (if any) interact with **zone** of resolved targets — MUST NOT bypass legacy classification without explicit policy.
- Whether a **cached zone map** file in `reports/` becomes a required companion artifact for reproducible CI — architecture allows, does not mandate.

## Traceability

- **Boundary semantics:** **DOA-FSN-001**
- **Snapshot-as-is policy:** **DOA-DEC-045**
- **Formal doc_type:** **DOA-DEC-046**
- **Git boundary SoT:** **DOA-DEC-047** (**Parent** of this draft)
- **Audit driver:** **DOA-AUD-010**
- **Concept:** **DOA-IDEA-004**
- **Evidence chain:** **DOA-OP-026**, **DOA-OP-027**, **DOA-IMP-023–025**, `reports/doa_*_op027.md`
