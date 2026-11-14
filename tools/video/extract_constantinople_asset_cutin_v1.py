#!/usr/bin/env python3
"""Extract exact CC0 siege/castle assets from verified Build 76 ZIP volumes."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from io import BytesIO
from pathlib import Path

EXPECTED={
 "siege-tower.glb":"81909d6c33b181a9935fc7f800e8ee309454bbf99ff3b6b0ab2ecf16c3bf5e9b",
 "siege-ram.glb":"6473c77747b1d0a2c273d5a013454a0c85e5fc33b831150dced46d89b8ff9a5e",
 "siege-trebuchet.glb":"123711fd475e35d061738f648d9bf46c7f463d57681325c369977cee8954679a",
 "castle_brick_02_red_diff_1k.jpg":"526019deb0533920273a0a2272f7735ca17bb578427515c6b972e2bbecf5726c",
 "castle_brick_02_red_nor_gl_1k.jpg":"ab172b4bb8d9a2492774336f223e7725eecf1aae1efca2923c67db3e978106a6",
}
VOLUMES={
 "opengameart":{
  "file":"opengameart-3d-textures-001.zip",
  "sha256":"e8bd2ffc95fd2dfe647276c9d4d026e1ba5f24c65d08ebb87729cbb78da7ac1e",
  "bytes":994179162,
  "license":"CC0-1.0 Kenney Castle Kit",
  "source":"https://kenney.nl/assets/castle-kit"
 },
 "polyhaven":{
  "file":"polyhaven-3d-textures-001.zip",
  "sha256":"1573a65d9698375dbfd9bead9b8a551848a99f8cdba9dfd2b16c892319b5f7ef",
  "bytes":347196184,
  "license":"CC0-1.0 Poly Haven",
  "source":"https://polyhaven.com/a/castle_brick_02_red"
 }
}
def digest(path:Path)->str:
 h=hashlib.sha256()
 with path.open("rb") as f:
  for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
 return h.hexdigest()
def extract_suffix(z:zipfile.ZipFile,suffix:str,dest:Path,expected:str):
 matches=[n for n in z.namelist() if n.endswith(suffix)]
 if len(matches)!=1:
  raise RuntimeError(f"Expected one archive entry ending {suffix!r}; found {len(matches)}: {matches[:6]}")
 data=z.read(matches[0])
 got=hashlib.sha256(data).hexdigest()
 if got!=expected:raise RuntimeError(f"SHA mismatch for {suffix}: {got} != {expected}")
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 print("EXTRACTED",suffix,"bytes",len(data),"sha256",got,flush=True)
 return {"entry":matches[0],"path":str(dest),"bytes":len(data),"sha256":got}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--downloads",type=Path,required=True)
 ap.add_argument("--character",type=Path,required=True)
 ap.add_argument("--out",type=Path,required=True)
 a=ap.parse_args()
 out=a.out.resolve();models=out/"models";textures=out/"textures";char=out/"character"
 for key,meta in VOLUMES.items():
  zpath=a.downloads/meta["file"]
  assert zpath.stat().st_size==meta["bytes"],(zpath.stat().st_size,meta["bytes"])
  assert digest(zpath)==meta["sha256"],f"volume SHA mismatch: {zpath}"
  print("VERIFIED VOLUME",key,zpath.stat().st_size,meta["sha256"],flush=True)
 oga=zipfile.ZipFile(a.downloads/VOLUMES["opengameart"]["file"])
 nested=[n for n in oga.namelist() if n.endswith("kenney_castle-kit.zip")]
 if len(nested)>1:
  raise RuntimeError(f"Kenney Castle Kit nested ZIP candidates are ambiguous: {nested[:10]}")
 models_manifest={}
 if len(nested)==1:
  # Some older asset-library volumes preserve the original nested ZIP.
  inner_bytes=oga.read(nested[0])
  with zipfile.ZipFile(BytesIO(inner_bytes)) as inner:
   for name in ("siege-tower.glb","siege-ram.glb","siege-trebuchet.glb"):
    models_manifest[name]=extract_suffix(inner,"Models/GLB format/"+name,models/name,EXPECTED[name])
  payload_layout="nested-kenney-zip"
 else:
  # Build 76 stores the Castle Kit files directly under the former ZIP path;
  # the index retains the original archive name as a virtual path component.
  # Extract the exact GLB entries from the verified outer volume instead.
  for name in ("siege-tower.glb","siege-ram.glb","siege-trebuchet.glb"):
   models_manifest[name]=extract_suffix(oga,"Models/GLB format/"+name,models/name,EXPECTED[name])
  payload_layout="flattened-castle-kit-tree"
 ph=zipfile.ZipFile(a.downloads/VOLUMES["polyhaven"]["file"])
 texture_manifest={}
 for name in ("castle_brick_02_red_diff_1k.jpg","castle_brick_02_red_nor_gl_1k.jpg"):
  texture_manifest[name]=extract_suffix(ph,"castle_brick_02_red/"+name,textures/name,EXPECTED[name])
 char_src=a.character/"ottoman-artillery-crew-cc0.glb"
 char_manifest=a.character/"manifest.json"
 if not char_src.is_file() or not char_manifest.is_file():raise FileNotFoundError(a.character)
 cm=json.loads(char_manifest.read_text(encoding="utf-8"))
 if not str(cm.get("license","")).startswith("CC0-1.0") or cm.get("bones",0)<50:
  raise RuntimeError("Character provenance/rig gate failed")
 char.mkdir(parents=True,exist_ok=True)
 char_dst=char/char_src.name
 char_dst.write_bytes(char_src.read_bytes())
 char_manifest_dst=char/"manifest.json"
 char_manifest_dst.write_bytes(char_manifest.read_bytes())
 assert digest(char_dst)==digest(char_src)
 report={
  "status":"PASS",
  "asset_library_release":"video-asset-library-build-41184526545",
  "volume_verification":VOLUMES,
  "castle_kit_payload_layout":payload_layout,
  "models":models_manifest,
  "textures":texture_manifest,
  "character":{
   "file":char_dst.name,"license":cm["license"],"bones":cm["bones"],"actions":cm["actions"],
   "sha256":digest(char_dst),"source_run":43439300571,
   "costume_note":cm.get("costume_note","")
  },
  "historical_note":"The Kenney Castle Kit siege tower, siege ram and trebuchet are generic CC0 illustrative props, not authenticated Ottoman/Byzantine siege equipment from the 1453 siege. Do not caption them as exact historical replicas.",
 }
 out.mkdir(parents=True,exist_ok=True)
 (out/"CUTIN-ASSET-MANIFEST.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print("ASSET EXTRACTION PASS",json.dumps({"models":list(models_manifest),"textures":list(texture_manifest),"character_bones":cm["bones"]}),flush=True)
if __name__=="__main__":main()
