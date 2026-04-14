#!/usr/bin/env python3
"""
MVP Report Generator (DOA-OP-021 T01–T07 + DOA-OP-024 + DOA-OP-025 RU strings).

Loads validator + gate JSON, builds deterministic markdown with mandatory
(source: …) tags, RU section titles and RU static copy, run record + delta,
provenance (incl. optional git HEAD), forbidden-string checks, structural DoD.
No NLP / LLM / policy interpretation.
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

GENERATOR_VERSION = "doa-report-generator/0.3.0-mvp"

# H1 title (RU static string, DOA-OP-025); must match validate_generated_report.
REPORT_TITLE = "# Вывод генератора отчётов"

# T04 / T05: explicit source markers (template-only).
SRC_GATE = "(source: gate JSON)"
SRC_VAL = "(source: validator JSON)"
SRC_GATE_VAL = "(source: gate JSON; validator JSON)"
SRC_ARCH019 = "(source: DOA-ARCH-019)"
SRC_OP021 = "(source: DOA-OP-021)"
SRC_OP024 = "(source: DOA-OP-024)"
SRC_OP025 = "(source: DOA-OP-025)"
SRC_GEN = "(source: generator internal)"
SRC_CLI = "(source: CLI arguments)"
SRC_GIT = "(source: subprocess git rev-parse HEAD)"
SRC_NA = "(source: unavailable)"

# T01: Russian section headings (DOA-OP-024).
SEC_SUMMARY = "## сводка"
SEC_RECORDED = "## зафиксировано в текущем запуске"
SEC_STATE = "## состояние по типам документов"
SEC_RISKS = "## риски"
SEC_NEXT = "## следующие шаги"
SEC_DELTA = "## что изменилось"
SEC_PROVENANCE = "## происхождение данных"

REQUIRED_SECTION_HEADINGS = (
    SEC_SUMMARY,
    SEC_RECORDED,
    SEC_STATE,
    SEC_RISKS,
    SEC_NEXT,
    SEC_DELTA,
    SEC_PROVENANCE,
)

TRACE_SECTIONS = frozenset(
    {
        "сводка",
        "зафиксировано в текущем запуске",
        "состояние по типам документов",
        "риски",
        "следующие шаги",
        "что изменилось",
        "происхождение данных",
    }
)

RUN_NAME_RE = re.compile(r"^report_generator_run_(\d+)\.md$", re.IGNORECASE)


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
    """Return (commit_hash_or_unavailable, source_tag_for_line)."""
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


def find_previous_report(out_path: Path) -> Path | None:
    """
    T03: deterministic search for report_generator_run_XXX.md in output directory,
    strictly lower run number than current file.
    """
    m = RUN_NAME_RE.match(out_path.name)
    if not m:
        return None
    cur = int(m.group(1))
    parent = out_path.parent
    if not parent.is_dir():
        return None
    best: int | None = None
    for p in parent.iterdir():
        if not p.is_file():
            continue
        mm = RUN_NAME_RE.match(p.name)
        if not mm:
            continue
        n = int(mm.group(1))
        if n >= cur:
            continue
        if best is None or n > best:
            best = n
    if best is None:
        return None
    return parent / f"report_generator_run_{best:03d}.md"


def extract_snapshot_from_report(md: str) -> dict[str, Any] | None:
    """
    T04: extract only fields this generator writes into сводка (same **keys**).
    Returns None if any mandatory field cannot be parsed.
    """
    m = re.search(r"\*\*gate_status\*\*[^`]*`([^`]*)`", md)
    if not m:
        return None
    gate_status = m.group(1).strip()
    m2 = re.search(r"\*\*gate counts\*\*[^`]*`(\{[^`]*\})`", md)
    if not m2:
        return None
    try:
        gate_counts = json.loads(m2.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(gate_counts, dict):
        return None
    m3 = re.search(r"\*\*validator counts\*\*[^`]*`(\{[^`]*\})`", md)
    if not m3:
        return None
    try:
        validator_counts = json.loads(m3.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(validator_counts, dict):
        return None
    return {
        "gate_status": gate_status,
        "gate_counts": gate_counts,
        "validator_counts": validator_counts,
    }


def _fmt_delta_gate_count(key: str, old_c: dict[str, Any], new_c: dict[str, Any]) -> str | None:
    ov = old_c.get(key)
    nv = new_c.get(key)
    try:
        oi = int(ov) if ov is not None else None
        ni = int(nv) if nv is not None else None
    except (TypeError, ValueError):
        return None
    if oi == ni:
        return None
    if oi is None or ni is None:
        return None
    d = ni - oi
    return (
        f"- счётчик **gate** `counts` / `{key}`: было `{oi}`, стало `{ni}`, разница `{d}` {SRC_GATE}"
    )


def build_delta_lines(
    prev_path: Path | None,
    prev_snap: dict[str, Any] | None,
    prev_read_failed: bool,
    gate_p: dict[str, Any],
    val_p: dict[str, Any],
) -> list[str]:
    """T04: deterministic delta bullets."""
    lines: list[str] = []
    if prev_path is None:
        lines.append(f"- предыдущий запуск не найден {SRC_NA}")
        return lines
    if prev_read_failed:
        lines.append(
            f"- предыдущий запуск найден (`{prev_path.name}`), но файл не прочитан {SRC_NA}"
        )
        return lines
    if prev_snap is None:
        lines.append(
            f"- предыдущий запуск найден (`{prev_path.name}`), но данные недоступны для сравнения {SRC_NA}"
        )
        return lines

    new_gs = gate_p.get("gate_status")
    old_gs = prev_snap.get("gate_status")
    new_gc = gate_p.get("counts") or {}
    old_gc = prev_snap.get("gate_counts") or {}
    new_vc = val_p.get("counts") or {}
    old_vc = prev_snap.get("validator_counts") or {}

    out: list[str] = []
    if old_gs != new_gs:
        out.append(f"- `gate_status`: было `{old_gs}`, стало `{new_gs}` {SRC_GATE}")

    for key in ("error", "warn", "info"):
        ln = _fmt_delta_gate_count(key, old_gc, new_gc)
        if ln:
            out.append(ln)

    old_js = json.dumps(old_vc, sort_keys=True, ensure_ascii=False)
    new_js = json.dumps(new_vc, sort_keys=True, ensure_ascii=False)
    if old_js != new_js:
        out.append(
            f"- `validator counts` (JSON): было `{old_js}`, стало `{new_js}` {SRC_VAL}"
        )

    if not out:
        out.append(
            f"- изменений по доступным полям не обнаружено {SRC_GEN}"
        )
    return out


def build_recorded_lines(
    validator_path: Path, gate_path: Path, out_path: Path
) -> list[str]:
    """T02: facts of current run only."""
    return [
        f"- выполнена загрузка входного файла validator `{validator_path.name}` {SRC_VAL}",
        f"- выполнена загрузка входного файла gate `{gate_path.name}` {SRC_GATE}",
        f"- сформирован файл отчёта `{out_path.name}` {SRC_GEN}",
    ]


def build_markdown(
    gate_p: dict[str, Any],
    val_p: dict[str, Any],
    validator_path: Path,
    gate_path: Path,
    out_path: Path,
    generated_ts: str,
    doc_type_ok: bool,
    doc_type_counts: dict[str, int],
    source_commit: str,
    source_commit_src: str,
    delta_lines: list[str],
) -> str:
    """Build full report (RU headings, new sections)."""
    lines: list[str] = []
    lines.append(REPORT_TITLE)
    lines.append("")
    lines.append(SEC_SUMMARY)
    lines.append("")
    gs = gate_p.get("gate_status")
    gc = gate_p.get("counts") or {}
    vc = val_p.get("counts") or {}
    lines.append(f"- **gate_status** (данные из gate JSON): `{gs}` {SRC_GATE}")
    lines.append(
        f"- **gate counts** (данные из gate JSON): `{json.dumps(gc, sort_keys=True, ensure_ascii=False)}` {SRC_GATE}"
    )
    lines.append(
        f"- **validator counts** (данные из validator JSON): `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}` {SRC_VAL}"
    )
    lines.append(
        f"- **примечание**: значения выше скопированы из входных JSON; файл не является каноническим документом DocOps. {SRC_ARCH019}"
    )
    lines.append("")
    lines.append(SEC_RECORDED)
    lines.append("")
    lines.extend(build_recorded_lines(validator_path, gate_path, out_path))
    lines.append("")
    lines.append(SEC_STATE)
    lines.append("")
    if not doc_type_ok:
        lines.append(
            f"- агрегация **doc_type** **недоступна**: во входах нет поля `doc_type` в строках находок. {SRC_GATE_VAL}"
        )
    else:
        lines.append(
            f"- агрегированные счётчики по строкам, где было поле `doc_type`. {SRC_GATE_VAL}"
        )
        for k in sorted(doc_type_counts.keys()):
            lines.append(f"- `{k}`: {doc_type_counts[k]} {SRC_GATE_VAL}")
    lines.append("")
    lines.append(SEC_RISKS)
    lines.append("")
    ge = gc.get("error")
    gw = gc.get("warn")
    gi = gc.get("info")
    lines.append(
        f"- из **gate** `counts`: error={ge}, warn={gw}, info={gi} (числовые поля из входного JSON). {SRC_GATE}"
    )
    if isinstance(vc, dict) and vc:
        lines.append(
            f"- из **validator** `counts`: `{json.dumps(vc, sort_keys=True, ensure_ascii=False)}`. {SRC_VAL}"
        )
    lines.append("")
    lines.append(SEC_NEXT)
    lines.append("")
    lines.append(
        f"- повторно запустить validator и gate, обновить входы и сгенерировать отчёт заново. {SRC_OP021}"
    )
    lines.append(
        f"- продолжить операционные задачи по `DOA-OP-021` вне этого генератора. {SRC_OP021}"
    )
    lines.append(
        f"- человеко-читаемый deterministic слой по `DOA-OP-024` / `DOA-DEC-043`. {SRC_OP024}"
    )
    lines.append(
        f"- полная русификация статических строк по `DOA-OP-025` / `DOA-DEC-044`. {SRC_OP025}"
    )
    lines.append("")
    lines.append(SEC_DELTA)
    lines.append("")
    lines.extend(delta_lines)
    lines.append("")
    lines.append(SEC_PROVENANCE)
    lines.append("")
    lines.append(f"- **время генерации отчёта (UTC)**: `{generated_ts}` {SRC_GEN}")
    lines.append(f"- **путь входного файла validator**: `{validator_path.as_posix()}` {SRC_CLI}")
    lines.append(f"- **путь входного файла gate**: `{gate_path.as_posix()}` {SRC_CLI}")
    lines.append(f"- **версия генератора**: `{GENERATOR_VERSION}` {SRC_GEN}")
    lines.append(f"- **source_commit**: `{source_commit}` {source_commit_src}")
    ev = gate_p.get("engine_version")
    pv = gate_p.get("policy_version")
    if ev is not None:
        lines.append(f"- **gate.engine_version** (из gate JSON): `{ev}` {SRC_GATE}")
    if pv is not None:
        lines.append(f"- **gate.policy_version** (из gate JSON): `{pv}` {SRC_GATE}")
    vm = val_p.get("validator_meta") or {}
    if isinstance(vm, dict) and vm.get("version") is not None:
        lines.append(
            f"- **validator** версия движка (из validator JSON): `{vm.get('version')}` {SRC_VAL}"
        )
    if gate_p.get("generated_at_utc") is not None:
        lines.append(
            f"- **gate.generated_at_utc** (из gate JSON): `{gate_p.get('generated_at_utc')}` {SRC_GATE}"
        )
    if val_p.get("generated_at_utc") is not None:
        lines.append(
            f"- **validator.generated_at_utc** (из validator JSON): `{val_p.get('generated_at_utc')}` {SRC_VAL}"
        )
    if gate_p.get("repo_root") is not None:
        lines.append(
            f"- **gate.repo_root** (из gate JSON): `{gate_p.get('repo_root')}` {SRC_GATE}"
        )
    if val_p.get("root") is not None:
        lines.append(
            f"- **validator.root** (из validator JSON): `{val_p.get('root')}` {SRC_VAL}"
        )
    lines.append("")
    return "\n".join(lines)


def check_forbidden_markdown(body: str) -> list[str]:
    """Forbidden structural patterns."""
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
    """Bullets in traced sections must contain '(source:' ."""
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
    """Structural DoD (DOA-DEC-039 subset) + RU headings (DOA-OP-024)."""
    errs: list[str] = []
    first_line = next((ln for ln in body.splitlines() if ln.strip()), "")
    if first_line.strip() != REPORT_TITLE:
        errs.append(f"DoD: first non-empty line must be '{REPORT_TITLE}'")
    for h in REQUIRED_SECTION_HEADINGS:
        if h not in body:
            errs.append(f"DoD: missing required section heading: {h}")
    errs.extend(check_traceability_markers(body))
    errs.extend(check_forbidden_markdown(body))
    prov_title = SEC_PROVENANCE[3:].strip()
    m = re.search(rf"^## {re.escape(prov_title)}\s*$", body, flags=re.MULTILINE)
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
    parser = argparse.ArgumentParser(
        description="DOA MVP report generator (T01–T07 + OP-024/025 human-readable RU layer)."
    )
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

    prev_path = find_previous_report(out_path)
    prev_snap: dict[str, Any] | None = None
    prev_read_failed = False
    if prev_path is not None:
        try:
            prev_text = prev_path.read_text(encoding="utf-8-sig")
        except OSError:
            prev_read_failed = True
        else:
            prev_snap = extract_snapshot_from_report(prev_text)

    delta_lines = build_delta_lines(prev_path, prev_snap, prev_read_failed, gate_p, val_p)

    md = build_markdown(
        gate_p,
        val_p,
        validator_path,
        gate_path,
        out_path,
        gen_ts,
        doc_type_ok,
        doc_type_counts,
        commit,
        commit_src,
        delta_lines,
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
