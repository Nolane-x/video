"""Compare local and cloud voice providers with one identical script.

Cloud synthesis is a potentially billable action. Google Cloud and ElevenLabs
are blocked unless the user explicitly passes --allow-cloud.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from client import VoiceStudioClient
from providers import google_cloud, korva, elevenlabs
from voice_audition import _language_matches


DIMENSIONS = [
    ("naturalness", "Naturalness"),
    ("vietnamese", "Vietnamese pronunciation and tones"),
    ("identity", "Stable speaker identity"),
    ("expression", "Emotion and expressive delivery"),
    ("character_fit", "Fit for the intended character"),
]


def _candidates(provider: str, language: str, client: VoiceStudioClient) -> list[dict[str, Any]]:
    if provider == "voicestudio":
        raw = client.list_profiles()
        items = raw if isinstance(raw, list) else raw.get("items", raw.get("profiles", []))
        return [
            {
                "id": str(row.get("id")),
                "name": str(row.get("name") or row.get("id")),
                "language": row.get("language"),
                "type": row.get("kind") or "saved_profile",
            }
            for row in items
            if isinstance(row, dict)
            and row.get("id")
            and _language_matches(row.get("language"), language)
        ]
    if provider == "korva":
        return korva.list_voices(language)
    if provider == "google":
        return google_cloud.list_voices(language)
    if provider == "elevenlabs":
        return elevenlabs.list_voices(language)
    raise ValueError(f"Unsupported provider: {provider}")


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-_")[:72] or "candidate"


def _synthesize(
    provider: str,
    candidate: dict[str, Any],
    text: str,
    destination: Path,
    *,
    engine: str | None,
    language: str,
    seed: int,
    client: VoiceStudioClient,
) -> Path:
    voice_id = str(candidate.get("id") or "")
    if not voice_id:
        raise ValueError("Provider catalogue entry has no voice ID")
    if provider == "voicestudio":
        if not engine:
            raise ValueError("VoiceStudio benchmark requires an exact --engine ID")
        return client.synthesize(
            text, destination, engine=engine, voice=voice_id,
            language=language, speed=1.0, seed=seed,
        )
    if provider == "korva":
        return korva.synthesize(
            text, voice_id, destination, language=language,
            speed=1.0, seed=seed,
            settings={"total_steps": 32, "num_threads": 4},
        )
    if provider == "google":
        return google_cloud.synthesize(
            text, voice_id, destination,
            language=language, speed=1.0,
            settings={"audio_encoding": "LINEAR16"},
        )
    if provider == "elevenlabs":
        return elevenlabs.synthesize(
            text, voice_id, destination,
            language=language, speed=1.0,
            settings={"model_id": "eleven_flash_v2_5"},
        )
    raise ValueError(f"Unsupported provider: {provider}")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    temporary.replace(path)


def _rating_html(rows: list[dict[str, Any]], *, blind: bool, provider: str) -> str:
    cards = []
    for row in rows:
        label = row.get("blind_label") if blind else row.get("name", "Voice")
        safe_label = html.escape(str(label or row.get("id", "Voice")))
        metadata = "Blind listening candidate" if blind else html.escape(
            f"{row.get('type', provider)} · {row.get('language') or ''}"
        )
        if row.get("audio_file"):
            audio = f'<audio controls preload="none" src="{html.escape(row["audio_file"], quote=True)}"></audio>'
        else:
            audio = f'<p class="error">{html.escape(str(row.get("error", "Audio unavailable")))}</p>'
        controls = []
        for key, title in DIMENSIONS:
            options = "".join(
                f'<option value="{score}">{score}</option>'
                for score in range(1, 6)
            )
            controls.append(
                f'<label>{html.escape(title)}<select data-dimension="{key}">'
                f'<option value="">Unrated</option>{options}</select></label>'
            )
        cards.append(
            f'<article data-label="{html.escape(str(row.get("blind_label") or row.get("id", "")), quote=True)}">'
            f'<h2>{safe_label}</h2><p class="meta">{metadata}</p>{audio}'
            f'<div class="ratings">{"".join(controls)}</div></article>'
        )
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nolane provider voice benchmark</title>
<style>
:root{color-scheme:dark;background:#11131a;color:#f1f2f5;font:15px system-ui,sans-serif}
body{max-width:1180px;margin:30px auto;padding:0 18px}
header{margin-bottom:24px}h1{font-size:27px;margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
article{background:#1d202a;border:1px solid #363a46;border-radius:14px;padding:16px;min-width:0}
h2{font-size:17px;margin:0 0 6px}.meta,.notice{color:#aeb5c5;font-size:13px}
audio{width:100%;margin:14px 0}.ratings{display:grid;gap:8px}
label{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px}
select{background:#303544;color:white;border:1px solid #555d70;border-radius:6px;padding:5px}
button{margin:20px 0;background:#e8eaf1;color:#151821;border:0;border-radius:8px;padding:10px 16px;font-weight:650;cursor:pointer}
.error{color:#ffadad;overflow-wrap:anywhere}
</style></head><body>
<header><h1>Nolane voice provider benchmark</h1>
<p class="notice">All candidates use the same script and nominal speed. Listen to the complete samples before rating. This is a human comparison sheet, not an automated quality claim.</p>
</header><main class="grid">""" + "\n".join(cards) + """</main>
<button id="export">Export human ratings JSON</button>
<script>
document.getElementById("export").addEventListener("click",()=>{
  const dimensions=["naturalness","vietnamese","identity","expression","character_fit"];
  const rows=[...document.querySelectorAll("article")].map(card=>{
    const ratings={};
    for(const key of dimensions){
      const value=card.querySelector('[data-dimension="'+key+'"]').value;
      ratings[key]=value?Number(value):null;
    }
    const values=Object.values(ratings).filter(v=>v!==null);
    const mean=values.length?values.reduce((a,b)=>a+b,0)/values.length:null;
    return {candidate:card.dataset.label,ratings,mean};
  });
  const data={schema_version:1,provider:"BENCHMARK_PROVIDER",ratings:rows,
    note:"Subjective human ratings; not a validated naturalness metric."};
  const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob);const a=document.createElement("a");
  a.href=url;a.download="voice-human-ratings.json";a.click();URL.revokeObjectURL(url);
});
</script></body></html>""".replace("BENCHMARK_PROVIDER", html.escape(provider))


def run_benchmark(
    provider: str,
    text: str,
    output_dir: Path,
    *,
    language: str = "vi",
    engine: str | None = None,
    limit: int = 20,
    seed: int = 4200,
    blind: bool = True,
    allow_cloud: bool = False,
    delay: float = 0.5,
    client: VoiceStudioClient | None = None,
) -> dict[str, Any]:
    if provider in {"google", "elevenlabs"} and not allow_cloud:
        raise ValueError(
            f"{provider} synthesis can incur charges; pass --allow-cloud to confirm the calls"
        )
    if provider == "voicestudio" and not engine:
        raise ValueError("VoiceStudio benchmark needs the exact installed --engine ID")
    if not text.strip() or len(text) > 4096:
        raise ValueError("Benchmark script must contain 1–4096 characters")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    if delay < 0:
        raise ValueError("delay must be non-negative")
    client = client or VoiceStudioClient()
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    candidates = _candidates(provider, language, client)[:limit]
    if not candidates:
        raise RuntimeError(f"No {provider} voices were found for language {language}")
    rows: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates, 1):
        voice_id = str(candidate.get("id") or "")
        name = str(candidate.get("name") or voice_id)
        blind_label = f"Candidate {index:02d}"
        extension = ".mp3" if provider == "elevenlabs" else ".wav"
        filename = (
            f"{index:03d}-{blind_label.replace(' ', '-')}{extension}"
            if blind else f"{index:03d}-{_slug(voice_id)}{extension}"
        )
        destination = audio_dir / filename
        row: dict[str, Any] = {
            "index": index,
            "id": voice_id,
            "name": name,
            "blind_label": blind_label,
            "provider": provider,
            "engine": engine,
            "language": language,
            "status": "pending",
        }
        try:
            path = _synthesize(
                provider, candidate, text, destination,
                engine=engine, language=language, seed=seed, client=client,
            )
            if not path.is_file() or path.stat().st_size <= 44:
                raise RuntimeError("Provider returned no usable audio file")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            row.update({
                "status": "ready",
                "audio_file": path.relative_to(output_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest,
            })
        except Exception as exc:
            row["status"] = "failed"
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
        print(f"[{index}/{len(candidates)}] {blind_label}: {row['status']}")
        if delay > 0 and index < len(candidates):
            time.sleep(delay)

    report = {
        "schema_version": 1,
        "provider": provider,
        "engine": engine,
        "language": language,
        "blind": blind,
        "script": text,
        "seed_base": seed,
        "candidate_count": len(rows),
        "ready": sum(row["status"] == "ready" for row in rows),
        "failed": sum(row["status"] == "failed" for row in rows),
        "candidates": rows,
        "human_review_required": True,
        "rating_dimensions": [key for key, _ in DIMENSIONS],
        "rating_note": "Human ratings are subjective; do not treat the mean as an objective TTS benchmark.",
    }
    _write_json(output_dir / "provider-voice-benchmark.json", report)
    (output_dir / "index.html").write_text(
        _rating_html(rows, blind=blind, provider=provider),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True,
                        choices=("voicestudio", "korva", "google", "elevenlabs"))
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--language", default="vi")
    parser.add_argument("--engine", help="Exact VoiceStudio engine ID (provider=voicestudio)")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--seed", type=int, default=4200)
    parser.add_argument("--output", type=Path, default=Path("out/provider-voice-benchmark"))
    parser.add_argument("--no-blind", action="store_true")
    parser.add_argument("--allow-cloud", action="store_true",
                        help="Confirm Google/ElevenLabs synthesis API calls may be billed")
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()
    try:
        text = args.text_file.read_text(encoding="utf-8")
        report = run_benchmark(
            args.provider, text, args.output,
            language=args.language, engine=args.engine,
            limit=args.limit, seed=args.seed, blind=not args.no_blind,
            allow_cloud=args.allow_cloud, delay=args.delay,
        )
    except Exception as exc:
        print(f"Provider voice benchmark failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "report": str(args.output / "provider-voice-benchmark.json"),
        "provider": report["provider"],
        "ready": report["ready"],
        "failed": report["failed"],
        "blind": report["blind"],
        "human_review_required": True,
    }, ensure_ascii=False, indent=2))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
