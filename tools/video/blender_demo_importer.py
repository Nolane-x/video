#!/usr/bin/env python3
"""Rights-screened importer for explicitly CC0 Blender demo projects and bundles."""
from __future__ import annotations

import hashlib
import io
import re
import time
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

CATALOG_URL = "https://www.blender.org/download/demo-files/"
LICENSE_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
UA = "NolaneVideoAssetLibrary/1.0 (+https://github.com/Nolane-x/video)"
MAX_CATALOG_BYTES = 12 * 1024 * 1024
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 320 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 12000
MAX_ARCHIVE_UNPACKED_BYTES = 512 * 1024 * 1024
OFFICIAL_HOSTS = {"www.blender.org", "download.blender.org"}
_ALLOWED_LICENSE = re.compile(r"\bCC0\b|\bCC[\s-]*0\b|\bCC[\s-]*BY(?:[\s-]*SA)?\b", re.IGNORECASE)

# Fixed, reviewed allowlist. A URL is not eligible merely because it is hosted by Blender:
# its exact title must also have a nearby CC0 marker on the current official catalog page.
ASSETS = (
    {
        "id": "human-base-meshes-v1-4-1",
        "title": "Human Base Meshes v1.4.1",
        "creator": "Blender Studio and community contributions",
        "category": "Human base meshes, character topology and rigging",
        "url": "https://www.blender.org/download/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip",
    },
    {
        "id": "cube-diorama",
        "title": "Cube Diorama",
        "creator": "Blender Studio",
        "category": "3D scene and asset bundle",
        "url": "https://www.blender.org/download/demo/bundles/bundles-3.0/asset-demo-bundle-3.0-cube-diorama.zip",
    },
    {
        "id": "animal-fur-examples",
        "title": "Animal Fur Examples",
        "creator": "Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, procedural fur and hair",
        "url": "https://www.blender.org/download/demo/geometry-nodes/hair_nodes-animal_fur_examples.blend",
    },
    {
        "id": "jiggly-pudding",
        "title": "Jiggly Pudding",
        "creator": "Mingwei Lim",
        "category": "Geometry Nodes, procedural animation",
        "url": "https://www.blender.org/download/demo/geometry-nodes/jiggly_pudding.blend",
    },
    {
        "id": "mesh-fracturing",
        "title": "Mesh Fracturing",
        "creator": "Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, destruction and simulation",
        "url": "https://www.blender.org/download/demo/geometry-nodes/simulation/mesh_fracturing.blend",
    },
    {
        "id": "particle-simulation",
        "title": "Particle Simulation",
        "creator": "Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, particles and simulation",
        "url": "https://www.blender.org/download/demo/geometry-nodes/simulation/basic_particle_simulation.blend",
    },
    {
        "id": "sample-uv-surface",
        "title": "Sample UV Surface",
        "creator": "Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, UV and surface workflows",
        "url": "https://www.blender.org/download/demo/geometry-nodes/geometry_nodes_sample_uv_surface.blend",
    },
    {
        "id": "pizza-delivery",
        "title": "Pizza Delivery",
        "creator": "Transform Sockets / Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, procedural scene",
        "url": "https://www.blender.org/download/demo/geometry-nodes/transform_socket-pizza_delivery.blend",
    },
    {
        "id": "impact-fracture",
        "title": "Impact Fracture",
        "creator": "Click Tools / Simon Thommes / Blender Studio",
        "category": "Geometry Nodes, fracture simulation",
        "url": "https://www.blender.org/download/demo/geometry-nodes/click_tools-impact_fracture.blend",
    },
    {
        "id": "tree-leaves-and-grass",
        "title": "Tree, leaves and grass",
        "creator": "Simon Thommes / Blender Studio",
        "category": "Procedural vegetation and environment assets",
        "url": "https://www.blender.org/download/demo/geometry-nodes/fields/tree_leaves_moss_geo-nodes-demo.blend",
    },
    {
        "id": "flower-scattering",
        "title": "Flower Scattering",
        "creator": "Blender Studio",
        "category": "Procedural vegetation and environment assets",
        "url": "https://www.blender.org/download/demo/geometry-nodes/fields/flower_scattering.blend",
    },
    {
        "id": "scattering-pebbles",
        "title": "Scattering Pebbles",
        "creator": "Blender Studio",
        "category": "Procedural environment assets",
        "url": "https://www.blender.org/download/demo/geometry-nodes/fields/pebble_scattering.blend",
    },
    {
        "id": "gizmo-array",
        "title": "Gizmo Array",
        "creator": "Simon Thommes",
        "category": "Geometry Nodes, procedural modelling",
        "url": "https://www.blender.org/download/demo/geometry-nodes/gizmo_array.blend",
    },
    {
        "id": "mandelbrot-grow",
        "title": "Mandelbrot Grow",
        "creator": "Shahzod Boyhonov",
        "category": "EEVEE, procedural graphics",
        "url": "https://www.blender.org/download/demo/eevee/mandelbrot_grow.blend",
    },
    {
        "id": "repeat-zone-raymarch-fractal",
        "title": "Repeat Zone Raymarch Fractal",
        "creator": "Cartesian Caramel",
        "category": "Shading, procedural fractals",
        "url": "https://www.blender.org/download/demo/rendering/repeat_zone_fractal_raymarch.blend",
    },
    {
        "id": "radial-tiling",
        "title": "Radial Tiling",
        "creator": "Johannes Kollmer",
        "category": "Shading, procedural patterns and textures",
        "url": "https://www.blender.org/download/demo/rendering/radial_tiling_texture.blend",
    },
    {
        "id": "xray-skeleton-arm",
        "title": "X-Ray Skeleton Arm",
        "creator": "Cartesian Caramel",
        "category": "EEVEE, stylised anatomy and visualisation",
        "url": "https://www.blender.org/download/demo/eevee/skeleton-arm-xray.blend",
    },
    {
        "id": "raycast-lines",
        "title": "Raycast Lines",
        "creator": "Andy Goralczyk / Miguel Pozo",
        "category": "Shading, procedural line graphics",
        "url": "https://download.blender.org/demo/rendering/raycast-line.blend",
    },
    {
        "id": "classroom",
        "title": "Classroom",
        "creator": "Christophe Seux",
        "category": "Architectural visualisation scene",
        "url": "https://www.blender.org/download/demo/test/classroom.zip",
    },
    {
        "id": "fishy-cat",
        "title": "Fishy Cat",
        "creator": "Manu Jarvinen",
        "category": "Character and stylised scene",
        "url": "https://www.blender.org/download/demo/test/splash_fishy_cat_2.zip",
    },
)


class _CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = next((value for key, value in attrs if key.lower() == "href" and value), None)
        if href:
            self.links.add(urljoin(CATALOG_URL, href))

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.text_parts.append(data.strip())


def official_blender_url_is_allowed(url: str) -> bool:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and parsed.hostname in OFFICIAL_HOSTS
        and parsed.username is None
        and parsed.password is None
        and not parsed.port
    )


def catalog_text_and_links(blob: bytes) -> tuple[str, set[str]]:
    if not blob or len(blob) > MAX_CATALOG_BYTES:
        raise ValueError("Blender demo catalog is empty or exceeds the metadata size budget")
    parser = _CatalogParser()
    parser.feed(blob.decode("utf-8", "replace"))
    text = re.sub(r"\s+", " ", " ".join(parser.text_parts)).strip()
    return text, parser.links


def catalog_cc0_evidence(catalog_text: str, title: str, *, max_context: int = 280) -> str | None:
    """Return the local catalog excerpt only when its first license marker is CC0."""
    folded = catalog_text.casefold()
    needle = re.sub(r"\s+", " ", title).strip().casefold()
    start = folded.find(needle)
    if start < 0:
        return None
    excerpt = catalog_text[start : start + max_context]
    marker = _ALLOWED_LICENSE.search(excerpt)
    if not marker:
        return None
    token = re.sub(r"[\s-]+", "", marker.group(0)).upper()
    if token != "CC0":
        return None
    return excerpt[:240].strip()


def _sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _read_bounded(url: str, limit: int) -> tuple[bytes, str, str]:
    if not official_blender_url_is_allowed(url):
        raise ValueError("URL is outside the official HTTPS Blender download hosts")
    request = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(request, timeout=45) as response:
        final_url = response.geturl()
        original = urlsplit(url)
        final = urlsplit(final_url)
        if (
            not official_blender_url_is_allowed(final_url)
            or final.hostname != original.hostname
            or final.path != original.path
        ):
            raise ValueError("Blender download redirected outside its exact official host/path")
        declared = response.headers.get("Content-Length")
        if declared:
            try:
                if int(declared) > limit:
                    raise ValueError("Blender resource exceeds its declared byte ceiling")
            except ValueError as exc:
                if "declared byte ceiling" in str(exc):
                    raise
        blob = response.read(limit + 1)
        if len(blob) > limit:
            raise ValueError("Blender resource exceeds its streaming byte ceiling")
        return blob, response.headers.get("Content-Type", ""), final_url


def _validate_project_blob(url: str, blob: bytes) -> tuple[str, int]:
    suffix = Path(urlsplit(url).path).suffix.lower()
    if suffix == ".blend":
        if not blob.startswith(b"BLENDER"):
            raise ValueError("downloaded .blend file does not have the Blender binary signature")
        return "blender-demo-cc0-project", 1
    if suffix != ".zip" or not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("only valid Blender project ZIP bundles or .blend files are accepted")
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = archive.infolist()
        if not members or len(members) > MAX_ARCHIVE_MEMBERS:
            raise ValueError("Blender ZIP member count is empty or exceeds the safety limit")
        unpacked = 0
        blend_count = 0
        for member in members:
            name = member.filename.replace("\\", "/")
            parts = PurePosixPath(name).parts
            if (
                not name
                or name.startswith("/")
                or any(part in {"", ".", ".."} for part in parts)
                or (member.external_attr >> 16) & 0o170000 == 0o120000
            ):
                raise ValueError("Blender ZIP contains an unsafe path or symbolic link")
            unpacked += int(member.file_size)
            if unpacked > MAX_ARCHIVE_UNPACKED_BYTES:
                raise ValueError("Blender ZIP expands beyond the uncompressed byte ceiling")
            if Path(name).suffix.lower() == ".blend":
                blend_count += 1
        if blend_count < 1:
            raise ValueError("Blender ZIP does not contain a .blend project file")
        if archive.testzip() is not None:
            raise ValueError("Blender ZIP failed its CRC integrity check")
    return "blender-demo-cc0-bundle", blend_count


def download_blender_demo_assets(root: Path, index: list[dict]) -> list[dict]:
    """Import only the fixed CC0 allowlist after checking live item-level catalog evidence."""
    root = Path(root)
    report: list[dict] = []
    try:
        catalog_blob, _, _ = _read_bounded(CATALOG_URL, MAX_CATALOG_BYTES)
        catalog_text, catalog_links = catalog_text_and_links(catalog_blob)
    except Exception as exc:
        return [{
            "id": "blender-demo-cc0-catalog",
            "status": "catalog_unavailable",
            "source_page": CATALOG_URL,
            "reason": str(exc)[:300],
        }]

    total_bytes = 0
    downloaded = 0
    for record in ASSETS:
        asset_id = str(record["id"])
        url = str(record["url"])
        evidence = catalog_cc0_evidence(catalog_text, str(record["title"]))
        if not evidence:
            report.append({
                "id": "blender-demo-" + asset_id,
                "status": "skipped_rights",
                "title": record["title"],
                "source_page": CATALOG_URL,
                "source_file_url": url,
                "reason": "The current official item listing did not show CC0 next to this exact allowlisted title.",
            })
            continue
        if url not in catalog_links or not official_blender_url_is_allowed(url):
            report.append({
                "id": "blender-demo-" + asset_id,
                "status": "skipped_unverified_url",
                "title": record["title"],
                "source_page": CATALOG_URL,
                "source_file_url": url,
                "reason": "The exact direct download link is no longer present on the official demo catalog.",
            })
            continue
        if total_bytes >= MAX_TOTAL_BYTES:
            report.append({
                "id": "blender-demo-" + asset_id,
                "status": "skipped_capacity",
                "title": record["title"],
                "reason": "The Blender CC0 lane reached its aggregate download ceiling.",
            })
            break
        try:
            blob, content_type, final_url = _read_bounded(url, min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total_bytes))
            asset_type, blend_count = _validate_project_blob(url, blob)
            filename = Path(urlsplit(url).path).name
            relative = Path("third-party") / "blender-demo-cc0" / (asset_id + Path(filename).suffix.lower())
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
            digest = _sha256(blob)
            entry = {
                "id": "blender-demo-" + asset_id,
                "path": relative.as_posix(),
                "type": asset_type,
                "provider": "Blender Foundation / Blender Studio",
                "title": record["title"],
                "creator": record["creator"],
                "category": record["category"],
                "source_page": CATALOG_URL,
                "source_file_url": final_url,
                "license": "CC0-1.0",
                "license_url": LICENSE_URL,
                "license_verified_from_current_official_catalog": True,
                "license_evidence": evidence,
                "attribution_required": False,
                "suggested_credit": f"{record['creator']} — Blender Demo Files",
                "size_bytes": len(blob),
                "sha256": digest,
                "archive_blend_project_count": blend_count if asset_type.endswith("bundle") else None,
                "content_type": content_type[:120],
                "redistributable": True,
            }
            index.append(entry)
            total_bytes += len(blob)
            downloaded += 1
            report.append({
                "id": entry["id"],
                "status": "downloaded",
                "path": entry["path"],
                "license": "CC0-1.0",
                "size_bytes": len(blob),
                "sha256": digest,
            })
            print("[Blender CC0] OK:", record["title"], len(blob), "bytes")
            time.sleep(0.12)
        except Exception as exc:
            report.append({
                "id": "blender-demo-" + asset_id,
                "status": "failed",
                "title": record["title"],
                "source_page": CATALOG_URL,
                "source_file_url": url,
                "reason": str(exc)[:320],
            })

    report.append({
        "id": "blender-demo-cc0-summary",
        "status": "summary",
        "downloaded_assets": downloaded,
        "downloaded_bytes": total_bytes,
        "allowlisted_assets": len(ASSETS),
        "license_gate": "exact item title + current CC0 marker + exact official catalog link",
    })
    return report
