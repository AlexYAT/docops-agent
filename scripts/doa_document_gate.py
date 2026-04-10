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

GATE_REPORT_SCHEMA = "doa-gate-report/1"
DEFAULT_POLICY_VERSION = "doa-gate-policy/1"
VALID_SEVERITIES = frozenset({"error", "warn", "info"})


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
                "resolution_status": item.get("resolution_status"),
                "overlay_source": item.get("overlay_source"),
                "overlay_rule_type": item.get("overlay_rule_type"),
            }
        )

    for item in report.get("canonical_violations") or []:
        _one("canonical", item)
    for item in report.get("legacy_findings") or []:
        _one("legacy", item)

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

    pol = policy or {}
    overrides = pol.get("category_overrides") or {}
    cat = finding.get("type") or ""
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


def build_gate_report(
    *,
    repo_root: Path,
    engine_report: dict[str, Any],
    findings: list[dict[str, Any]],
    gate_status: str,
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

    return {
        "schema": GATE_REPORT_SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": str(repo_root.resolve()),
        "gate_status": gate_status,
        "engine_version": engine_version,
        "policy_version": policy_version,
        "counts": {
            "total": counts["total"],
            "error": counts["error"],
            "warn": counts["warn"],
            "info": counts["info"],
        },
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
        entry: dict[str, Any] = {
            "type": f["type"],
            "severity": assigned,
            "file": f["file"],
            "details": f["details"],
            "engine_mode": f.get("engine_mode"),
        }
        if f.get("severity") is not None:
            entry["engine_severity"] = f["severity"]
        if f.get("resolution_status") is not None:
            entry["resolution_status"] = f["resolution_status"]
        if f.get("overlay_source") is not None:
            entry["overlay_source"] = f["overlay_source"]
        if f.get("overlay_rule_type") is not None:
            entry["overlay_rule_type"] = f["overlay_rule_type"]
        findings.append(entry)

    gate_status = compute_gate_status(findings)

    report = build_gate_report(
        repo_root=root,
        engine_report=engine_report,
        findings=findings,
        gate_status=gate_status,
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

    print(f"Wrote {out_path} gate_status={gate_status}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
