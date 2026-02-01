#!/usr/bin/env python3
import json
import random
from pathlib import Path
from datetime import datetime
import argparse


def load_json(path):
    """
    Unicode-safe JSON loader (matches export_repo.py approach).
    Tries UTF-8 variants first, then common fallbacks.
    """
    path = Path(path)
    data = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return json.loads(data.decode(enc))
        except Exception:
            continue
    return json.loads(data.decode("latin-1", errors="replace"))


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_active_pc_id(state: dict) -> str | None:
    pc_id = state.get("active_pc_id") or state.get("active_pc")
    if isinstance(pc_id, str) and pc_id.startswith("pc_"):
        return pc_id
    # fallback: first PC entry
    pcs = state.get("player_characters") or []
    if pcs and isinstance(pcs, list) and isinstance(pcs[0], dict):
        return pcs[0].get("id")
    return None


def resolve_pc_appearance_path(repo_root: Path, pc_id: str) -> Path:
    slug = pc_id.replace("pc_", "")
    return repo_root / "data" / "pcs" / "appearances" / f"{slug}_appearance.json"


def load_npc_metadata(repo_root: Path, npc_id: str) -> dict:
    """
    Best-effort NPC metadata loader.
    Checks data/npcs first, then data/npc_stat_sheets.
    """
    candidates = [
        repo_root / "data" / "npcs" / f"{npc_id}.json",
        repo_root / "data" / "npc_stat_sheets" / f"{npc_id}.json"
    ]
    for p in candidates:
        if p.exists():
            try:
                return load_json(p)
            except Exception:
                pass
    return {}


def infer_disposition(repo_root: Path, npc_id: str, state: dict) -> str:
    """
    Determine default disposition bucket: neutral | positive | negative
    based on civil war alignment + obvious faction tags.
    """
    npc = load_npc_metadata(repo_root, npc_id)
    player_alliance = (state.get("civil_war_state") or {}).get("player_alliance", "")
    player_alliance = (player_alliance or "").lower()

    # gather faction-ish signals from npc
    blobs = []
    for k in ("faction", "affiliation", "allegiance", "side", "tags", "keywords"):
        v = npc.get(k)
        if isinstance(v, str):
            blobs.append(v.lower())
        elif isinstance(v, list):
            blobs.append(" ".join([str(x).lower() for x in v]))
    blob = " ".join(blobs)

    if "thalmor" in blob:
        return "negative"

    if player_alliance == "stormcloak":
        if "imperial" in blob or "legion" in blob:
            return "negative"
        if "stormcloak" in blob:
            return "positive"

    if player_alliance == "imperial":
        if "stormcloak" in blob:
            return "negative"
        if "imperial" in blob or "legion" in blob:
            return "positive"

    return "neutral"


def maybe_first_impression(state_path, appearance_path, npc_id, disposition="neutral", force=False):
    """
    Records first impressions so NPCs can comment once, then recognize later.
    disposition: neutral|positive|negative (GM decides based on context)
    force: if True, overwrites an existing first impression for this npc->pc
    """
    state = load_json(state_path)
    appearance = load_json(appearance_path)

    state.setdefault("npc_first_impressions", {})
    state["npc_first_impressions"].setdefault(npc_id, {})

    pc_id = appearance.get("pc_id", "unknown_pc")

    # Already recorded? do nothing unless force.
    if (pc_id in state["npc_first_impressions"][npc_id]) and not force:
        return None

    lines = (appearance.get("first_impression_lines", {}) or {}).get(disposition, [])
    if not lines:
        lines = (appearance.get("first_impression_lines", {}) or {}).get("neutral", [])

    line = random.choice(lines) if lines else None

    state["npc_first_impressions"][npc_id][pc_id] = {
        "timestamp": datetime.now().isoformat(),
        "disposition": disposition,
        "line": line,
        "recognition_tags": appearance.get("recognition_tags", [])
    }

    save_json(state_path, state)
    return line


def auto_first_impression(repo_root, npc_id, disposition=None, force=False, quiet=False, trigger=None):
    """
    Convenience wrapper for the repo:
    - Reads state/campaign_state.json to find active PC
    - Finds PC appearance bark file
    - Infers disposition (unless explicitly provided)
    - Writes state.npc_first_impressions and returns the bark line
    - trigger parameter is accepted for compatibility but not used
    """
    repo_root = Path(repo_root).resolve()
    state_path = repo_root / "state" / "campaign_state.json"
    if not state_path.exists():
        raise FileNotFoundError(f"Missing campaign state: {state_path}")

    state = load_json(state_path)
    pc_id = resolve_active_pc_id(state)
    if not pc_id:
        if not quiet:
            print("No active PC found in campaign_state.json (active_pc_id/player_characters missing).")
        return None

    appearance_path = resolve_pc_appearance_path(repo_root, pc_id)
    if not appearance_path.exists():
        if not quiet:
            print(f"No appearance file found at: {appearance_path}")
            print("Create data/pcs/appearances/<slug>_appearance.json to enable NPC first-impression barks.")
        return None

    disp = disposition or infer_disposition(repo_root, npc_id, state)
    line = maybe_first_impression(state_path, appearance_path, npc_id, disposition=disp, force=force)

    if (line is not None) and (not quiet):
        print(f"[First Impression:{disp}] {npc_id} -> {pc_id}: {line}")

    return line


def main():
    ap = argparse.ArgumentParser(description="Record/emit NPC first-impression bark for the active PC.")
    ap.add_argument("--repo", default=".", help="Repo root (default: .)")
    ap.add_argument("--npc", required=True, help="NPC id (e.g., hadvar, ralof, elenwen)")
    ap.add_argument("--disposition", default=None, choices=["neutral", "positive", "negative"], help="Override inferred disposition bucket.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing impression if already recorded.")
    ap.add_argument("--quiet", action="store_true", help="Suppress console output.")
    args = ap.parse_args()

    auto_first_impression(args.repo, args.npc, disposition=args.disposition, force=args.force, quiet=args.quiet)


if __name__ == "__main__":
    main()
