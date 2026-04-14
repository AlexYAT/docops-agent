# Decision: DOA-DEC-039

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-039
- Status: draft
- Date: 2026-04-14
- Parent: DOA-ARCH-019

---

## Title

Machine-verifiable Definition of Done for Report Generator MVP

## Context

The Report Generator MVP is defined architecturally (`DOA-ARCH-017`, `DOA-ARCH-019`). Prior wording tied “human-readable report” to outcomes that are hard to verify mechanically. A **decision** is required to adopt a **Definition of Done** that is **objectively checkable** and does not depend on subjective quality of prose.

## Problem

- Subjective DoD (“clear”, “useful”, “well written”) cannot be enforced in CI or automated checks.
- Without verifiable criteria, report output may drift into narrative that is not traceable to canonical documents or to validator/gate outputs.
- The repository needs a single agreed bar for “MVP report generator done” that aligns with anti-SoT rules for reports.

## Options considered

1. **Subjective DoD** — retain human-judged readability as the primary gate. Rejected: not machine-verifiable.
2. **Hybrid DoD** — mix mechanical checks with a human sign-off on wording. Rejected for MVP bar: the subjective part remains non-automatable as a hard criterion.
3. **Machine-verifiable DoD only** — define completion solely through checks that can be implemented as deterministic predicates over artifacts and inputs. **Chosen.**

## Chosen solution

Adopt a **machine-verifiable Definition of Done** for the Report Generator MVP. Satisfaction of DoD **must** be determined only by the criteria listed in “Machine-verifiable DoD criteria”. No additional subjective criteria **may** be required for declaring MVP compliance.

## Machine-verifiable DoD criteria

The MVP Report Generator run **must** be considered DoD-satisfied **if and only if** all of the following hold:

1. **Generation completed without error** — the generation process terminates in a success state (no uncaught failure / non-zero exit semantics as defined for that process, when checks are automated).
2. **Required sections present** — the output contains, with recognizable section boundaries per the minimal schema in `DOA-ARCH-019`, each of: `summary`, `state by doc_type`, `risks`, `next steps`, `provenance`.
3. **Provenance block present** — the `provenance` section includes all mandatory fields defined in `DOA-ARCH-019`: generated timestamp, source scope, source commit (or equivalent), generator/version reference.
4. **Traceability of factual statements** — every statement that asserts a fact about the repository (existence of a document, status value, relationship, gate/validator outcome, counts, file paths) **must** be accompanied by an explicit trace to either:
   - one or more canonical document IDs (`DOA-*` file references as defined by repository rules), or  
   - derived content explicitly labeled as coming from a specified validator or gate output, with that output identified in provenance or an unambiguous pointer included in the report body.
5. **No forbidden references** — the output **must not** contain `Parent:` or `Replaces:` (or equivalent DocOps metadata fields) targeting the report as a canonical document; **must not** declare the report as a `doc_type` under `docs/`; **must not** assert normative policy not present in cited canonical architecture or decision documents.
6. **No report-only facts** — the output **must not** introduce factual claims that cannot be traced as in criterion 4 (i.e. no free-standing facts originating only in the report narrative).

Deterministic checkers **may** use parsing, pattern matching, and reference validation against repository paths and `DOA-*` identifiers; they **must not** require natural-language understanding of “quality”.

## Rejected criteria

The following **must not** be used as mandatory DoD conditions for the MVP:

- “Useful enough” for stakeholders.
- “Looks good” or visual/layout approval.
- “Well written”, “clear”, “readable”, or other subjective readability judgments.
- Informal “LGTM” without reference to the verifiable checklist above.

## Why

- Objective criteria align with gate/validator philosophy and future automation.
- Traceability rules reinforce that reports are **not** SoT (`DOA-ARCH-019`).
- Removing subjective wording avoids blocking releases on non-reproducible judgment.

## Consequences

- Human readability remains a **product goal**, not a **hard DoD** requirement for MVP compliance.
- Teams **must** invest in mechanical checks (schema, provenance, reference lint) rather than editorial review as the compliance gate.
- Documentation and training **should** separate “good narrative” from “DoD satisfied”.

## Trade-offs

- **Gain:** repeatable, auditable MVP completion.
- **Loss:** a report can pass DoD while still being awkward or dense for humans.
- **Mitigation (non-DoD):** editorial improvement and UX work remain optional quality work outside the verifiable bar.

## Follow-ups

- Align validator rules with traceability and forbidden-reference checks for generated report artifacts (when such artifacts are in scope for validation).
- Align Document Gate policy with treating report outputs as non-canonical and excluding them from doc graph rules for `Parent` / `Replaces`.
- Revisit DoD when a future decision extends MVP or adds optional human-readability gates **as non-blocking** quality metrics.

## Links

- `DOA-ARCH-019` — Report Layer invariants and minimal report schema (provenance, sections, failure conditions).
- `DOA-ARCH-017` — Report Generator MVP architecture.
- `DOA-ARCH-016`, `DOA-DEC-038` — Report Layer and prior DoD framing (human-facing); superseded **only for the MVP DoD bar** by the verifiable criteria in this decision, where they conflict on measurability.
