#!/usr/bin/env python3
"""
PC Visual Manager (Trigger-based)

- Loads a PC sheet.
- Loads that PC's visual profile JSON.
- Given a trigger (Zone-In / First Impression / location tags), prints:
  - portrait path
  - short or detailed appearance (based on trigger mapping)

This mirrors the repo pattern where NPC stat sheets contain "scene_triggers".
"""

import json
import argparse
from pathlib import Path


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def auto_pick_single_pc(pcs_dir: Path):
    pcs = [p for p in pcs_dir.glob("pc_*.json") if p.name != "example_pc.json"]
    if len(pcs) == 1:
        return pcs[0]
    return None


def get_pc_path(repo_root: Path, pc_id: str | None):
    pcs_dir = repo_root / "data" / "pcs"
    if pc_id:
        p = pcs_dir / f"{pc_id}.json"
        if p.exists():
            return p
    auto = auto_pick_single_pc(pcs_dir)
    if auto:
        return auto
    raise FileNotFoundError("Could not determine PC file. Provide --pc pc_<your_character_id> (or ensure only 1 pc_*.json exists, excluding example_pc.json).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="Repo root (default: .)")
    ap.add_argument("--pc", default=None, help="PC id (e.g., pc_khagar_yal). If omitted, auto-picks if only one PC exists.")
    ap.add_argument("--trigger", default="Zone-In", help="Trigger keyword (Zone-In, First Impression, Riften, Whiterun, etc.)")
    args = ap.parse_args()

    repo_root = Path(args.repo).resolve()
    pc_path = get_pc_path(repo_root, args.pc)
    pc = load_json(pc_path)

    vp_ref = pc.get("visual_profile_ref")
    if not vp_ref:
        print("No visual_profile_ref on PC sheet. Add it to enable trigger outputs.")
        print(f"PC file: {pc_path}")
        return

    vp_path = repo_root / vp_ref
    vp = load_json(vp_path)

    trigger = (args.trigger or "").strip()
    outputs = vp.get("trigger_outputs", {})
    mode = outputs.get(trigger, "short")

    portrait_path = vp.get("portrait", {}).get("path") or pc.get("portrait_path")

    print("=" * 70)
    print(f"PC VISUALS — {pc.get('name', pc.get('id', 'Unknown PC'))}")
    print("=" * 70)
    print(f"Trigger: {trigger}")
    print(f"Output: {mode}")
    if portrait_path:
        print(f"Portrait: {portrait_path}")
    print()

    appearance = vp.get("appearance", {})
    text = appearance.get(mode) or appearance.get("short") or ""
    print(text)
    print()


if __name__ == "__main__":
    main()
