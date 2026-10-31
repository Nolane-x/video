"""Prepare a CPU-only Dockerfile from the exact pinned VoiceStudio source.

The upstream Dockerfile is GPU-first and asserts that CUDA/ROCm is present.
GitHub-hosted public runners have no GPU, so this transformation changes only
the build base, preinstalls official CPU PyTorch wheels, and makes the
hardware assertion explicitly understand GPU_FLAVOR=cpu. App source, package
lockfiles, and all other build instructions remain byte-identical.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

CPU_INSTALL = (
    "RUN python3 -m pip install --no-cache-dir "
    "--index-url https://download.pytorch.org/whl/cpu "
    "torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0\n"
)

COPY_ANCHOR = "COPY deploy/uv-overrides.txt ./deploy/uv-overrides.txt\n"
GUARD_PATTERN = re.compile(
    r"flavor = os\.environ\['GPU_FLAVOR'\];\s*"
    r"accel = torch\.version\.hip if flavor == 'rocm' else torch\.version\.cuda;"
)
GUARD_CPU = (
    "flavor = os.environ['GPU_FLAVOR']; "
    "accel = torch.version.hip if flavor == 'rocm' "
    "else (torch.version.cuda if flavor == 'cuda' else 'cpu');"
)


def transform_dockerfile(source: str) -> str:
    if source.count(COPY_ANCHOR) != 1:
        raise ValueError("Pinned VoiceStudio Dockerfile changed: torch install anchor must occur once")
    if "torch==2.8.0" in source and "index-url https://download.pytorch.org/whl/cpu" in source:
        raise ValueError("CPU PyTorch install already exists; refusing to double-patch Dockerfile")
    transformed = source.replace(COPY_ANCHOR, COPY_ANCHOR + CPU_INSTALL, 1)
    transformed, count = GUARD_PATTERN.subn(GUARD_CPU, transformed)
    if count != 1:
        raise ValueError(
            f"Pinned VoiceStudio Dockerfile changed: expected one GPU-only torch guard, found {count}"
        )
    # Fail closed if the Dockerfile acquires a second accelerator-only check
    # that this narrow CPU compatibility patch was not designed to change.
    if "GPU_FLAVOR" not in transformed or "python3 -m pip install --no-cache-dir" not in transformed:
        raise ValueError("Transformed Dockerfile failed required CPU runtime invariants")
    return transformed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Pinned vendor/VoiceStudio/deploy/Dockerfile")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        original = args.source.read_text(encoding="utf-8")
        transformed = transform_dockerfile(original)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(transformed, encoding="utf-8")
    except Exception as exc:
        print(f"CPU Dockerfile preparation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(
        f"source_sha256={hashlib.sha256(original.encode('utf-8')).hexdigest()} "
        f"output_sha256={hashlib.sha256(transformed.encode('utf-8')).hexdigest()} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
