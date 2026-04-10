# rules — overlay registry description

## Metadata

- Project: DocOps Agent
- Doc type: rules
- ID: DOA-RUL-001
- Status: draft
- Date: 2026-04-10
- Parent: DOA-OP-023

---

## What is overlay registry

Overlay registry is a small machine-readable layer that sits on top of existing documents and
adds explicit remediation hints for known canonical blockers under create-only constraints.

It does not rewrite historical documents. It records how specific issues are interpreted.

## Why it is needed

- Keep create-only discipline.
- Reduce blocker noise caused by legacy/canonical collisions.
- Make remediation explicit, traceable, and deterministic.

## JSON structure

File: `docs/rules/overlay_registry.json`

Top-level required fields:

- `schema`
- `version`
- `generated_at`

Sections:

- `mappings` — ID-level rules (for example duplicate ID handling).
- `parent_overrides` — parent link remediation for known missing/legacy references.
- `aliases` — optional alias declarations (empty in MVP).

## How to read mappings and parent_overrides

- `mappings`: each entry defines one explicit ID remediation rule, including reason/source/status.
- `parent_overrides`: each entry defines one explicit parent correction hint from original to resolved value.

Every rule must be explicit and traceable (`reason`, `source` where applicable). No implicit magic is allowed.

## Limitation

Overlay registry is mitigation only. It does not change history and does not replace canonical metadata
as source of truth for new documents.
