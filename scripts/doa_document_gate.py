#!/usr/bin/env python3
"""
DocOps Document Gate MVP (DOA-OP-020) — CLI, validator adapter, policy (T01–T04).

Does not implement document checks; delegates to scripts/doa_link_id_validator.py.
Semantic autofix is not implemented.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GATE_REPORT_SCHEMA = "doa-gate-report/1+dual_mode_mvp"
DEFAULT_POLICY_VERSION = "doa-gate-policy/1"
VALID_SEVERITIES = frozenset({"error", "warn", "info"})
CLOSURE_CONTRACT_VERSION = "closure/1"
closure_semantics_enabled = True
M1_SUCCESSOR_ACTIVATION_CATEGORIES = frozenset(
    {"noncanonical_doc_type_key", "invalid_replaces_format"}
)


def run_validator(root_path: str | Path) -> dict[str, Any]:
    """
    Execute doa_link_id_validator.py as subprocess and return parsed JSON report.

    The validator resolves its own ROOT from __file__; root_path must be the
    repository root containing scripts/doa_link_id_validator.py.
    """
    root = Path(root_path).resolve()
    script = root / "scripts" / "doa_link_id_validator.py"
    if not script.is_file():
        raise FileNotFoundError(
            f"Validator not found at {script} (is --root the repo root?)"
        )

    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if proc.returncode != 0:
        raise RuntimeError(
            f"Validator exited with code {proc.returncode}; "
            f"stderr: {proc.stderr.strip() or '(empty)'}"
        )

    raw = proc.stdout.strip()
    if not raw:
        raise RuntimeError(
            "Validator produced empty stdout; stderr: "
            + (proc.stderr.strip() or "(empty)")
        )

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Validator stdout is not valid JSON: {e}\n"
            f"stderr: {proc.stderr.strip() or '(empty)'}"
        ) from e


def normalize_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Flatten canonical_violations and legacy_findings into a uniform list.

    Each item: type (category), severity from engine or None, file, details,
    engine_mode (canonical | legacy | root_link), plus optional overlay markers.
    """
    out: list[dict[str, Any]] = []

    def _one(default_mode: str, item: dict[str, Any]) -> None:
        category = item.get("category") or default_mode
        sev = item.get("severity")
        if sev is not None:
            sev = str(sev).lower()

        engine_mode = item.get("mode") or default_mode

        f = item.get("file")
        if f is None and item.get("files"):
            f = "; ".join(str(p) for p in item["files"])

        detail_parts: list[str] = []
        if item.get("detail") is not None:
            detail_parts.append(str(item["detail"]))
        if item.get("files"):
            detail_parts.append("files: " + ", ".join(str(x) for x in item["files"]))
        details = "; ".join(detail_parts) if detail_parts else None

        out.append(
            {
                "type": str(category),
                "severity": sev,
                "file": str(f) if f is not None else None,
                "details": details,
                "engine_mode": engine_mode,
                "source_zone": item.get("source_zone"),
                "target_zone": item.get("target_zone"),
                "resolution_status": item.get("resolution_status", "none"),
                "resolution_source": item.get("resolution_source", "none"),
                "trace_reference": item.get("trace_reference"),
                "closure_contract_version": item.get(
                    "closure_contract_version", CLOSURE_CONTRACT_VERSION
                ),
                "overlay_source": item.get("overlay_source"),
                "overlay_rule_type": item.get("overlay_rule_type"),
            }
        )

    for item in report.get("canonical_violations") or []:
        _one("canonical", item)
    for item in report.get("legacy_findings") or []:
        _one("legacy", item)
    for item in report.get("cross_zone_violations") or []:
        _one("cross_zone", item)

    return out


def assign_severity(finding: dict[str, Any], policy: dict[str, Any] | None) -> str:
    """
    Resolve final severity for one finding: overlay handling, engine value,
    policy override, or defaults.

    Default mapping when engine omits severity (DOA-DEC-032 aligned):
    - mode canonical -> error
    - mode legacy -> warn
    - mode root_link:
        - category broken_markdown_link -> warn
        - other root_link (e.g. markdown_link_escape, informational notes) -> info

    Optional policy JSON keys:
    - version: str (reported as policy_version)
    - category_overrides: { "<category>": "error"|"warn"|"info" }
    """
    # Overlay-aware MVP rule (OP-023 T05):
    # findings already resolved via overlay are downgraded to informational.
    if finding.get("resolution_status") == "resolved_via_overlay":
        return "info"

    raw = finding.get("severity")
    if raw is not None:
        s = str(raw).lower()
        if s in VALID_SEVERITIES:
            return s

    cat = finding.get("type") or ""
    if cat == "controlled_reference_to_legacy":
        return "error"

    pol = policy or {}
    overrides = pol.get("category_overrides") or {}
    if cat in overrides:
        o = str(overrides[cat]).lower()
        if o in VALID_SEVERITIES:
            return o

    mode = finding.get("engine_mode") or "legacy"
    if mode == "canonical":
        return "error"
    if mode == "root_link":
        if cat == "broken_markdown_link":
            return "warn"
        return "info"
    return "warn"


def apply_closure_activation(
    finding: dict[str, Any], assigned_severity: str
) -> tuple[str, str, str, Any]:
    """
    T07 activation (category-scoped MVP):
    only M1 categories can be interpreted as resolved via successor activation.
    """
    status = str(finding.get("resolution_status") or "none")
    source = str(finding.get("resolution_source") or "none")
    trace_reference = finding.get("trace_reference")
    contract = str(
        finding.get("closure_contract_version") or CLOSURE_CONTRACT_VERSION
    )
    category = str(finding.get("type") or "")

    if not closure_semantics_enabled:
        return assigned_severity, status, source, trace_reference

    if category not in M1_SUCCESSOR_ACTIVATION_CATEGORIES:
        return assigned_severity, status, source, trace_reference

    if (
        status == "candidate_successor"
        and source == "successor"
        and trace_reference
        and contract == CLOSURE_CONTRACT_VERSION
    ):
        return (
            "info",
            "resolved_via_successor_activation",
            "successor",
            trace_reference,
        )

    return assigned_severity, status, source, trace_reference


def compute_gate_status_controlled(findings: list[dict[str, Any]]) -> str:
    """
    Verdict for post-boundary work health (DOA-ARCH-021 MVP):
    only controlled + boundary source zones, plus all cross-zone violations.
    Legacy-only and root findings do not affect this verdict by default.
    """
    relevant: list[dict[str, Any]] = []
    for f in findings:
        t = f.get("type")
        em = f.get("engine_mode")
        if t == "controlled_reference_to_legacy" or em == "cross_zone":
            relevant.append(f)
            continue
        sz = f.get("source_zone")
        if sz in ("controlled", "boundary"):
            relevant.append(f)
    if not relevant:
        return "ACCEPT"
    return compute_gate_status(relevant)


def compute_gate_status(findings: list[dict[str, Any]]) -> str:
    """
    Aggregate severities into gate status (DOA-DEC-032):
    any error -> REJECT; else any warn -> ACCEPT_WITH_WARNINGS; else ACCEPT.
    """
    sevs = [f.get("severity") for f in findings]
    if any(s == "error" for s in sevs):
        return "REJECT"
    if any(s == "warn" for s in sevs):
        return "ACCEPT_WITH_WARNINGS"
    return "ACCEPT"


def _count_severities(findings: list[dict[str, Any]]) -> dict[str, int]:
    c = {"error": 0, "warn": 0, "info": 0}
    for f in findings:
        s = f.get("severity")
        if s in c:
            c[s] += 1
    c["total"] = len(findings)
    return c


def _dual_mode_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    legacy_c = controlled_c = cross_c = other = 0
    for f in findings:
        t = f.get("type")
        em = f.get("engine_mode")
        if t == "controlled_reference_to_legacy" or em == "cross_zone":
            cross_c += 1
            continue
        sz = f.get("source_zone")
        if sz == "legacy":
            legacy_c += 1
        elif sz in ("controlled", "boundary"):
            controlled_c += 1
        else:
            other += 1
    return {
        "legacy_findings_count": legacy_c,
        "controlled_findings_count": controlled_c,
        "cross_zone_violations_count": cross_c,
        "other_zone_findings_count": other,
    }


def build_gate_report(
    *,
    repo_root: Path,
    engine_report: dict[str, Any],
    findings: list[dict[str, Any]],
    gate_status: str,
    gate_status_controlled: str,
    policy: dict[str, Any] | None,
    dry_run: bool,
    autofix: bool,
    policy_path: str | None,
) -> dict[str, Any]:
    eng = engine_report.get("validator") or {}
    engine_version = str(eng.get("version") or "unknown")
    pol = policy or {}
    policy_version = str(pol.get("version") or DEFAULT_POLICY_VERSION)

    counts = _count_severities(findings)
    dm = _dual_mode_counts(findings)

    return {
        "schema": GATE_REPORT_SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": str(repo_root.resolve()),
        "closure_contract_version": CLOSURE_CONTRACT_VERSION,
        "gate_status": gate_status,
        "gate_status_controlled": gate_status_controlled,
        "engine_version": engine_version,
        "policy_version": policy_version,
        "counts": {
            "total": counts["total"],
            "error": counts["error"],
            "warn": counts["warn"],
            "info": counts["info"],
        },
        "dual_mode_counts": dm,
        "findings": findings,
        "gate_run": {
            "dry_run": dry_run,
            "autofix": autofix,
            "policy_path": policy_path,
            "policy_loaded": policy_path is not None,
        },
        "raw": {
            "engine_report": engine_report,
        },
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="DocOps Document Gate — validator engine + policy (MVP T01–T04)."
    )
    p.add_argument(
        "--root",
        default=".",
        help="Repository root (must contain scripts/doa_link_id_validator.py).",
    )
    p.add_argument(
        "--out",
        default="reports/doa_document_gate_run_001.json",
        help="Path for gate output JSON (created under --root if relative).",
    )
    p.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Dry-run mode (default: on).",
    )
    p.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Disable dry-run (no file mutations in current MVP).",
    )
    p.set_defaults(dry_run=True)

    p.add_argument(
        "--autofix",
        action="store_true",
        default=False,
        help="Opt-in mechanical autofix (not implemented).",
    )

    p.add_argument(
        "--policy",
        default=None,
        help="Optional path to policy JSON (category_overrides, version).",
    )

    return p.parse_args(argv)


def _load_policy(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    pp = Path(path)
    if not pp.is_file():
        raise FileNotFoundError(f"Policy file not found: {pp}")
    with pp.open(encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    root = Path(args.root).resolve()

    policy_data = _load_policy(args.policy)

    engine_report = run_validator(root)

    normalized = normalize_findings(engine_report)

    findings: list[dict[str, Any]] = []
    for f in normalized:
        assigned = assign_severity(f, policy_data)
        (
            assigned,
            resolved_status,
            resolved_source,
            resolved_trace_reference,
        ) = apply_closure_activation(f, assigned)
        entry: dict[str, Any] = {
            "type": f["type"],
            "severity": assigned,
            "file": f["file"],
            "details": f["details"],
            "engine_mode": f.get("engine_mode"),
        }
        if f.get("severity") is not None:
            entry["engine_severity"] = f["severity"]
        entry["resolution_status"] = resolved_status
        entry["resolution_source"] = resolved_source
        entry["trace_reference"] = resolved_trace_reference
        entry["closure_contract_version"] = f.get(
            "closure_contract_version", CLOSURE_CONTRACT_VERSION
        )
        if f.get("overlay_source") is not None:
            entry["overlay_source"] = f["overlay_source"]
        if f.get("overlay_rule_type") is not None:
            entry["overlay_rule_type"] = f["overlay_rule_type"]
        if f.get("source_zone") is not None:
            entry["source_zone"] = f["source_zone"]
        if f.get("target_zone") is not None:
            entry["target_zone"] = f["target_zone"]
        findings.append(entry)

    gate_status = compute_gate_status(findings)
    gate_status_controlled = compute_gate_status_controlled(findings)

    report = build_gate_report(
        repo_root=root,
        engine_report=engine_report,
        findings=findings,
        gate_status=gate_status,
        gate_status_controlled=gate_status_controlled,
        policy=policy_data,
        dry_run=bool(args.dry_run),
        autofix=bool(args.autofix),
        policy_path=args.policy,
    )

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"Wrote {out_path} gate_status={gate_status} "
        f"gate_status_controlled={gate_status_controlled}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
