## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-047
- Status: accepted
- Date: 2026-04-18
- Parent: DOA-DEC-046

---

## Title

Define boundary determination model for fixed_snapshot (Git-based)

## Context

- **DOA-FSN-001** introduces the first documentation boundary between **legacy** and **controlled** zones, with strict reference rules.
- **DOA-DEC-046** formalizes **`fixed_snapshot`** as a first-class `doc_type` (**FSN** prefix, `docs/fixed_snapshot/`).
- **DOA-AUD-010** (external architecture audit request) highlights that “**created after** the snapshot” is **not machine-checkable** without a defined source of truth — blocking validator/gate enforcement of controlled→legacy reference rules.

## Problem

- The boundary is **declared in prose** but **not computable**, so tooling cannot reliably classify documents.
- **Validator / gate** cannot separate **legacy** vs **controlled** behavior → noisy or misleading reports and **no** reliable path to enforce “controlled **must not** reference legacy.”
- **Reference rules** from **DOA-FSN-001** / **DOA-IDEA-004** risk becoming **policy drift** if humans interpret “created after” differently than automation.

## Alternatives considered

1. **Metadata `Date` on documents** — rejected: not authoritative for “first existence,” can be inconsistent with actual introduction order, and may be edited in ways that break auditability.
2. **Document index only** — rejected for **primary** boundary: the index is not yet implemented (**DOA-IDEA-004**); it cannot be the sole truth for classifying the existing tree at introduction time.
3. **Git commit graph as boundary** — **chosen:** immutable, replayable, independent of in-file metadata, aligned with repository as source of truth.

## Decision

### 1. Boundary definition

The **boundary** for the first fixed snapshot is the **Git commit** that introduced **`DOA-FSN-001`** into the canonical repository history used for validation (default: `main` / repository HEAD history as configured by the gate).

**Recorded boundary commit (repository fact at decision time):**

```text
boundary_commit = d94a7d7b9751309ffbd55dd71614e25071c08c8a
```

This commit is the one returned by:

`git log -1 --format=%H -- docs/fixed_snapshot/DOA-FSN-001_boundary_pre_controlled_phase.md`

Future fixed snapshots (**DOA-FSN-002**, …) define their own **`boundary_commit_N`** by the same rule: the commit hash that introduces that snapshot file.

### 2. Zone classification (per path)

For each tracked Markdown path under the validation roots (initially `docs/**/*.md` unless policy narrows scope), determine **`first_commit(path)`**: the **earliest** commit in the evaluated branch history where that path exists.

Let **Git partial order** be used: write **`A ≺ B`** when **`A` is a strict ancestor of `B`** (equivalently: `B` is a strict descendant of `A`).

```text
legacy_zone(path):
  first_commit(path) ≺ boundary_commit

controlled_zone(path):
  boundary_commit ≺ first_commit(path)

boundary_artifact(path):
  first_commit(path) == boundary_commit
  AND path == docs/fixed_snapshot/DOA-FSN-001_boundary_pre_controlled_phase.md
```

**Notes**

- **`boundary_artifact`** is **not** `legacy_zone` for reference enforcement: controlled documents **may** cite **DOA-FSN-001** as the sanctioned bridge (**DOA-FSN-001**, **DOA-IDEA-004**).
- Any other path with `first_commit(path) == boundary_commit` is treated as **`controlled_zone`** by default (same commit as boundary landing; exceptional cases only by future **decision_log**).

### 3. Source of truth

- **Git history** is the **authoritative** source for **boundary_commit** and **`first_commit(path)`** classification.
- **In-document metadata** does **not** define zone membership for enforcement (metadata remains required for controlled authoring quality, but not for computing the epoch).

### 4. Relationship to document index (forward compatibility)

- A future **document index** may list **controlled** documents, constrain validation scope, and speed lookups.
- The index **does not replace** Git-based boundary classification; it **layers** on top for operational convenience and “existence” rules (**DOA-IDEA-004**).

### 5. Validator / gate implications

- Validator and gate **must** be able to classify each analyzed path into **`legacy` / `boundary` / `controlled`** using Git history relative to the active **`boundary_commit`** for the epoch (initially the hash in §1).
- **Policy split (dual-mode):**
  - **legacy** findings: default to **informational / suppressed** in gate “blocking” aggregation unless explicitly running a **legacy audit mode**.
  - **controlled** findings: **strict** enforcement remains the default for controlled-zone health.

### 6. Reference enforcement model

```text
A controlled document MUST NOT reference (by canonical ID / path rules)
any document classified as legacy_zone for the active boundary_commit.
```

- **Permitted:** references to **boundary** artifacts (e.g., **DOA-FSN-001**) and other **controlled** documents, per **DOA-FSN-001** / **DOA-IDEA-004**.
- **Enforcement expectation:** **machine-checkable**, based on **resolved link targets** + **Git classification** of targets.

## Consequences

### Positive

- The boundary becomes **computable** and **replayable** from repository facts.
- Validator/gate can implement **dual-mode** behavior without ambiguous “created after” language.
- Reduces **policy drift** between humans and automation.

### Negative

- **Hard dependency on Git** metadata availability (history, shallow clones, rewritten history would be architecturally hostile — out of scope here but a real operational constraint).
- Validator/gate integration requires **Git-aware** classification (higher implementation complexity than metadata-only heuristics).
- Local checks without Git context are **incomplete** unless they fetch history or consume a precomputed classification artifact.

## Follow-ups

- Implement **Git-based classification** in the link/ID validator and/or gate configuration for DocOps Agent.
- Update **document gate** to aggregate **controlled** vs **legacy** severities separately (dual-mode reporting).
- When the **document index** exists: store **controlled** membership and optional cached **`first_commit(path)`** for performance — **not** as a replacement for Git truth.
- Consider **caching** classification results in CI artifacts for speed and reproducibility.

## Traceability

- **DOA-FSN-001** — first boundary; supplies semantic boundary rules paired with this computational model.
- **DOA-DEC-045** — snapshot-as-is policy context.
- **DOA-DEC-046** — formal `fixed_snapshot` doc_type (Parent of this decision).
- **DOA-AUD-010** — audit request surfacing “created after” ambiguity.
- **DOA-IDEA-004** — conceptual model: snapshot + index + reference boundary.
