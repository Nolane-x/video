from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prepare_voicestudio_cpu_dockerfile import transform_dockerfile


class PrepareVoiceStudioCpuDockerfileTests(unittest.TestCase):
    def source(self):
        return """ARG BASE_IMAGE=pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime
FROM ${BASE_IMAGE} AS runtime
COPY deploy/torch-constraints.txt ./deploy/torch-constraints.txt
COPY deploy/uv-overrides.txt ./deploy/uv-overrides.txt
RUN uv pip install --python \"$(command -v python3)\" --no-cache .
ARG GPU_FLAVOR=cuda
RUN python3 -c \"import os, torch; flavor = os.environ['GPU_FLAVOR']; accel = torch.version.hip if flavor == 'rocm' else torch.version.cuda; assert accel\"
"""

    def test_adds_official_cpu_wheels_and_cpu_hardware_guard(self):
        transformed = transform_dockerfile(self.source())
        self.assertIn("--index-url https://download.pytorch.org/whl/cpu", transformed)
        self.assertIn("torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0", transformed)
        self.assertIn("else (torch.version.cuda if flavor == 'cuda' else 'cpu')", transformed)
        self.assertLess(
            transformed.index("torch==2.8.0 torchvision"),
            transformed.index("RUN uv pip install"),
        )
        self.assertEqual(transformed.count("torch==2.8.0 torchvision"), 1)

    def test_fails_closed_when_upstream_copy_anchor_changes(self):
        altered = self.source().replace(
            "COPY deploy/uv-overrides.txt ./deploy/uv-overrides.txt",
            "COPY deploy/new-overrides.txt ./deploy/new-overrides.txt",
        )
        with self.assertRaisesRegex(ValueError, "install anchor"):
            transform_dockerfile(altered)

    def test_fails_closed_when_hardware_guard_changes(self):
        altered = self.source().replace(
            "flavor = os.environ['GPU_FLAVOR']; accel = torch.version.hip if flavor == 'rocm' else torch.version.cuda;",
            "flavor = os.environ['GPU_FLAVOR']; accel = True;",
        )
        with self.assertRaisesRegex(ValueError, "GPU-only torch guard"):
            transform_dockerfile(altered)

    def test_fails_instead_of_inserting_duplicate_cpu_runtime(self):
        altered = self.source().replace(
            "COPY deploy/uv-overrides.txt ./deploy/uv-overrides.txt\n",
            "COPY deploy/uv-overrides.txt ./deploy/uv-overrides.txt\n"
            "RUN python3 -m pip install --no-cache-dir --index-url "
            "https://download.pytorch.org/whl/cpu torch==2.8.0\n",
        )
        with self.assertRaisesRegex(ValueError, "already exists"):
            transform_dockerfile(altered)


if __name__ == "__main__":
    unittest.main()
