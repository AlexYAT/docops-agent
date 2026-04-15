#!/usr/bin/env python3
"""
Minimal link/ID validator for DocOps Agent (DOA-OP-018).
Outputs JSON to stdout; use shell redirection to save report.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY_REGISTRY_PATH = ROOT / "docs" / "rules" / "overlay_registry.json"
CLOSURE_CONTRACT_VERSION = "closure/1"
closure_semantics_enabled = False

# MVP dual-mode boundary (DOA-DEC-047): Git commit that introduced DOA-FSN-001.
# Replace only when a new fixed_snapshot epoch is policy-approved.
BOUNDARY_COMMIT = "d94a7d7b9751309ffbd55dd71614e25071c08c8a"
BOUNDARY_FILE_POSIX = "docs/fixed_snapshot/DOA-FSN-001_boundary_pre_controlled_phase.md"

STRICT_ID_RE = re.compile(r"^DOA-(IDEA|ARCH|DEC|LT|MT|OP|IMP|AUD|OTH|RUL|FSN)-(\d+)$")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

FAMILY_TO_DOC_TYPE = {
    "IDEA": "idea_to_mvp",
    "ARCH": "architecture_draft",
    "DEC": "decision_log",
    "LT": "longterm_plan",
    "MT": "midterm_plan",
    "OP": "operational_plan",
    "IMP": "implementation_snapshot",
    "AUD": "audit_check",
    "OTH": "other",
    "RUL": "rules",
    "FSN": "fixed_snapshot",
}

STATUS_ENUM = frozenset({"draft", "review", "accepted", "obsolete"})


def _git_first_commit_introducing(root: Path, rel_posix: str) -> str | None:
    """Earliest commit that introduced path (diff-filter=A). Best-effort; None on failure."""
    proc = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "--format=%H",
            "--reverse",
            "--",
            rel_posix,
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    if proc.returncode != 0:
        return None
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return lines[0] if lines else None


def _git_is_strict_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    if ancestor == descendant:
        return False
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(root),
        capture_output=True,
        timeout=60,
    )
    return proc.returncode == 0


def classify_path_zone(root: Path, rel_posix: str, first_commit: str | None) -> str:
    """
    legacy | boundary | controlled | unknown (DOA-DEC-047 + DOA-ARCH-021).
    """
    if first_commit is None:
        return "unknown"
    if rel_posix == BOUNDARY_FILE_POSIX and first_commit == BOUNDARY_COMMIT:
        return "boundary"
    if first_commit == BOUNDARY_COMMIT and rel_posix != BOUNDARY_FILE_POSIX:
        return "controlled"
    if _git_is_strict_ancestor(root, first_commit, BOUNDARY_COMMIT):
        return "legacy"
    if _git_is_strict_ancestor(root, BOUNDARY_COMMIT, first_commit):
        return "controlled"
    return "unknown"


def build_docs_path_zones(root: Path, targets: list[Path]) -> dict[str, str]:
    """Map docs-relative posix path -> zone."""
    zones: dict[str, str] = {}
    for path in targets:
        rel = path.relative_to(root)
        if rel.parts[0] != "docs":
            continue
        rp = rel.as_posix()
        fc = _git_first_commit_introducing(root, rp)
        zones[rp] = classify_path_zone(root, rp, fc)
    return zones


def check_controlled_to_legacy_links(
    root: Path,
    source_path: Path,
    content: str,
    source_zone: str,
    path_zones: dict[str, str],
    cross_zone: list[dict],
) -> None:
    if source_zone != "controlled":
        return
    rel_parent = source_path.parent
    srel = source_path.relative_to(root).as_posix()
    for _text, target in LINK_RE.findall(content):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in target:
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        cand = (rel_parent / clean).resolve()
        try:
            trel = cand.relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
        if not cand.is_file():
            continue
        if not trel.endswith(".md") or not trel.startswith("docs/"):
            continue
        tz = path_zones.get(trel, "unknown")
        if tz == "legacy":
            cross_zone.append(
                {
                    "severity": "error",
                    "mode": "cross_zone",
                    "category": "controlled_reference_to_legacy",
                    "file": srel,
                    "target": trel,
                    "detail": f"controlled file links to legacy target {trel}",
                    "source_zone": "controlled",
                    "target_zone": "legacy",
                }
            )


def _posix_rel_key(path_str: str) -> str:
    """Normalize Windows paths to POSIX keys for zone map lookup."""
    return path_str.replace("\\", "/")


def _attach_source_zone(item: dict, path_zones: dict[str, str]) -> None:
    if item.get("source_zone"):
        return
    f = item.get("file")
    if f and isinstance(f, str):
        fp = _posix_rel_key(f)
        if fp.startswith("docs/"):
            item["source_zone"] = path_zones.get(fp, "unknown")
        else:
            item["source_zone"] = "root"
        return
    files = item.get("files")
    if files and isinstance(files, (list, tuple)) and files:
        first = _posix_rel_key(str(files[0]))
        if first.startswith("docs/"):
            item["source_zone"] = path_zones.get(first, "unknown")


def load_overlay_registry(path: Path) -> dict:
    if not path.is_file():
        return {
            "loaded": False,
            "source": str(path.relative_to(ROOT)),
            "mappings": [],
            "parent_overrides": [],
            "aliases": [],
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "loaded": False,
            "source": str(path.relative_to(ROOT)),
            "mappings": [],
            "parent_overrides": [],
            "aliases": [],
        }
    return {
        "loaded": True,
        "source": str(path.relative_to(ROOT)),
        "mappings": data.get("mappings") or [],
        "parent_overrides": data.get("parent_overrides") or [],
        "aliases": data.get("aliases") or [],
    }


def apply_overlay_resolution_markers(
    canonical_violations: list[dict], overlay: dict
) -> tuple[int, int]:
    source = overlay.get("source", "docs/rules/overlay_registry.json")

    duplicate_overlay_ids = {
        m.get("legacy_id")
        for m in overlay.get("mappings", [])
        if m.get("type") == "duplicate_id" and m.get("status") == "active"
    }

    parent_override_index = {
        (po.get("child"), po.get("original_parent")): po
        for po in overlay.get("parent_overrides", [])
        if po.get("child") and po.get("original_parent")
    }

    resolved = 0
    unresolved = 0

    for item in canonical_violations:
        item["resolution_status"] = "none"
        item["resolution_source"] = "none"
        item["trace_reference"] = None
        item["closure_contract_version"] = CLOSURE_CONTRACT_VERSION

        if item.get("category") == "duplicate_id_registry":
            dup_id = item.get("detail")
            if dup_id in duplicate_overlay_ids:
                item["resolution_status"] = "resolved_via_overlay"
                item["resolution_source"] = "overlay"
                item["overlay_source"] = source
                item["overlay_rule_type"] = "mapping:duplicate_id"
                item["trace_reference"] = "mapping:duplicate_id"

        elif item.get("category") == "unresolved_parent":
            child = item.get("doc_id")
            original_parent = item.get("detail")
            if (child, original_parent) in parent_override_index:
                item["resolution_status"] = "resolved_via_overlay"
                item["resolution_source"] = "overlay"
                item["overlay_source"] = source
                item["overlay_rule_type"] = "parent_override"
                item["trace_reference"] = "parent_override"

        if item["resolution_status"] == "resolved_via_overlay":
            resolved += 1
        else:
            unresolved += 1

    return resolved, unresolved


def apply_candidate_successor_markers(
    canonical_violations: list[dict], successor_by_replaces: dict[str, list[dict[str, str]]]
) -> None:
    """
    T06 bridge marker only:
    annotate candidate successor closure for selected categories without changing severity.
    """
    for item in canonical_violations:
        if item.get("resolution_status") != "none":
            continue
        if item.get("category") not in {"noncanonical_doc_type_key", "invalid_replaces_format"}:
            continue
        src_id = item.get("doc_id")
        if not src_id:
            continue
        candidates = successor_by_replaces.get(str(src_id), [])
        if not candidates:
            continue
        chosen = candidates[0]
        item["resolution_status"] = "candidate_successor"
        item["resolution_source"] = "successor"
        item["trace_reference"] = chosen.get("id")


def parse_metadata(content: str) -> dict[str, str] | None:
    m = re.search(
        r"^## Metadata\s*\n(.*?)(?=^---\s*$|^\n## \S|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not m:
        return None
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("- ") and ":" in line[2:]:
            k, v = line[2:].split(":", 1)
            data[k.strip()] = v.strip()
    return data if data else None


def file_doc_type(rel: Path) -> str | None:
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "docs":
        return parts[1]
    return None


def stem_base_id(name: str) -> str | None:
    m = re.match(r"^(DOA-(?:IDEA|ARCH|DEC|LT|MT|OP|IMP|AUD|OTH|RUL|FSN)-\d+)", name)
    return m.group(1) if m else None


def legacy_header_id(content: str) -> str | None:
    for pat in (
        r"^#\s*Decision:\s*(DOA-DEC-\d+)",
        r"^#\s*(DOA-DEC-\d+)\s+[—\-]",
        r"^#\s*(DOA-DEC-\d+)\s*$",
        r"^#\s*architecture_draft\s*[—\-]\s*(DOA-ARCH-\d+)",
        r"^#\s*operational_plan\s*[—\-]\s*(DOA-OP-\d+)",
        r"^#\s*implementation_snapshot\s*[—\-]\s*(DOA-IMP-\d+)",
        r"^#\s*audit_check\s*[—\-]\s*(DOA-AUD-\d+)",
        r"^#\s*(DOA-OP-\d+)\s*$",
        r"^#\s*(DOA-IMP-\d+)\s+",
    ):
        m = re.search(pat, content, re.MULTILINE)
        if m:
            return m.group(1)
    return None


def is_canonical(meta: dict[str, str] | None) -> bool:
    if not meta:
        return False
    i = meta.get("ID") or meta.get("Id")
    return bool(i and STRICT_ID_RE.match(i))


def collect_targets(root: Path) -> list[Path]:
    out: list[Path] = []
    out.extend(sorted(root.glob("docs/**/*.md")))
    for name in ("README.md", "WORKFLOW.md"):
        p = root / name
        if p.is_file():
            out.append(p)
    return out


def check_links(path: Path, content: str, issues: list[dict]) -> None:
    rel_parent = path.parent
    for _text, target in LINK_RE.findall(content):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in target:
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        cand = (rel_parent / clean).resolve()
        try:
            cand.relative_to(ROOT.resolve())
        except ValueError:
            issues.append(
                {
                    "severity": "info",
                    "mode": "root_link",
                    "category": "markdown_link_escape",
                    "file": str(path.relative_to(ROOT)),
                    "target": target,
                }
            )
            continue
        if not cand.is_file():
            issues.append(
                {
                    "severity": "warn",
                    "mode": "root_link",
                    "category": "broken_markdown_link",
                    "file": str(path.relative_to(ROOT)),
                    "target": target,
                }
            )


def main() -> int:
    targets = collect_targets(ROOT)
    overlay = load_overlay_registry(OVERLAY_REGISTRY_PATH)
    # Pass 1: known IDs
    id_to_files: dict[str, list[str]] = {}
    for path in targets:
        rel = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(json.dumps({"error": str(e), "file": str(rel)}), file=sys.stderr)
            return 1
        meta = parse_metadata(text)
        ids: list[str] = []
        if is_canonical(meta):
            assert meta is not None
            ids.append(meta["ID"])
        bid = stem_base_id(path.stem)
        if bid:
            ids.append(bid)
        hid = legacy_header_id(text)
        if hid:
            ids.append(hid)
        srel = str(rel)
        for i in ids:
            lst = id_to_files.setdefault(i, [])
            if srel not in lst:
                lst.append(srel)

    known_ids = set(id_to_files.keys())

    path_zones = build_docs_path_zones(ROOT, targets)
    cross_zone_violations: list[dict] = []

    canonical_violations: list[dict] = []
    legacy_findings: list[dict] = []
    successor_by_replaces: dict[str, list[dict[str, str]]] = {}

    for path in targets:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        meta = parse_metadata(text)
        fdt = file_doc_type(rel)

        if rel.parts[0] != "docs":
            check_links(path, text, legacy_findings)
            legacy_findings.append(
                {
                    "mode": "legacy",
                    "category": "root_markdown_outside_docs_model",
                    "file": str(rel),
                    "detail": "README/WORKFLOW not required to carry ## Metadata",
                }
            )
            continue

        sz = path_zones.get(rel.as_posix(), "unknown")
        check_controlled_to_legacy_links(
            ROOT, path, text, sz, path_zones, cross_zone_violations
        )

        canonical = is_canonical(meta)

        if not canonical:
            lf = {
                "mode": "legacy",
                "category": "legacy_no_canonical_metadata",
                "file": str(rel),
                "detail": "No ## Metadata with strict ID field",
            }
            legacy_findings.append(lf)
            hid = legacy_header_id(text)
            bid = stem_base_id(path.stem)
            inferred = meta.get("ID") if meta else None
            if hid and bid and hid != bid:
                legacy_findings.append(
                    {
                        "mode": "legacy",
                        "category": "legacy_heading_filename_id_mismatch",
                        "file": str(rel),
                        "detail": f"heading {hid} vs filename {bid}",
                    }
                )
            if meta and "Type" in meta and "Doc type" not in meta:
                legacy_findings.append(
                    {
                        "mode": "legacy",
                        "category": "legacy_type_alias_metadata",
                        "file": str(rel),
                        "detail": "Uses Type: instead of Doc type:",
                    }
                )
            if meta and "Parent" not in meta:
                legacy_findings.append(
                    {
                        "mode": "legacy",
                        "category": "legacy_metadata_incomplete",
                        "file": str(rel),
                        "detail": "Metadata present but missing Parent",
                    }
                )
            # unresolved parent from legacy header/metadata line ## Parent
            pm = re.search(r"^## Parent\s*\n\s*(\S.+)$", text, re.MULTILINE)
            if pm:
                pv = pm.group(1).strip()
                if pv.lower() != "null" and pv not in known_ids:
                    legacy_findings.append(
                        {
                            "mode": "legacy",
                            "category": "legacy_unresolved_parent",
                            "file": str(rel),
                            "detail": f"Parent {pv}",
                        }
                    )
            continue

        assert meta is not None
        doc_id = meta["ID"]
        doc_type_val = meta.get("Doc type") or meta.get("Type")
        has_canonical_doc_type_key = "Doc type" in meta and "Type" not in meta
        if "Type" in meta and "Doc type" not in meta:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "noncanonical_doc_type_key",
                    "file": str(rel),
                    "doc_id": doc_id,
                    "detail": "Uses Type: instead of Doc type:",
                }
            )
        if not doc_type_val:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "missing_doc_type",
                    "file": str(rel),
                }
            )
        elif fdt and doc_type_val != fdt:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "folder_doc_type_mismatch",
                    "file": str(rel),
                    "detail": f"folder={fdt} metadata={doc_type_val}",
                }
            )

        bid = stem_base_id(path.stem)
        if bid and bid != doc_id:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "id_filename_mismatch",
                    "file": str(rel),
                    "detail": f"metadata {doc_id} vs filename stem {bid}",
                }
            )

        parts = doc_id.split("-")
        if len(parts) >= 3:
            fam_key = parts[1]
            expected_dt = FAMILY_TO_DOC_TYPE.get(fam_key)
            if expected_dt and doc_type_val and expected_dt != doc_type_val:
                canonical_violations.append(
                    {
                        "mode": "canonical",
                        "category": "id_family_doc_type_mismatch",
                        "file": str(rel),
                        "detail": f"{doc_id} family implies {expected_dt}, got {doc_type_val}",
                    }
                )

        st = (meta.get("Status") or "").lower()
        if st and st not in STATUS_ENUM:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "status_not_in_enum",
                    "file": str(rel),
                    "detail": st,
                }
            )

        parent = meta.get("Parent")
        if parent is None:
            canonical_violations.append(
                {
                    "mode": "canonical",
                    "category": "missing_parent_field",
                    "file": str(rel),
                }
            )
        else:
            pl = parent.strip()
            if pl.lower() != "null" and pl not in known_ids:
                canonical_violations.append(
                    {
                        "mode": "canonical",
                        "category": "unresolved_parent",
                        "file": str(rel),
                        "doc_id": doc_id,
                        "detail": pl,
                    }
                )

        replaces = meta.get("Replaces")
        if replaces:
            rs = replaces.strip()
            if not STRICT_ID_RE.match(rs):
                canonical_violations.append(
                    {
                        "mode": "canonical",
                        "category": "invalid_replaces_format",
                        "file": str(rel),
                        "doc_id": doc_id,
                        "detail": rs,
                    }
                )
            elif rs not in known_ids:
                canonical_violations.append(
                    {
                        "mode": "canonical",
                        "category": "unresolved_replaces",
                        "file": str(rel),
                        "detail": rs,
                    }
                )

            # Successor index (T06 bridge): canonical Doc type key + valid Replaces format.
            if (
                has_canonical_doc_type_key
                and fdt is not None
                and doc_type_val == fdt
                and STRICT_ID_RE.match(rs)
            ):
                successor_by_replaces.setdefault(rs, []).append(
                    {
                        "id": doc_id,
                        "file": str(rel),
                    }
                )

        # OP doc in IMP folder (family from filename)
        if bid:
            fam = bid.split("-")[1]
            if fam == "OP" and fdt == "implementation_snapshot":
                canonical_violations.append(
                    {
                        "mode": "canonical",
                        "category": "folder_family_mismatch",
                        "file": str(rel),
                        "detail": "OP id in implementation_snapshot path",
                    }
                )

    dup_ids = {i: fs for i, fs in id_to_files.items() if len(fs) > 1}
    for i, fs in dup_ids.items():
        canonical_violations.append(
            {
                "mode": "canonical",
                "category": "duplicate_id_registry",
                "detail": i,
                "files": fs,
            }
        )

    resolved_count, unresolved_count = apply_overlay_resolution_markers(
        canonical_violations, overlay
    )
    apply_candidate_successor_markers(canonical_violations, successor_by_replaces)

    for item in canonical_violations:
        _attach_source_zone(item, path_zones)
    for item in legacy_findings:
        _attach_source_zone(item, path_zones)

    zone_counts = Counter(path_zones.values())

    report = {
        "validator": {
            "name": "doa_link_id_validator",
            "version": "0.2.0",
            "schema": "doa-validator-report/1",
        },
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": str(ROOT),
        "scope": {
            "globs": ["docs/**/*.md", "README.md", "WORKFLOW.md"],
            "files_scanned": len(targets),
        },
        "counts": {
            "canonical_violations": len(canonical_violations),
            "legacy_findings": len(legacy_findings),
            "canonical_resolved_via_overlay": resolved_count,
            "canonical_unresolved_violations": unresolved_count,
            "cross_zone_violations": len(cross_zone_violations),
        },
        "closure_contract_version": CLOSURE_CONTRACT_VERSION,
        "dual_mode": {
            "boundary_commit": BOUNDARY_COMMIT,
            "boundary_file": BOUNDARY_FILE_POSIX,
            "docs_path_zone_counts": dict(zone_counts),
            "note": "Zones from Git first-commit vs boundary (DOA-DEC-047). "
            "Authoritative runs require full Git history (non-shallow clone).",
        },
        "cross_zone_violations": cross_zone_violations,
        "canonical_violations": canonical_violations,
        "legacy_findings": legacy_findings,
        "overlay": {
            "loaded": overlay.get("loaded", False),
            "source": overlay.get("source", "docs/rules/overlay_registry.json"),
        },
        "top_categories": [],
    }

    cat_counter: Counter[str] = Counter()
    for item in canonical_violations:
        cat_counter[item.get("category", "?")] += 1
    for item in legacy_findings:
        cat_counter[item.get("category", "?")] += 1
    report["top_categories"] = [
        {"category": c, "count": n} for c, n in cat_counter.most_common(10)
    ]

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
