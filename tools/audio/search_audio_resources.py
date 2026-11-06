#!/usr/bin/env python3
"""Search Build 76 and Meta Open Sound audio metadata without unpacking source ZIPs."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CATALOGS = (
    Path("audio-library/generated/preview-catalog.json"),
    Path("audio-library/generated/meta-preview-catalog.json"),
)
REDISTRIBUTABLE = {"redistributable_candidate", "cc0_public_domain", "cc_by_4_attribution_required"}

def tokens(value: str) -> list[str]:
    return [x.casefold() for x in re.findall(r"[a-z0-9]+", value)]

def rights(item: dict[str, Any]) -> str:
    return str(item.get("rights_class") or item.get("rights_status") or item.get("license") or "review_required")

def fields(item: dict[str, Any]) -> dict[str, str]:
    tags = item.get("tags") or item.get("keywords") or []
    if isinstance(tags, str): tags = [tags]
    return {
        "title": str(item.get("title") or item.get("description") or "").casefold(),
        "category": str(item.get("category") or item.get("collection_kind") or "").casefold(),
        "tags": " ".join(str(x) for x in tags).casefold(),
        "file": " ".join(str(item.get(k) or "") for k in ("file_name","archive_name","archive_member","path")).casefold(),
        "source": " ".join(str(item.get(k) or "") for k in ("provider","collection","source_url","source_page","license")).casefold(),
        "credit": str(item.get("attribution_text") or "").casefold(),
    }

def token_variants(term: str) -> set[str]:
    aliases = {
        "hoof": {"hoof", "hooves"}, "hooves": {"hoof", "hooves"},
        "footstep": {"footstep", "footsteps"}, "footsteps": {"footstep", "footsteps"},
        "sword": {"sword", "swords"}, "swords": {"sword", "swords"},
        "arrow": {"arrow", "arrows"}, "arrows": {"arrow", "arrows"},
        "horse": {"horse", "horses"}, "horses": {"horse", "horses"},
    }
    if term in aliases:
        return aliases[term]
    if len(term) > 4 and term.endswith("s"):
        return {term, term[:-1]}
    return {term}

def score_item(item: dict[str, Any], query: str) -> tuple[int, list[str]]:
    terms=tokens(query)
    if not terms: return 1,[]
    f=fields(item)
    field_tokens={key:set(tokens(value)) for key,value in f.items()}
    all_tokens=set().union(*field_tokens.values())
    matched=[]
    for term in terms:
        variants=token_variants(term)
        if not (variants & all_tokens):
            return 0,[]
        matched.append(term)
    score=0
    weights={"title":6,"category":4,"tags":4,"file":2,"source":1,"credit":1}
    for term in terms:
        variants=token_variants(term)
        score += sum(weights[key] for key,values in field_tokens.items() if variants & values)
    return score,matched

def search_catalogs(catalog_paths: Iterable[Path], query: str, *, limit:int=30,
                    include_review_required:bool=False, only_auditioned:bool=False,
                    kind:str|None=None) -> list[dict[str,Any]]:
    if limit<1: raise ValueError("limit must be at least 1")
    results=[]; seen=set()
    for cp in catalog_paths:
        if not cp.is_file(): continue
        data=json.loads(cp.read_text(encoding="utf-8"))
        for raw in data.get("assets",[]):
            status=rights(raw)
            if not include_review_required and status not in REDISTRIBUTABLE: continue
            heard=bool(raw.get("auditioned_by_human",raw.get("auditioned",False)))
            if only_auditioned and not heard: continue
            item_kind=str(raw.get("collection_kind") or raw.get("kind") or "").casefold()
            if kind and item_kind!=kind.casefold(): continue
            score,matched=score_item(raw,query)
            if score<=0: continue
            unique=(str(raw.get("asset_id") or raw.get("id") or ""),str(raw.get("source_url") or raw.get("source_page") or ""),str(raw.get("archive_member") or raw.get("path") or ""))
            if unique in seen: continue
            seen.add(unique)
            out=dict(raw); out["catalog"]=cp.stem; out["rights_status_normalized"]=status
            out["search_score"]=score; out["matched_terms"]=matched
            out["audition_status"]="HUMAN_AUDITIONED" if heard else "NOT_AUDITIONED"
            out["final_use_gate"]="human_audition_and_item_level_rights_check_required" if not heard else "project_context_and_mix_check"
            out["recommended_use"]=("instrument_sample_not_finished_music" if item_kind=="instrument" else "foley_or_ambience_candidate" if item_kind=="foley" else "recorded_audio_candidate")
            results.append(out)
    results.sort(key=lambda x:(-x["search_score"],str(x.get("title") or "").casefold(),str(x.get("archive_member") or x.get("path") or "").casefold()))
    return results[:limit]

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query",required=True,help='e.g. "katana sword clash", "horse hooves", "rain roof"')
    p.add_argument("--catalog",type=Path,action="append",default=None)
    p.add_argument("--limit",type=int,default=30)
    p.add_argument("--include-review-required",action="store_true")
    p.add_argument("--only-auditioned",action="store_true")
    p.add_argument("--kind",choices=("foley","instrument"))
    p.add_argument("--json",action="store_true")
    a=p.parse_args(); paths=a.catalog or DEFAULT_CATALOGS
    missing=[str(x) for x in paths if not x.is_file()]
    if missing:
        print("Missing catalog(s): "+", ".join(missing),file=sys.stderr)
        print("Run the build-cinematic-audio-library GitHub Actions workflow first.",file=sys.stderr)
        return 2
    results=search_catalogs(paths,a.query,limit=a.limit,include_review_required=a.include_review_required,only_auditioned=a.only_auditioned,kind=a.kind)
    if a.json: print(json.dumps(results,ensure_ascii=False,indent=2))
    else:
        for x in results:
            title=x.get("title") or x.get("file_name") or x.get("archive_member") or "Untitled"
            print(f"{title} | {x.get('collection_kind') or x.get('category') or ''} | {x['rights_status_normalized']}")
            print(f"  {x.get('archive_name') or x.get('collection','unknown')} :: {x.get('archive_member') or x.get('path') or x.get('file_name','')}")
            print(f"  audition={x['audition_status']} | {x['recommended_use']} | score={x['search_score']}")
            if x.get("attribution_text"): print("  attribution="+x["attribution_text"])
            if x.get("source_url"): print("  source="+x["source_url"])
            print()
    print(f"Matches: {len(results)} (search never approves an unauditioned sample)",file=sys.stderr)
    return 0

if __name__=="__main__": raise SystemExit(main())
