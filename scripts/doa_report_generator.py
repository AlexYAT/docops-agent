#!/usr/bin/env python3
"""
MVP Report Generator (DOA-OP-021 T01–T03).

Loads validator + gate JSON reports, extracts deterministic fields only,
writes a markdown report with fixed sections. No NLP, no policy logic.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENERATOR_VERSION = "doa-report-generator/0.1.0-mvp"


def load_json(path: Path) -> dict[str, Any]:
    """T01: load a single JSON file; exit on missing file or invalid JSON."""
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        # utf-8-sig strips a leading BOM if present (some reports are utf-8-sig).
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        print(f"error: cannot read file {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print(f"error: expected JSON object at top level in {path}", file=sys.stderr)
        sys.exit(1)
    return data


def _get_counts(obj: dict[str, Any]) -> dict[str, Any]:
    raw = obj.get("counts")
    return raw if isinstance(raw, dict) else {}


def parse_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """T02: extract gate fields when present."""
    findings = gate.get("findings")
    if not isinstance(findings, list):
        findings = []
    return {
        "gate_status": gate.get("gate_status"),
        "counts": _get_counts(gate),
        "findings": findings,
        "engine_version": gate.get("engine_version"),
        "policy_version": gate.get("policy_version"),
        "generated_at_utc": gate.get("generated_at_utc"),
        "repo_root": gate.get("repo_root"),
    }


def parse_validator(val: dict[str, Any]) -> dict[str, Any]:
    """T02: extract validator fields when present."""
    canon = val.get("canonical_violations")
    if not isinstance(canon, list):
        canon = []
    legacy = val.get("legacy_findings")
    if not isinstance(legacy, list):
        legacy = []
    vmeta = val.get("validator")
    if not isinstance(vmeta, dict):
        vmeta = {}
    return {
        "validator_meta": vmeta,
        "counts": _get_counts(val),
        "canonical_violations": canon,
        "legacy_findings": legacy,
        "generated_at_utc": val.get("generated_at_utc"),
        "root": val.get("root"),
        "scope": val.get("scope"),
    }


def _finding_rows_have_doc_type(rows: list[Any]) -> bool:
    for row in rows:
        if isinstance(row, dict) and row.get("doc_type") is not None:
            return True
    return False


def _aggregate_doc_type(rows: list[Any]) -> dict[str, int]:
    """Only counts rows that already contain a doc_type field."""
    ctr: Counter[str] = Counter()
    for row in rows:
        if not isinstance(row, dict):
            continue
        dt = row.get("doc_type")
        if dt is None or dt == "":
            continue
        ctr[str(dt)] += 1
    return dict(ctr)


def doc_type_from_inputs(gate_p: dict[str, Any], val_p: dict[str, Any]) -> tuple[bool, dict[str, int]]:
    """
    If any finding-like row includes doc_type, aggregate counts.
    Otherwise (False, {}).
    """
    rows: list[Any] = []
    rows.extend(gate_p.get("findings") or [])
    rows.extend(val_p.get("canonical_violations") or [])
    rows.extend(val_p.get("legacy_findings") or [])
    if not _finding_rows_have_doc_type(rows):
        return False, {}
    return True, _aggregate_doc_type(rows)


def build_markdown(
    gate_p: dict[str, Any],
    val_p: dict[str, Any],
    validator_path: Path,
    gate_path: Path,
    generated_ts: str,
    doc_type_ok: bool,
    doc_type_counts: dict[str, int],
) -> str:
    """T03: fixed section layout; deterministic text only."""
    lines: list[str] = []
    lines.append("# Report Generator Output")
    lines.append("")
    lines.append("## summary")
    lines.append("")
    gs = gate_p.get("gate_status")
    gc = gate_p.get("counts") or {}
    vc = val_p.get("counts") or {}
    lines.append(f"- **gate_status** (from gate JSON): `{gs}`")
    lines.append(f"- **gate counts** (from gate JSON): `{json.dumps(gc, sort_keys=True, ensure_ascii=False)}`")
    lines.append(f"- **validator counts** (from validator JSON): `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}`")
    lines.append(
        "- **traceability**: values above are copied from the cited JSON inputs; "
        "this file is not a canonical DocOps document."
    )
    lines.append("")
    lines.append("## state by doc_type")
    lines.append("")
    if not doc_type_ok:
        lines.append(
            "doc_type aggregation **unavailable** from current inputs "
            "(no `doc_type` field on finding rows in validator or gate payloads)."
        )
    else:
        lines.append("Aggregated counts where `doc_type` was present on finding rows:")
        for k in sorted(doc_type_counts.keys()):
            lines.append(f"- `{k}`: {doc_type_counts[k]}")
    lines.append("")
    lines.append("## risks")
    lines.append("")
    # Explicitly observed from numeric / severity fields only
    ge = gc.get("error")
    gw = gc.get("warn")
    gi = gc.get("info")
    lines.append(
        f"- From **gate** `counts`: error={ge}, warn={gw}, info={gi} (as reported in input JSON)."
    )
    if isinstance(vc, dict) and vc:
        lines.append(f"- From **validator** `counts`: `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}`.")
    lines.append("")
    lines.append("## next steps")
    lines.append("")
    lines.append("- Re-run validator and gate to refresh inputs, then regenerate this report.")
    lines.append("- When implementing later tasks (T04+), add deterministic traceability and DoD checks.")
    lines.append("")
    lines.append("## provenance")
    lines.append("")
    lines.append(f"- **report generated at (UTC)**: `{generated_ts}`")
    lines.append(f"- **validator input path**: `{validator_path.as_posix()}`")
    lines.append(f"- **gate input path**: `{gate_path.as_posix()}`")
    lines.append(f"- **generator version**: `{GENERATOR_VERSION}`")
    ev = gate_p.get("engine_version")
    pv = gate_p.get("policy_version")
    if ev is not None:
        lines.append(f"- **gate engine_version** (from gate JSON): `{ev}`")
    if pv is not None:
        lines.append(f"- **gate policy_version** (from gate JSON): `{pv}`")
    vm = val_p.get("validator_meta") or {}
    if isinstance(vm, dict) and vm.get("version") is not None:
        lines.append(f"- **validator engine version** (from validator JSON): `{vm.get('version')}`")
    if gate_p.get("generated_at_utc") is not None:
        lines.append(f"- **gate.generated_at_utc** (from gate JSON): `{gate_p.get('generated_at_utc')}`")
    if val_p.get("generated_at_utc") is not None:
        lines.append(f"- **validator.generated_at_utc** (from validator JSON): `{val_p.get('generated_at_utc')}`")
    if gate_p.get("repo_root") is not None:
        lines.append(f"- **gate.repo_root** (from gate JSON): `{gate_p.get('repo_root')}`")
    if val_p.get("root") is not None:
        lines.append(f"- **validator.root** (from validator JSON): `{val_p.get('root')}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="DOA MVP report generator (T01–T03).")
    parser.add_argument("--validator", type=Path, required=True, help="Path to validator JSON report")
    parser.add_argument("--gate", type=Path, required=True, help="Path to gate JSON report")
    parser.add_argument("--out", type=Path, required=True, help="Output markdown path")
    args = parser.parse_args()

    validator_path = args.validator.resolve()
    gate_path = args.gate.resolve()
    out_path = args.out.resolve()

    val_raw = load_json(validator_path)
    gate_raw = load_json(gate_path)

    gate_p = parse_gate(gate_raw)
    val_p = parse_validator(val_raw)
    doc_type_ok, doc_type_counts = doc_type_from_inputs(gate_p, val_p)

    gen_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = build_markdown(
        gate_p,
        val_p,
        validator_path,
        gate_path,
        gen_ts,
        doc_type_ok,
        doc_type_counts,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_path.write_text(md, encoding="utf-8", newline="\n")
    except OSError as exc:
        print(f"error: cannot write {out_path}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
