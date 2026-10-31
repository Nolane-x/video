"""Compare local and cloud voice providers with one identical script.

Cloud synthesis is a potentially billable action. Google Cloud and ElevenLabs
are blocked unless the user explicitly passes --allow-cloud.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import random
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

from client import VoiceStudioClient
from voice_quality import compare_text
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
            language=language, speed=1.0,
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


def _cache_key(
    provider: str,
    candidate: dict[str, Any],
    text: str,
    *,
    engine: str | None,
    language: str,
    seed: int,
) -> str:
    identity = {
        "pipeline_schema": 1,
        "synthesis_settings": "provider-defaults-v1",
        "provider": provider,
        "voice_id": str(candidate.get("id") or ""),
        "engine": engine if provider == "voicestudio" else None,
        "language": language,
        "seed": seed if provider == "korva" else None,
        "script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    encoded = json.dumps(identity, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _safe_report_audio_path(output_dir: Path, relative: str | None) -> Path | None:
    if not relative:
        return None
    root = output_dir.resolve()
    try:
        candidate = (root / relative).resolve()
        candidate.relative_to(root)
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


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
            f"{row.get('provider', provider)} · {row.get('type', provider)} · {row.get('language') or ''}"
        )
        proxy = row.get("asr_intelligibility_proxy") or {}
        if proxy.get("status") == "available":
            metadata += html.escape(
                f" · ASR proxy WER {proxy['wer']:.1%} / CER {proxy['cer']:.1%}"
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
        notes = (
            '<label class="notes-label">Listener notes'
            '<textarea data-notes rows="3" placeholder="Why does this voice work or fail?"></textarea>'
            '</label>'
        )
        cards.append(
            f'<article data-label="{html.escape(str(row.get("blind_label") or row.get("id", "")), quote=True)}">'
            f'<h2>{safe_label}</h2><p class="meta">{metadata}</p>{audio}'
            f'<div class="ratings">{"".join(controls)}</div>{notes}</article>'
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
.notes-label{display:grid;gap:7px;margin-top:14px}.notes-label textarea{width:100%;box-sizing:border-box;min-height:72px;background:#303544;color:white;border:1px solid #555d70;border-radius:7px;padding:8px;font:inherit;resize:vertical}
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
    const notes=card.querySelector("[data-notes]").value.trim();
    return {candidate:card.dataset.label,ratings,mean,notes};
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
    asr: bool = False,
    blind_seed: int = 20261031,
    resume: bool = True,
    client: VoiceStudioClient | None = None,
) -> dict[str, Any]:
    valid_providers = {"voicestudio", "korva", "google", "elevenlabs", "all"}
    if provider not in valid_providers:
        raise ValueError(f"Unsupported provider selection: {provider}")
    if provider in {"google", "elevenlabs"} and not allow_cloud:
        raise ValueError(
            f"{provider} synthesis can incur charges; pass --allow-cloud to confirm the calls"
        )
    if provider == "all" and not engine:
        raise ValueError("Provider-wide benchmark needs the exact VoiceStudio --engine ID")
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
    requested_providers = (
        ["voicestudio", "korva", "google", "elevenlabs"]
        if provider == "all" and allow_cloud
        else ["voicestudio", "korva"]
        if provider == "all"
        else [provider]
    )
    candidates: list[dict[str, Any]] = []
    catalogue_errors: list[dict[str, str]] = []
    for provider_name in requested_providers:
        try:
            provider_candidates = _candidates(provider_name, language, client)[:limit]
            for candidate in provider_candidates:
                tagged = dict(candidate)
                tagged["_provider"] = provider_name
                candidates.append(tagged)
        except Exception as exc:
            catalogue_errors.append({
                "provider": provider_name,
                "error": f"{type(exc).__name__}: {exc}",
            })
    if not candidates:
        details = "; ".join(f"{row['provider']}: {row['error']}" for row in catalogue_errors)
        raise RuntimeError(
            f"No voices were found for language {language}" + (f" ({details})" if details else "")
        )

    # Sorting first makes the shuffled blind order reproducible across restarts,
    # even when provider catalogues return candidates in a different order.
    candidates.sort(key=lambda item: (
        str(item.get("_provider") or provider), str(item.get("id") or "")
    ))
    if blind:
        random.Random(blind_seed).shuffle(candidates)

    report_path = output_dir / "provider-voice-benchmark.json"
    previous_rows: dict[str, dict[str, Any]] = {}
    if resume and report_path.is_file():
        try:
            previous = json.loads(report_path.read_text(encoding="utf-8"))
            previous_rows = {
                str(row["cache_key"]): row
                for row in previous.get("candidates", [])
                if isinstance(row, dict) and row.get("cache_key")
            }
        except (OSError, ValueError, TypeError):
            previous_rows = {}

    rows: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates, 1):
        candidate_provider = str(candidate.get("_provider") or provider)
        voice_id = str(candidate.get("id") or "")
        name = str(candidate.get("name") or voice_id)
        blind_label = f"Candidate {index:02d}"
        extension = ".mp3" if candidate_provider == "elevenlabs" else ".wav"
        filename = (
            f"{index:03d}-{blind_label.replace(' ', '-')}{extension}"
            if blind else f"{index:03d}-{candidate_provider}-{_slug(voice_id)}{extension}"
        )
        cache_key = _cache_key(
            candidate_provider, candidate, text,
            engine=engine, language=language, seed=seed,
        )
        rows.append({
            "index": index,
            "id": voice_id,
            "name": name,
            "blind_label": blind_label,
            "provider": candidate_provider,
            "engine": engine if candidate_provider == "voicestudio" else None,
            "language": language,
            "status": "pending",
            "audio_file": (audio_dir / filename).relative_to(output_dir).as_posix(),
            "cache_key": cache_key,
            "cache_hit": False,
        })

    def snapshot(status: str) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "status": status,
            "provider": provider,
            "providers_included": requested_providers,
            "cloud_enabled": any(name in {"google", "elevenlabs"} for name in requested_providers),
            "asr_enabled": asr,
            "catalogue_errors": catalogue_errors,
            "engine": engine,
            "language": language,
            "blind": blind,
            "blind_seed": blind_seed,
            "resume_enabled": resume,
            "script": text,
            "script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "seed_base": seed,
            "candidate_count": len(rows),
            "ready": sum(row["status"] == "ready" for row in rows),
            "failed": sum(row["status"] == "failed" for row in rows),
            "pending": sum(row["status"] == "pending" for row in rows),
            "cache_hits": sum(row.get("cache_hit") is True for row in rows),
            "candidates": rows,
            "human_review_required": True,
            "rating_dimensions": [key for key, _ in DIMENSIONS],
            "rating_note": "Human ratings are subjective; do not treat the mean as an objective TTS benchmark.",
        }

    # Persist the complete plan before the first synthesis call. A killed run
    # can resume from the last atomic checkpoint instead of re-rendering voices.
    _write_json(report_path, snapshot("running"))
    for index, (candidate, row) in enumerate(zip(candidates, rows), 1):
        candidate_provider = row["provider"]
        destination = output_dir / row["audio_file"]
        previous = previous_rows.get(row["cache_key"])
        reused = False

        if resume and previous and previous.get("status") == "ready":
            cached_path = _safe_report_audio_path(
                output_dir, previous.get("audio_file")
            )
            if cached_path:
                try:
                    digest = hashlib.sha256(cached_path.read_bytes()).hexdigest()
                    if digest == previous.get("sha256") and cached_path.stat().st_size > 44:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        if cached_path.resolve() != destination.resolve():
                            shutil.copy2(cached_path, destination)
                        row.update({
                            "status": "ready",
                            "bytes": destination.stat().st_size,
                            "sha256": digest,
                            "cache_hit": True,
                        })
                        if asr and (previous.get("asr_intelligibility_proxy") or {}).get("status") == "available":
                            row["asr_intelligibility_proxy"] = previous["asr_intelligibility_proxy"]
                        reused = True
                        if asr and (row.get("asr_intelligibility_proxy") or {}).get("status") != "available":
                            try:
                                transcript = client.transcribe(destination, language=language)
                                row["asr_intelligibility_proxy"] = compare_text(text, transcript)
                                row["asr_intelligibility_proxy"]["status"] = "available"
                            except Exception as asr_exc:
                                row["asr_intelligibility_proxy"] = {
                                    "status": "unavailable",
                                    "reason": f"{type(asr_exc).__name__}: {asr_exc}",
                                }
                except OSError:
                    reused = False

        if not reused:
            try:
                path = _synthesize(
                    candidate_provider, candidate, text, destination,
                    engine=engine, language=language, seed=seed, client=client,
                )
                if not path.is_file() or path.stat().st_size <= 44:
                    raise RuntimeError("Provider returned no usable audio file")
                # Benchmark artifacts must stay inside the selected output folder.
                relative_audio = path.resolve().relative_to(output_dir.resolve())
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                row.update({
                    "status": "ready",
                    "audio_file": relative_audio.as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": digest,
                    "cache_hit": False,
                })
                if asr:
                    try:
                        transcript = client.transcribe(path, language=language)
                        row["asr_intelligibility_proxy"] = compare_text(text, transcript)
                        row["asr_intelligibility_proxy"]["status"] = "available"
                    except Exception as asr_exc:
                        row["asr_intelligibility_proxy"] = {
                            "status": "unavailable",
                            "reason": f"{type(asr_exc).__name__}: {asr_exc}",
                        }
            except Exception as exc:
                row["status"] = "failed"
                row["error"] = f"{type(exc).__name__}: {exc}"
        print(f"[{index}/{len(candidates)}] {row['blind_label']}: {row['status']}"
              + (" (resume cache)" if row.get("cache_hit") else ""))
        _write_json(report_path, snapshot("running"))
        if delay > 0 and index < len(candidates):
            time.sleep(delay)

    report = snapshot("partial" if any(row["status"] != "ready" for row in rows) else "complete")
    _write_json(report_path, report)
    (output_dir / "index.html").write_text(
        _rating_html(rows, blind=blind, provider=provider),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True,
                        choices=("voicestudio", "korva", "google", "elevenlabs", "all"))
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--language", default="vi")
    parser.add_argument("--engine", help="Exact VoiceStudio engine ID (provider=voicestudio)")
    parser.add_argument("--limit", type=int, default=20,
                        help="Maximum candidates per provider when --provider all is used")
    parser.add_argument("--seed", type=int, default=4200,
                        help="Provider seed where supported (e.g. KorvaTTS)")
    parser.add_argument("--blind-seed", type=int, default=20261031,
                        help="Deterministic shuffle seed for blind candidate order")
    parser.add_argument("--no-resume", action="store_true",
                        help="Render every candidate again even when a valid cached sample exists")
    parser.add_argument("--output", type=Path, default=Path("out/provider-voice-benchmark"))
    parser.add_argument("--no-blind", action="store_true")
    parser.add_argument("--allow-cloud", action="store_true",
                        help="Confirm Google/ElevenLabs synthesis API calls may be billed")
    parser.add_argument("--asr", action="store_true",
                        help="Round-trip every generated candidate through VoiceStudio ASR (WER/CER proxy)")
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()
    try:
        text = args.text_file.read_text(encoding="utf-8")
        report = run_benchmark(
            args.provider, text, args.output,
            language=args.language, engine=args.engine,
            limit=args.limit, seed=args.seed, blind=not args.no_blind,
            allow_cloud=args.allow_cloud, delay=args.delay, asr=args.asr,
        )
    except Exception as exc:
        print(f"Provider voice benchmark failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "report": str(args.output / "provider-voice-benchmark.json"),
        "provider": report["provider"],
        "ready": report["ready"],
        "failed": report["failed"],
        "cache_hits": report["cache_hits"],
        "status": report["status"],
        "blind": report["blind"],
        "human_review_required": True,
        "asr_enabled": report.get("asr_enabled", False),
    }, ensure_ascii=False, indent=2))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
