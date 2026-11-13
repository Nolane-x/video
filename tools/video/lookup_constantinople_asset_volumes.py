#!/usr/bin/env python3
"""Resolve exact Build 76 resource hashes/paths to the release ZIP volume map."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

TARGETS = [
    {
        "label": "CC0 Castle Kit siege tower GLB",
        "sha256": "81909d6c33b181a9935fc7f800e8ee309454bbf99ff3b6b0ab2ecf16c3bf5e9b",
        "path": "third-party/opengameart/3d/castle-kit-7f94b54084e1/kenney_castle-kit.zip/Models/GLB format/siege-tower.glb",
    },
    {
        "label": "CC0 Castle Kit siege ram GLB",
        "sha256": "6473c77747b1d0a2c273d5a013454a0c85e5fc33b831150dced46d89b8ff9a5e",
        "path": "third-party/opengameart/3d/castle-kit-7f94b54084e1/kenney_castle-kit.zip/Models/GLB format/siege-ram.glb",
    },
    {
        "label": "CC0 Castle Kit demolished siege tower GLB",
        "sha256": "6504a432e6e72a51c75f862ea08e144058727add6eb0f76dc7d9f7352e8a23d0",
        "path": "third-party/opengameart/3d/castle-kit-7f94b54084e1/kenney_castle-kit.zip/Models/GLB format/siege-tower-demolished.glb",
    },
    {
        "label": "CC0 Castle Kit siege trebuchet GLB",
        "sha256": "123711fd475e35d061738f648d9bf46c7f463d57681325c369977cee8954679a",
        "path": "third-party/opengameart/3d/castle-kit-7f94b54084e1/kenney_castle-kit.zip/Models/GLB format/siege-trebuchet.glb",
    },
    {
        "label": "CC0 Poly Haven castle brick normal DirectX",
        "sha256": "b125c181ae256f2cd32d128cfe66a189d9864c55612566d640a9ece422ed6c77",
        "path": "third-party/polyhaven/textures/castle_brick_02_red/castle_brick_02_red_nor_dx_1k.jpg",
    },
    {
        "label": "CC0 Poly Haven castle brick normal OpenGL",
        "sha256": "ab172b4bb8d9a2492774336f223e7725eecf1aae1efca2923c67db3e978106a6",
        "path": "third-party/polyhaven/textures/castle_brick_02_red/castle_brick_02_red_nor_gl_1k.jpg",
    },
    {
        "label": "CC0 Poly Haven castle brick diffuse",
        "sha256": "526019deb0533920273a0a2272f7735ca17bb578427515c6b972e2bbecf5726c",
        "path": "third-party/polyhaven/textures/castle_brick_02_red/castle_brick_02_red_diff_1k.jpg",
    },
]

VOLUME_WORDS = ("volume", "archive", "zip", "release", "download", "asset", "sha", "hash", "path", "file", "url", "size")

def compact(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if isinstance(v, (str, int, float, bool)) or v is None:
                if any(w in str(k).casefold() for w in VOLUME_WORDS):
                    out[str(k)] = v
            elif isinstance(v, list) and len(v) <= 12 and all(isinstance(x, (str, int, float, bool)) or x is None for x in v):
                if any(w in str(k).casefold() for w in VOLUME_WORDS):
                    out[str(k)] = v
        return out
    return {"value": str(node)[:1000]}

def walk(node, trail="$"):
    if isinstance(node, dict):
        yield node, trail
        for k, v in node.items():
            yield from walk(v, f"{trail}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{trail}[{i}]")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--map",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    raw=args.map.read_bytes()
    data=json.loads(raw)
    results={t["sha256"]:{"target":t,"matches":[]} for t in TARGETS}
    by_path={t["path"]:t["sha256"] for t in TARGETS}
    for row,trail in walk(data):
        candidates=[]
        for key,value in row.items():
            if isinstance(key,str) and key in results:
                candidates.append(key)
            if isinstance(value,str) and value in results:
                candidates.append(value)
            if isinstance(value,str) and value in by_path:
                candidates.append(by_path[value])
        if not candidates:
            # Search a compact serialization only for this small set of exact IDs.
            text=json.dumps(row,ensure_ascii=False)
            for target in TARGETS:
                if target["sha256"] in text or target["path"] in text:
                    candidates.append(target["sha256"])
        for sha in set(candidates):
            excerpt=compact(row)
            entry={"trail":trail,"fields":excerpt}
            signature=json.dumps(entry,sort_keys=True,ensure_ascii=False)
            if all(json.dumps(x,sort_keys=True,ensure_ascii=False)!=signature for x in results[sha]["matches"]):
                results[sha]["matches"].append(entry)
    summary={
        "status":"PASS",
        "map_bytes":len(raw),
        "map_sha256":__import__("hashlib").sha256(raw).hexdigest(),
        "target_count":len(TARGETS),
        "resolved_count":sum(bool(x["matches"]) for x in results.values()),
        "targets":list(results.values()),
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":summary["status"],"map_bytes":summary["map_bytes"],
        "resolved_count":summary["resolved_count"],
        "targets":[{"label":x["target"]["label"],"matches":len(x["matches"])} for x in summary["targets"]]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
