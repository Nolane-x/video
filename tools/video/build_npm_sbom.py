#!/usr/bin/env python3
"""Create a small CycloneDX 1.5 SBOM from npm package-lock v2/v3."""
from __future__ import annotations
import argparse
import json
import uuid
from pathlib import Path

def package_name_from_path(path: str) -> str | None:
    marker = "node_modules/"
    if marker not in path: return None
    return path.rsplit(marker, 1)[1]

def build(lock: dict) -> dict:
    components = []
    for location, info in sorted(lock.get("packages", {}).items()):
        if not location: continue
        name = info.get("name") or package_name_from_path(location)
        version = info.get("version")
        if not name or not version: continue
        purl = f"pkg:npm/{name.replace('@', '%40', 1) if name.startswith('@') else name}@{version}"
        component = {"type":"library","bom-ref":purl,"name":name,"version":version,"purl":purl}
        license_value = info.get("license")
        if isinstance(license_value, str): component["licenses"] = [{"license":{"id":license_value}}]
        elif isinstance(license_value, dict): component["licenses"] = [{"license":license_value}]
        components.append(component)
    return {
      "bomFormat":"CycloneDX","specVersion":"1.5","serialNumber":f"urn:uuid:{uuid.uuid4()}","version":1,
      "metadata":{"component":{"type":"application","name":lock.get("name","nolane-video-toolchain"),"version":lock.get("version","0.0.0")}},
      "components":components
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    lock = json.loads(Path(args.input).read_text(encoding='utf-8'))
    bom = build(lock)
    if not bom['components']: raise SystemExit('package-lock contains no resolved components')
    Path(args.output).write_text(json.dumps(bom, indent=2) + '\n', encoding='utf-8')
    print(f"CycloneDX 1.5 SBOM: {len(bom['components'])} components -> {args.output}")
    return 0
if __name__ == '__main__': raise SystemExit(main())
