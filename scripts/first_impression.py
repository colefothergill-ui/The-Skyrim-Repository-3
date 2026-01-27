#!/usr/bin/env python3
"""
First Impression System (PC meets NPC)

GOALS:
- When Aldric meets an NPC for the first time, generate a short NPC-flavored comment
  about Aldric's look (handsomeness, attire, physique, tells).
- Record the meeting so it only triggers once unless forced.
- Store meeting in:
  - PC sheet: data/pcs/<pc>.json -> relationships.met_npcs
  - Campaign state: state/campaign_state.json -> world_consequences.npcs_met (if exists)

This is intentionally light-weight and heuristic-driven (string matching on NPC roles/aspects).
"""

import json
import argparse
import os
from pathlib import Path
from datetime import datetime


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def auto_pick_single_pc(pcs_dir: Path):
    pcs = [p for p in pcs_dir.glob("pc_*.json") if p.name != "example_pc.json"]
    if len(pcs) == 1:
        return pcs[0]
    return None


def get_pc_path(repo_root: Path, pc_id: str | None):
    pcs_dir = repo_root / "data" / "pcs"
    # explicit
    if pc_id:
        p = pcs_dir / f"{pc_id}.json"
        if p.exists():
            return p
    # env fallback
    env_id = os.environ.get("PC_ID")
    if env_id:
        p = pcs_dir / f"{env_id}.json"
        if p.exists():
            return p
    # auto fallback
    auto = auto_pick_single_pc(pcs_dir)
    if auto:
        return auto
    return None


def get_npc_meta(repo_root: Path, npc_id: str):
    # prefer stat sheet (richer "aspects" and "category/type" patterns)
    stat_path = repo_root / "data" / "npc_stat_sheets" / f"{npc_id}.json"
    if stat_path.exists():
        s = load_json(stat_path)
        return {
            "id": npc_id,
            "name": s.get("name", npc_id),
            "type": s.get("type", ""),
            "category": s.get("category", ""),
            "aspects": s.get("aspects", {}),
        }

    npc_path = repo_root / "data" / "npcs" / f"{npc_id}.json"
    if npc_path.exists():
        n = load_json(npc_path)
        return {
            "id": npc_id,
            "name": n.get("name", npc_id),
            "type": n.get("role", n.get("type", "")),
            "category": "NPC",
            "aspects": n.get("aspects", {}),
        }

    raise FileNotFoundError(f"NPC not found in data/npc_stat_sheets/ or data/npcs/: {npc_id}")


def load_visual_profile(repo_root: Path, pc: dict):
    ref = pc.get("visual_profile_ref")
    if not ref:
        return None
    vp_path = repo_root / ref
    if not vp_path.exists():
        return None
    return load_json(vp_path)


def pick_detail_markers(vp: dict, limit: int = 3):
    markers = vp.get("silhouette_markers", []) if vp else []
    # deterministic pick: first few are “most recognizable”
    return markers[:limit] if markers else []


def npc_tone(npc_meta: dict):
    name = (npc_meta.get("name") or "").lower()
    t = (npc_meta.get("type") or "").lower()
    c = (npc_meta.get("category") or "").lower()
    aspects = npc_meta.get("aspects", {})
    high = (aspects.get("high_concept") or "").lower()

    # priority: specific famous IDs by name
    if "brynjolf" in name:
        return "warm_thief"
    if "justiciar" in t or "thalmor" in t or "thalmor" in high:
        return "cold_thalmor"
    if "guard" in t or "legionnaire" in t or "soldier" in t:
        return "suspicious_guard"
    if "jarl" in name or "noble" in t or "thane" in t:
        return "courtly_noble"
    if "companion" in t:
        return "warrior_respect"
    if "friendly" in c:
        return "neutral_friendly"

    return "neutral_default"


def compose_first_impression(pc: dict, vp: dict, npc_meta: dict, trigger: str):
    pc_name = pc.get("name", "The PC")
    npc_name = npc_meta.get("name", npc_meta.get("id", "NPC"))

    short = (vp.get("appearance", {}).get("short") if vp else "") or ""
    details = pick_detail_markers(vp, limit=3)

    tone = npc_tone(npc_meta)

    # lightweight “recognition” hooks
    pc_hc = (pc.get("aspects", {}).get("high_concept") or "").lower()
    guild = (pc.get("neutral_subfaction") or "").lower()
    thieves_hint = ("thieves" in pc_hc) or ("thieves_guild" in guild)

    # build a subtle, NPC-flavored line
    if tone == "warm_thief":
        line = (
            f"{npc_name}'s eyes flick over {pc_name}'s gear and posture. "
            f"'Still got that {('street-noble' if 'street-noble' in (vp.get('tags', []) if vp else []) else 'Riften')} look about you,' he murmurs—"
            f"a grin tugging at the corner of his mouth."
        )
    elif tone == "cold_thalmor":
        line = (
            f"{npc_name} studies {pc_name} with clinical calm—lingering on the eyes and the braid. "
            f"'A provincial affectation,' comes the quiet judgment, but their gaze stays sharp, like they're cataloging a threat."
        )
    elif tone == "suspicious_guard":
        line = (
            f"{npc_name}'s attention catches on {pc_name}'s cloak, wraps, and the way he stands too confidently for a common traveler. "
            f"'You look like trouble that learned manners,' they mutter, watching your hands."
        )
    elif tone == "courtly_noble":
        line = (
            f"{npc_name} reads {pc_name} like a ledger—noble bearing under practical leathers. "
            f"'Interesting,' they say, as if deciding whether you belong at court or in the gutters."
        )
    elif tone == "warrior_respect":
        line = (
            f"{npc_name} sizes up {pc_name}'s shoulders and wrapped forearms with a fighter's eye. "
            f"'You move like someone who's been in real fights,' they say—half compliment, half warning."
        )
    elif tone == "neutral_friendly":
        line = (
            f"{npc_name} offers a polite glance that lingers—icy eyes, braided hair, and that calm half-smirk. "
            f"'You carry yourself like you've survived worse than bad weather,' they note."
        )
    else:
        line = (
            f"{npc_name} gets a first look at {pc_name}: {('; '.join(details) if details else 'a calm, capable presence')}."
        )

    # add a gentle thieves-guild “tell” if appropriate
    if thieves_hint and tone in ("suspicious_guard", "courtly_noble", "neutral_default"):
        line += " Their gaze pauses on the subtle purple accents—like they recognize the color language, even if they can't name it."

    # if trigger explicitly wants full “First Impression”, add a tiny extra flourish
    if (trigger or "").lower() == "first impression" and short:
        line += " (First impression: " + short + ")"

    return line


def ensure_relationship_container(pc: dict):
    pc.setdefault("relationships", {})
    if not isinstance(pc["relationships"], dict):
        pc["relationships"] = {}
    pc["relationships"].setdefault("met_npcs", {})
    if not isinstance(pc["relationships"]["met_npcs"], dict):
        pc["relationships"]["met_npcs"] = {}


def update_campaign_met_list(repo_root: Path, npc_id: str):
    state_path = repo_root / "state" / "campaign_state.json"
    if not state_path.exists():
        return
    state = load_json(state_path)
    state.setdefault("world_consequences", {})
    wc = state["world_consequences"]
    wc.setdefault("npcs_met", [])
    if npc_id not in wc["npcs_met"]:
        wc["npcs_met"].append(npc_id)
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json(state_path, state)


def run(repo_root: Path, pc_id: str | None, npc_id: str, trigger: str, force: bool, quiet: bool):
    pc_path = get_pc_path(repo_root, pc_id)
    if not pc_path:
        if not quiet:
            print("No PC could be determined. Provide --pc pc_aldric_galewarden or set env var PC_ID.")
        return None

    pc = load_json(pc_path)
    ensure_relationship_container(pc)

    met_npcs = pc["relationships"]["met_npcs"]
    if (npc_id in met_npcs) and (not force):
        return {"skipped": True, "reason": "Already met", "npc_id": npc_id}

    vp = load_visual_profile(repo_root, pc)
    npc_meta = get_npc_meta(repo_root, npc_id)

    line = compose_first_impression(pc, vp, npc_meta, trigger)

    met_npcs[npc_id] = {
        "npc_id": npc_id,
        "npc_name": npc_meta.get("name", npc_id),
        "met_trigger": trigger,
        "met_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "first_impression": line
    }

    save_json(pc_path, pc)
    update_campaign_met_list(repo_root, npc_id)

    if not quiet:
        print(line)

    return {"skipped": False, "npc_id": npc_id, "first_impression": line, "pc_file": str(pc_path)}


def auto_first_impression(repo_root: Path, npc_id: str, trigger: str = "First Impression", force: bool = False, quiet: bool = False):
    return run(repo_root, pc_id=None, npc_id=npc_id, trigger=trigger, force=force, quiet=quiet)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="Repo root (default: .)")
    ap.add_argument("--pc", default=None, help="PC id (e.g., pc_aldric_galewarden). Optional if only one PC exists.")
    ap.add_argument("--npc", required=True, help="NPC id (e.g., brynjolf, olfrid_battle-born, whiterun_guard)")
    ap.add_argument("--trigger", default="First Impression", help="Trigger keyword")
    ap.add_argument("--force", action="store_true", help="Force a new impression even if already met")
    ap.add_argument("--quiet", action="store_true", help="Do not print; only record")
    args = ap.parse_args()

    repo_root = Path(args.repo).resolve()
    run(repo_root, args.pc, args.npc, args.trigger, args.force, args.quiet)


if __name__ == "__main__":
    main()
