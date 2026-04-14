# Report Generator Output

## summary

- **gate_status** (from gate JSON): `REJECT`
- **gate counts** (from gate JSON): `{"error": 7, "info": 0, "total": 52, "warn": 45}`
- **validator counts** (from validator JSON): `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}`
- **traceability**: values above are copied from the cited JSON inputs; this file is not a canonical DocOps document.

## state by doc_type

doc_type aggregation **unavailable** from current inputs (no `doc_type` field on finding rows in validator or gate payloads).

## risks

- From **gate** `counts`: error=7, warn=45, info=0 (as reported in input JSON).
- From **validator** `counts`: `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}`.

## next steps

- Re-run validator and gate to refresh inputs, then regenerate this report.
- When implementing later tasks (T04+), add deterministic traceability and DoD checks.

## provenance

- **report generated at (UTC)**: `2026-04-14T03:04:27Z`
- **validator input path**: `D:/Work/DocOp/Project/reports/doa_link_id_validator_run_001.json`
- **gate input path**: `D:/Work/DocOp/Project/reports/doa_document_gate_run_001.json`
- **generator version**: `doa-report-generator/0.1.0-mvp`
- **gate engine_version** (from gate JSON): `0.1.0`
- **gate policy_version** (from gate JSON): `doa-gate-policy/1`
- **validator engine version** (from validator JSON): `0.1.0`
- **gate.generated_at_utc** (from gate JSON): `2026-04-10T07:25:19Z`
- **validator.generated_at_utc** (from validator JSON): `2026-04-10T08:35:19Z`
- **gate.repo_root** (from gate JSON): `D:\Work\DocOp\Project`
- **validator.root** (from validator JSON): `D:\Work\DocOp\Project`
