#!/usr/bin/env python3
"""
DocOps Document Gate MVP (DOA-OP-020) — CLI and validator adapter (T01/T02).

Does not implement document checks; delegates to scripts/doa_link_id_validator.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


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

    Each item: type, severity (None if absent), file, details.
    """
    out: list[dict[str, Any]] = []

    def _one(bucket: str, item: dict[str, Any]) -> None:
        category = item.get("category") or bucket
        sev = item.get("severity")
        if sev is not None:
            sev = str(sev).lower()

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
            }
        )

    for item in report.get("canonical_violations") or []:
        _one("canonical_violation", item)
    for item in report.get("legacy_findings") or []:
        _one("legacy_finding", item)

    return out


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="DocOps Document Gate — validator adapter (MVP T01/T02)."
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
        help="Disable dry-run (for future phases; no file mutations in T01/T02).",
    )
    p.set_defaults(dry_run=True)

    p.add_argument(
        "--autofix",
        action="store_true",
        default=False,
        help="Enable mechanical autofix (opt-in; not implemented in T01/T02).",
    )

    p.add_argument(
        "--policy",
        default=None,
        help="Optional path to policy file (JSON); loaded if present, passed through in output.",
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

    policy_data = None
    if args.policy:
        policy_data = _load_policy(args.policy)

    engine_report = run_validator(root)

    normalized = normalize_findings(engine_report)

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "gate": {
            "dry_run": args.dry_run,
            "autofix": bool(args.autofix),
            "policy_path": args.policy,
            "policy_loaded": policy_data is not None,
        },
        "engine_report": engine_report,
        "normalized_findings": normalized,
    }
    if policy_data is not None:
        payload["policy"] = policy_data

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
