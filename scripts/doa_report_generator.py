#!/usr/bin/env python3
"""
MVP Report Generator (DOA-OP-021 T01–T07).

Loads validator + gate JSON, builds deterministic markdown with mandatory
(source: …) tags, provenance (incl. optional git HEAD), forbidden-string checks,
and a structural DoD gate. No NLP / LLM / policy interpretation.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENERATOR_VERSION = "doa-report-generator/0.1.0-mvp"

# T04: explicit source markers (short tags, template-only).
SRC_GATE = "(source: gate JSON)"
SRC_VAL = "(source: validator JSON)"
SRC_GATE_VAL = "(source: gate JSON; validator JSON)"
SRC_ARCH019 = "(source: DOA-ARCH-019)"
SRC_OP021 = "(source: DOA-OP-021)"
SRC_GEN = "(source: generator internal)"
SRC_CLI = "(source: CLI arguments)"
SRC_GIT = "(source: subprocess git rev-parse HEAD)"
SRC_NA = "(source: unavailable)"

REQUIRED_SECTION_HEADINGS = (
    "## summary",
    "## state by doc_type",
    "## risks",
    "## next steps",
    "## provenance",
)

TRACE_SECTIONS = frozenset(
    {
        "summary",
        "state by doc_type",
        "risks",
        "next steps",
        "provenance",
    }
)


def load_json(path: Path) -> dict[str, Any]:
    """T01: load JSON; exit on missing file or invalid JSON."""
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
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
    rows: list[Any] = []
    rows.extend(gate_p.get("findings") or [])
    rows.extend(val_p.get("canonical_violations") or [])
    rows.extend(val_p.get("legacy_findings") or [])
    if not _finding_rows_have_doc_type(rows):
        return False, {}
    return True, _aggregate_doc_type(rows)


def _find_git_root(candidates: list[Path | None]) -> Path | None:
    for base in candidates:
        if base is None:
            continue
        p = Path(base)
        if not p.exists():
            continue
        cur = p if p.is_dir() else p.parent
        for _ in range(20):
            if (cur / ".git").exists():
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent
    return None


def resolve_source_commit(repo_hint: Path | None) -> tuple[str, str]:
    """
    T06: return (commit_hash_or_unavailable, source_tag_for_line).
    Deterministic: git rev-parse HEAD in discovered repo, else unavailable.
    """
    root = _find_git_root([repo_hint, Path.cwd()])
    if root is None:
        return "unavailable", SRC_NA
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable", SRC_NA
    if proc.returncode != 0:
        return "unavailable", SRC_NA
    h = (proc.stdout or "").strip()
    if not h or not re.fullmatch(r"[0-9a-f]{7,40}", h, flags=re.IGNORECASE):
        return "unavailable", SRC_NA
    return h, SRC_GIT


def build_markdown(
    gate_p: dict[str, Any],
    val_p: dict[str, Any],
    validator_path: Path,
    gate_path: Path,
    generated_ts: str,
    doc_type_ok: bool,
    doc_type_counts: dict[str, int],
    source_commit: str,
    source_commit_src: str,
) -> str:
    """T03+T04+T06: fixed sections; every bullet carries an explicit (source: …) tag."""
    lines: list[str] = []
    lines.append("# Report Generator Output")
    lines.append("")
    lines.append("## summary")
    lines.append("")
    gs = gate_p.get("gate_status")
    gc = gate_p.get("counts") or {}
    vc = val_p.get("counts") or {}
    lines.append(
        f"- **gate_status** (from gate JSON): `{gs}` {SRC_GATE}"
    )
    lines.append(
        f"- **gate counts** (from gate JSON): `{json.dumps(gc, sort_keys=True, ensure_ascii=False)}` {SRC_GATE}"
    )
    lines.append(
        f"- **validator counts** (from validator JSON): `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}` {SRC_VAL}"
    )
    lines.append(
        f"- **note**: values above are copied from JSON inputs; this file is not a canonical DocOps document. {SRC_ARCH019}"
    )
    lines.append("")
    lines.append("## state by doc_type")
    lines.append("")
    if not doc_type_ok:
        lines.append(
            f"- doc_type aggregation **unavailable** from current inputs (no `doc_type` field on finding rows). {SRC_GATE_VAL}"
        )
    else:
        lines.append(
            f"- Aggregated counts where `doc_type` was present on finding rows. {SRC_GATE_VAL}"
        )
        for k in sorted(doc_type_counts.keys()):
            lines.append(f"- `{k}`: {doc_type_counts[k]} {SRC_GATE_VAL}")
    lines.append("")
    lines.append("## risks")
    lines.append("")
    ge = gc.get("error")
    gw = gc.get("warn")
    gi = gc.get("info")
    lines.append(
        f"- From **gate** `counts`: error={ge}, warn={gw}, info={gi} (numeric fields from input JSON). {SRC_GATE}"
    )
    if isinstance(vc, dict) and vc:
        lines.append(
            f"- From **validator** `counts`: `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}`. {SRC_VAL}"
        )
    lines.append("")
    lines.append("## next steps")
    lines.append("")
    lines.append(
        f"- Re-run validator and gate to refresh inputs, then regenerate this report. {SRC_OP021}"
    )
    lines.append(
        f"- Continue operational tasks per `DOA-OP-021` outside this generator. {SRC_OP021}"
    )
    lines.append("")
    lines.append("## provenance")
    lines.append("")
    lines.append(f"- **report generated at (UTC)**: `{generated_ts}` {SRC_GEN}")
    lines.append(f"- **validator input path**: `{validator_path.as_posix()}` {SRC_CLI}")
    lines.append(f"- **gate input path**: `{gate_path.as_posix()}` {SRC_CLI}")
    lines.append(f"- **generator version**: `{GENERATOR_VERSION}` {SRC_GEN}")
    lines.append(f"- **source_commit**: `{source_commit}` {source_commit_src}")
    ev = gate_p.get("engine_version")
    pv = gate_p.get("policy_version")
    if ev is not None:
        lines.append(f"- **gate engine_version** (from gate JSON): `{ev}` {SRC_GATE}")
    if pv is not None:
        lines.append(f"- **gate policy_version** (from gate JSON): `{pv}` {SRC_GATE}")
    vm = val_p.get("validator_meta") or {}
    if isinstance(vm, dict) and vm.get("version") is not None:
        lines.append(
            f"- **validator engine version** (from validator JSON): `{vm.get('version')}` {SRC_VAL}"
        )
    if gate_p.get("generated_at_utc") is not None:
        lines.append(
            f"- **gate.generated_at_utc** (from gate JSON): `{gate_p.get('generated_at_utc')}` {SRC_GATE}"
        )
    if val_p.get("generated_at_utc") is not None:
        lines.append(
            f"- **validator.generated_at_utc** (from validator JSON): `{val_p.get('generated_at_utc')}` {SRC_VAL}"
        )
    if gate_p.get("repo_root") is not None:
        lines.append(
            f"- **gate.repo_root** (from gate JSON): `{gate_p.get('repo_root')}` {SRC_GATE}"
        )
    if val_p.get("root") is not None:
        lines.append(
            f"- **validator.root** (from validator JSON): `{val_p.get('root')}` {SRC_VAL}"
        )
    lines.append("")
    return "\n".join(lines)


def check_forbidden_markdown(body: str) -> list[str]:
    """T05: structural string checks only."""
    errs: list[str] = []
    if "Parent:" in body or "parent:" in body:
        errs.append("forbidden substring: Parent:")
    if "Replaces:" in body or "replaces:" in body:
        errs.append("forbidden substring: Replaces:")
    if re.search(r"(?i)-\s*doc\s+type\s*:", body):
        errs.append("forbidden pattern: Doc type metadata bullet")
    if re.search(r"(?i)^-\s*id\s*:\s*DOA-", body, flags=re.MULTILINE):
        errs.append("forbidden pattern: canonical ID metadata bullet")
    if "## Metadata" in body:
        errs.append("forbidden section heading: ## Metadata")
    return errs


def check_traceability_markers(body: str) -> list[str]:
    """T04/T07: bullets in traced sections must contain '(source:' ."""
    errs: list[str] = []
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        if current is None or current not in TRACE_SECTIONS:
            continue
        if not line.strip():
            continue
        if line.strip().startswith("- "):
            if "(source:" not in line:
                errs.append(
                    f"traceability: bullet in '## {current}' missing (source: …): {line[:160]}"
                )
        else:
            errs.append(
                f"traceability: non-bullet line in '## {current}' (use bullet + source): {line[:160]}"
            )
    return errs


def validate_generated_report(body: str) -> list[str]:
    """T07: deterministic DoD checks aligned with DOA-DEC-039 MVP bar (structural)."""
    errs: list[str] = []
    first_line = next((ln for ln in body.splitlines() if ln.strip()), "")
    if first_line.strip() != "# Report Generator Output":
        errs.append("DoD: first non-empty line must be '# Report Generator Output'")
    for h in REQUIRED_SECTION_HEADINGS:
        if h not in body:
            errs.append(f"DoD: missing required section heading: {h}")
    errs.extend(check_traceability_markers(body))
    errs.extend(check_forbidden_markdown(body))
    # provenance non-empty: at least 4 bullet lines after ## provenance
    m = re.search(r"^## provenance\s*$", body, flags=re.MULTILINE)
    if not m:
        errs.append("DoD: provenance section not found")
    else:
        rest = body[m.end() :]
        nxt = re.search(r"^## ", rest, flags=re.MULTILINE)
        prov_block = rest if not nxt else rest[: nxt.start()]
        bullets = [ln for ln in prov_block.splitlines() if ln.strip().startswith("- ")]
        if len(bullets) < 4:
            errs.append(
                f"DoD: provenance must contain at least 4 bullet lines, got {len(bullets)}"
            )
    return errs


def main() -> None:
    parser = argparse.ArgumentParser(description="DOA MVP report generator (T01–T07).")
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
    repo_hint: Path | None = None
    for cand in (gate_p.get("repo_root"), val_p.get("root"), out_path.parent):
        if cand:
            repo_hint = Path(str(cand))
            break
    commit, commit_src = resolve_source_commit(repo_hint)

    md = build_markdown(
        gate_p,
        val_p,
        validator_path,
        gate_path,
        gen_ts,
        doc_type_ok,
        doc_type_counts,
        commit,
        commit_src,
    )

    problems = validate_generated_report(md)
    if problems:
        print("error: report validation failed:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_path.write_text(md, encoding="utf-8", newline="\n")
    except OSError as exc:
        print(f"error: cannot write {out_path}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
