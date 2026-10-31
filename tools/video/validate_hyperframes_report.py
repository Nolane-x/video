#!/usr/bin/env python3
"""Fail closed when HyperFrames' integrated QA report contains non-zero findings."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SECTIONS = ("lint", "runtime", "layout", "motion", "contrast", "craft", "audio")


def validate_report(
    report: dict[str, Any],
    *,
    snapshot_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if report.get("ok") is not True:
        errors.append("HyperFrames check report did not return ok=true")
    if report.get("strict") is not True:
        errors.append("HyperFrames check report was not produced in strict mode")

    for section_name in SECTIONS:
        section = report.get(section_name)
        if not isinstance(section, dict):
            errors.append(f"Missing QA section: {section_name}")
            continue
        if section.get("ok") is not True:
            errors.append(f"{section_name}: ok is not true")
        for count_name in ("errorCount", "warningCount"):
            count = section.get(count_name)
            if not isinstance(count, int):
                errors.append(f"{section_name}: missing integer {count_name}")
            elif count != 0:
                errors.append(f"{section_name}: {count_name}={count}")
        findings = section.get("findings", [])
        if isinstance(findings, list):
            for finding in findings:
                if isinstance(finding, dict):
                    errors.append(
                        f"{section_name}: {finding.get('severity', 'unknown')} "
                        f"finding {finding.get('code', 'unknown')}"
                    )
        else:
            errors.append(f"{section_name}: findings must be an array")

    motion = report.get("motion")
    if isinstance(motion, dict):
        if motion.get("enabled") is not True:
            errors.append("motion: assertions were not enabled by a motion sidecar")
        samples = motion.get("samples")
        if not isinstance(samples, int) or samples < 1:
            errors.append("motion: no sampled motion assertions were evaluated")

    contrast = report.get("contrast")
    if isinstance(contrast, dict) and contrast.get("enabled") is not True:
        errors.append("contrast: contrast audit was not enabled")

    snapshots = report.get("snapshots")
    snapshot_files: list[str] = []
    if isinstance(snapshots, dict):
        if snapshots.get("enabled") is not True:
            errors.append("snapshots: screenshot evidence was not enabled")
        files = snapshots.get("files")
        if not isinstance(files, list) or len(files) < 5:
            errors.append("snapshots: at least five screenshot samples are required")
        else:
            snapshot_files = [str(item) for item in files]
    else:
        errors.append("Missing QA section: snapshots")

    if snapshot_root is not None:
        for relative_path in snapshot_files:
            candidate = Path(relative_path)
            if not candidate.is_absolute():
                candidate = snapshot_root / candidate
            if not candidate.is_file():
                errors.append(f"snapshots: missing screenshot file {relative_path}")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print(
            "Usage: validate_hyperframes_report.py <hyperframes-check.json>",
            file=sys.stderr,
        )
        return 2
    path = Path(args[0])
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"HYPERFRAMES QA: FAIL — cannot read report: {exc}", file=sys.stderr)
        return 2
    failures = validate_report(report, snapshot_root=Path.cwd())
    if failures:
        print("HYPERFRAMES QA: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("HYPERFRAMES QA: PASS")
    print("- strict mode, runtime, lint, layout, motion, contrast, craft and audio")
    print(f"- evaluated motion samples: {report['motion']['samples']}")
    print(f"- preserved frame samples: {len(report['snapshots']['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
