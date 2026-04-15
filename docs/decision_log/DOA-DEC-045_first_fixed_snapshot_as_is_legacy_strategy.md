## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-045
- Status: accepted
- Date: 2026-04-16
- Parent: DOA-IDEA-004

---

## Title

Legacy corpus handling before the first fixed snapshot: snapshot-as-is strategy

## Context

- **DOA-IDEA-004** defines **fixed_snapshot** as a separate `doc_type`, a **reference boundary** after snapshot creation, and a **document index** as the existence rule for controlled work.
- **DOA-OP-026** / **DOA-OP-027** drove a validation campaign; **T03** is recorded in **DOA-IMP-025** with evidence in **`reports/doa_metadata_issues_t03_op027.md`**.
- T03 facts (frozen corpus **125** paths): **45** blocking issue rows, **0** deferred, **81** clean paths, **44** paths with at least one issue — dominated by legacy files **without** a `## Metadata` section, plus isolated structural cases (e.g. **DOA-DEC-027** non-canonical keys, **`docs/implementation_snapshot/DOA-OP-017.md`** without metadata).

## Problem

- A large share of the **historical** corpus does **not** meet current metadata expectations.
- If **full remediation** of that legacy layer were treated as a **hard prerequisite** for authoring the **first fixed snapshot**, boundary creation could be **blocked indefinitely** by retroactive cleanup work.
- The system still needs a **practical path** into a **controlled** post-boundary mode **without** rewriting the entire pre-boundary history (**create-only** discipline).

## Options considered

### Option A — Full remediation before the first fixed snapshot

Normalize metadata (and related canon) across the whole legacy corpus, **then** create the first fixed snapshot.

### Option B — First fixed snapshot as-is over the current validated understanding

Create the first fixed snapshot **on top of** the present corpus, with **explicit** declaration of legacy limitations and gaps in the snapshot itself.

### Option C — Partial minimum remediation before snapshot

Fix only a **minimal** subset of legacy documents, then snapshot.

## Decision

**Adopt Option B — first fixed snapshot as-is over the current validated understanding.**

- **No** requirement for **complete** legacy metadata remediation **before** the first fixed snapshot.
- Legacy **does not** block **boundary creation**; it remains a **historical / pre-boundary** layer whose defects are **honestly recorded**.
- After the snapshot, **strict reference rules** apply to **new** work as described in **DOA-IDEA-004** (new documents reference **only** the fixed snapshot and post-snapshot artifacts, **not** direct legacy targets).

## Why

- Matches the **role** of **fixed_snapshot** as a **boundary artifact**, not a retroactive rewrite of history.
- Preserves **create-only**: avoids mass-editing legacy files as a gate for progress.
- Makes the **transition practically achievable** and reduces the risk of an endless **pre-snapshot cleanup** phase.
- Aligns with **DOA-IMP-025** / **`reports/doa_metadata_issues_t03_op027.md`**: the corpus is **known-imperfect** but **fully inventoried and reviewed** for this decision.

## Consequences

- The **legacy corpus** stays in place as a **historical zone** with **documented** defects (including T03 blocking rows where they remain unaddressed).
- The **first fixed snapshot** **must** **declaratively** capture limitations, **known gaps**, and any material constraints implied by that legacy state (per **DOA-IDEA-004**).
- **Post-snapshot** documents **must not** **directly** link into the legacy zone; the snapshot is the **only sanctioned bridge** for understanding pre-boundary context.
- **Legacy remediation** may continue **later** but is **not** a **prerequisite** for creating the **first** fixed snapshot.

## Trade-offs

- The first snapshot **does not** assert a “fully clean” historical corpus — it asserts a **boundary** and an **honest state description**.
- **Validator / gate semantics** for **legacy vs post-snapshot** zones will need **distinct** treatment in future **architecture_draft** work (not decided here).
- Some **machine checks** may remain noisy against legacy paths until policy and tooling explicitly separate **pre-boundary** vs **controlled** behavior.

## Follow-ups

- Continue **DOA-OP-026** execution slices (e.g. naming, links, legacy classification) **as preparation and evidence**, not as a hard gate blocking snapshot authoring under this decision.
- Author the **first `fixed_snapshot`** artifact when ready, **explicitly** incorporating T03/T02 artifacts and this decision in its declarative content.
- Architecture work: formalize **legacy zone / controlled zone / document index** rules and validator–gate behavior under the boundary model (**DOA-IDEA-004**).
