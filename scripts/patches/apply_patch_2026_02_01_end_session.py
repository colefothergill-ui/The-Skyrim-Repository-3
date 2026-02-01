import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # repo root
STAMP = "2026-02-01 (Session End Protocol)"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def clamp(n, lo, hi): 
    return max(lo, min(hi, n))

def main():
    # -------------------------
    # FILE PATHS
    # -------------------------
    p_faction_trust = REPO / "data/clocks/faction_trust_clocks.json"
    p_whiterun_jobs = REPO / "data/clocks/whiterun_jobs.json"
    p_pc_clocks     = REPO / "data/clocks/pc_extras_clocks.json"
    p_civil_war     = REPO / "data/clocks/civil_war_clocks.json"
    p_campaign      = REPO / "state/campaign_state.json"
    p_pc            = REPO / "data/pcs/pc_khagar_yal.json"
    p_hadvar        = REPO / "data/npc_stat_sheets/hadvar.json"

    faction_trust = load_json(p_faction_trust)
    whiterun_jobs = load_json(p_whiterun_jobs)
    pc_clocks     = load_json(p_pc_clocks)
    civil_war     = load_json(p_civil_war)
    campaign      = load_json(p_campaign)
    pc            = load_json(p_pc)
    hadvar        = load_json(p_hadvar)

    # -------------------------
    # CHECK IF PATCH ALREADY APPLIED (idempotency check)
    # -------------------------
    if campaign.get("last_updated") == STAMP:
        print(f"\n[INFO] Patch already applied (last_updated = {STAMP}). Skipping to avoid duplicate updates.")
        return

    # -------------------------
    # 1) CONTINUITY FIX: Thieves Guild bleedover → reset to 0/uninvolved
    # -------------------------
    tg = faction_trust["faction_trust_clocks"]["clocks"]["thieves_guild_trust"]
    tg["current_trust"] = 0
    tg["trust_level"] = "Stranger"
    note = "Continuity correction (2026-02-01): Aldrin-era Thieves Guild progress removed; Khagar Yal has no TG affiliation."
    tg["notes"] = (tg.get("notes","").strip() + (" " if tg.get("notes","").strip() else "") + note).strip()

    # -------------------------
    # 2) CONTINUITY FIX: Aldrin-era Whiterun TG job clocks → set to 0 + mark inactive
    # -------------------------
    clocks = whiterun_jobs["whiterun_jobs"]["clocks"]
    for k in ("guild_foothold_whiterun", "battleborn_strongbox"):
        clocks[k]["current"] = 0
        clocks[k]["status"] = "inactive_for_khagar_yal"
        clocks[k]["continuity_note"] = (
            "Retired: this clock belonged to Aldrin/Thieves Guild story. "
            "Keep as optional module, but it is NOT active for Khagar Yal."
        )

    # -------------------------
    # 3) BITTER MERCY: Awakening 6/6 + unlock text
    # -------------------------
    bm = pc_clocks["pc_extras_clocks"]["clocks"]["khagar_bitter_mercy_awakening"]
    bm["current_progress"] = 6
    bm["unlocks"]["6"] = (
        "Level 4 (Awakening 6): Apex Predator (free stunt tied to Bitter Mercy) + "
        "clarify Bitter Mercy synergy as Weapon:+1 vs 'Bitter Mercy' marked prey (max Weapon:3 total)."
    )

    # Thalmor scry escalation +1 (public daedric/lycanthrope signature in major battle)
    scry = pc_clocks["pc_extras_clocks"]["clocks"]["thalmor_scent_scry_escalation"]
    scry["current_progress"] = clamp(scry.get("current_progress",0) + 1, 0, scry.get("total_segments",6))

    # -------------------------
    # 4) FP LEDGER + FP TOTAL: set FP to 1, fix the specific entries
    # -------------------------
    pc["fate_points"] = 1
    ledger = pc.get("fate_point_ledger", [])

    # Fix: Hadvar elixir compel should be +2
    for e in ledger:
        if e.get("type") == "compel_award" and "Potion of the Huntsman" in e.get("note",""):
            e["delta"] = 2
            e["note"] = "Compel accepted: offered Hadvar the healing elixir + honored duel terms (Trouble/Code of Hircine)."

        # Remove phantom FP award
        if e.get("type") == "compel_award" and "predator-rite escalation" in e.get("note",""):
            e["type"] = "admin_note"
            e["delta"] = 0
            e["note"] = "(Deprecated) Removed erroneous FP award from earlier sim. No FP gained here."

    # Add: Stag of Eastmarch FP spend if missing
    if not any(e.get("type") == "invoke_spend" and "Stag of Eastmarch" in e.get("note","") for e in ledger):
        ledger.append({
            "type": "invoke_spend",
            "delta": -1,
            "note": "Spent FP: Invoked 'Stag of Eastmarch' to land the decisive social blow during the Hadvar duel.",
            "timestamp": "2026-02-01T00:00:00Z"
        })

    pc["fate_point_ledger"] = ledger

    # -------------------------
    # 5) ADD FREE STUNT: Apex Predator (tied to Bitter Mercy extra)
    # -------------------------
    bm_extra = pc["extras"]["daedric_artifact_bitter_mercy"]
    bm_extra["name"] = "Daedric Artifact: Spear of Bitter Mercy (Awakening 6 — Apex Predator)"

    # Clarify Bitter Mercy trait text (Weapon:+1 vs marked prey, max Weapon:3)
    if bm_extra.get("traits"):
        bm_extra["traits"][0] = (
            "Bitter Mercy: When Bitter Mercy helps you inflict a Mild Consequence on a target, that target gains the "
            "situation aspect 'Bitter Mercy'. Until that creature is taken out, your stress dealt to that creature "
            "increases by +1 weapon rating (max Weapon:3 total, including the spear)."
        )

    apex = (
        "Apex Predator (Bitter Mercy): While wielding Bitter Mercy, wildlife predators (bears, wolves, frostbite spiders, "
        "sabre cats) and other lycanthropes suffer -1 on Fight or Shoot attack rolls made against Khagar Yal. "
        "When Khagar Yal attacks one of those creatures with Bitter Mercy, he gains +1 to the Fight or Shoot attack roll."
    )
    stunts = bm_extra.setdefault("stunts", [])
    # Check if any stunt already contains "Apex Predator" to avoid duplicates
    if not any("Apex Predator" in s for s in stunts):
        stunts.append(apex)

    # -------------------------
    # 6) CIVIL WAR CLOCKS: Set explicit target values (idempotent)
    # -------------------------
    cw = civil_war["civil_war_clocks"]["clocks"]
    # Target: Stormcloak momentum = 5 (from original 4)
    cw["stormcloak_rebellion_momentum"]["current_progress"] = clamp(
        5, 0, cw["stormcloak_rebellion_momentum"]["total_segments"]
    )
    # Target: Imperial dominance = 2 (from original 3)
    cw["imperial_military_dominance"]["current_progress"] = clamp(
        2, 0, cw["imperial_military_dominance"]["total_segments"]
    )

    # -------------------------
    # 7) FACTION TRUST: Set explicit target value (idempotent)
    # -------------------------
    sc = faction_trust["faction_trust_clocks"]["clocks"]["stormcloak_rebellion_trust"]
    # Target: Stormcloaks = 5 (from original 3)
    sc["current_trust"] = clamp(5, 0, sc["max_trust"])
    sc["trust_level"] = sc.get("trust_level","Ally")  # keep label stable; numeric drives unlocks

    # -------------------------
    # 8) CAMPAIGN STATE: set target session_count, scene + objective, flags, modifiers
    # -------------------------
    # Target session count: 2 (idempotent)
    campaign["session_count"] = 2
    campaign["last_updated"] = STAMP
    campaign["current_scene_id"] = "A1-S03-WHITERUN-GATES-AFTERMATH"
    campaign["current_objective"] = "Resolve Hadvar's fate with Ralof, then decide whether to press into Whiterun or consolidate the breach."

    sf = campaign.setdefault("scene_flags", {})
    sf["hadvar_duel_in_progress"] = False
    sf["hadvar_duel_concluded"] = True
    sf["hadvar_taken_out_alive"] = True
    sf["hadvar_fate_pending"] = True

    # Add battle modifiers (payoff for honor + command decapitation)
    mods = campaign["civil_war_state"].setdefault("battle_of_whiterun_modifiers", [])

    def has_aspect(a): 
        return any(m.get("aspect") == a for m in mods)

    if not has_aspect("Chain of Command Severed"):
        mods.append({
            "aspect": "Chain of Command Severed",
            "free_invokes": 1,
            "source": "Khagar and Ralof neutralized the horn signaller and the line-conducting officer during the gate breach.",
            "expires": "End of Battle of Whiterun",
            "note": "Represents ongoing Imperial confusion at the gates/backline."
        })

    if not has_aspect("Word Kept at the Gate"):
        mods.append({
            "aspect": "Word Kept at the Gate",
            "free_invokes": 1,
            "source": "Khagar honored the duel terms, allowed wounded to retreat, and ceded Hadvar's fate to Ralof.",
            "expires": "End of Battle of Whiterun",
            "note": "Social + tactical leverage: hesitation, parley openings, and reduced panic among noncombatants."
        })

    # Slightly soften Imperial relationship due to honor (still hostile, just not mindless)
    fr = campaign["civil_war_state"].setdefault("faction_relationship", {})
    fr["imperial_legion"] = min(int(fr.get("imperial_legion", -20)) + 2, 0)

    # World consequence log
    wc = campaign.setdefault("world_consequences", {})
    wc.setdefault("major_choices", [])
    line = (
        "Hadvar was Taken Out in honorable single combat at Whiterun's gates; "
        "Khagar allowed the node's wounded retreat and ceded Hadvar's fate to Ralof (pending decision)."
    )
    if line not in wc["major_choices"]:
        wc["major_choices"].append(line)

    # Ralof loyalty: set explicit target value and sync with companion_relationships (idempotent)
    target_loyalty = 70  # Target: 70 (from original 62)
    session_note = (
        "Session 2: Khagar fought in sync with Ralof, then honored Ralof's history with Hadvar by giving him the final call."
    )
    ralof_loyalty = None
    for comp in campaign.get("companions", {}).get("active_companions", []):
        if comp.get("name") == "Ralof":
            # Set to target value
            comp["loyalty"] = clamp(target_loyalty, 0, 100)
            ralof_loyalty = comp["loyalty"]
            
            # Add note if not already present (idempotent)
            notes = comp.get("notes", "").strip()
            if session_note not in notes:
                comp["notes"] = (notes + (" " if notes else "") + session_note).strip()

    # Keep companion_relationships entry for Ralof in sync with active companion loyalty
    if ralof_loyalty is not None:
        companions_root = campaign.setdefault("companions", {})
        relationships = companions_root.setdefault("companion_relationships", {})
        relationships["ralof"] = ralof_loyalty

    # -------------------------
    # 9) HADVAR NPC SHEET: mark taken out alive + injuries (for continuity)
    # -------------------------
    hadvar.setdefault("consequences", {})
    hadvar["consequences"]["moderate"] = hadvar["consequences"].get("moderate") or "Ribcage Raked Open (Bleeding Hard)"
    hadvar["consequences"]["severe"] = hadvar["consequences"].get("severe") or "Pinned to the Cobbles (Shoulder Impaled)"
    hadvar["status"] = {
        "state": "taken_out_alive",
        "captor": "Khagar Yal / Ralof",
        "location": "Whiterun Gate (Stormcloak breach line)",
        "note": "Alive, incapacitated. Fate pending: execute / capture / ransom / release / recruit."
    }

    # -------------------------
    # 10) WRITE SESSION LOG (LATEST)
    # -------------------------
    log_path = REPO / "logs/2026-02-01_session-02_LATEST.md"
    log_path.write_text(
        "# Session 02 — Battle of Whiterun: Gates & the Duel (LATEST)\n"
        "**Date:** 2026-02-01  \n"
        "**Act / Scene:** Act I — A1-S03 (Whiterun Gates → Aftermath)  \n"
        "**PC:** Khagar Yal (Werebear Warchief; Spear of Bitter Mercy)  \n"
        "**Primary Ally:** Ralof (Companion)\n\n"
        "## Major Events (Canon)\n"
        "1. Gate breach momentum established (Khagar spearhead; Pack Tactics).\n"
        "2. Imperial chain of command shattered (horn/signaller + conducting officer neutralized).\n"
        "3. Hadvar node allowed to retreat; honor duel agreed and honored.\n"
        "4. Duel resolved: Hadvar Taken Out **alive**; Khagar cedes final decision to Ralof.\n\n"
        "## Mechanical Summary\n"
        "- Fate Points (end): **1**\n"
        "- Bitter Mercy Awakening: **6/6** (Unlock: **Apex Predator**)\n"
        "- New battle modifiers: **Chain of Command Severed** (1 free invoke), **Word Kept at the Gate** (1 free invoke)\n\n"
        "## Fallout\n"
        "- Ralof loyalty +3\n"
        "- Stormcloak trust +1\n"
        "- Imperial relationship slightly softened (honor noted; still hostile)\n\n"
        "## Next Session Start Hook\n"
        "- Ralof decides Hadvar's fate: execute / capture / ransom / release / recruit.\n"
        "- Decide: press into Whiterun or consolidate the breach.\n",
        encoding="utf-8"
    )

    # -------------------------
    # SAVE ALL JSON
    # -------------------------
    save_json(p_faction_trust, faction_trust)
    save_json(p_whiterun_jobs, whiterun_jobs)
    save_json(p_pc_clocks, pc_clocks)
    save_json(p_civil_war, civil_war)
    save_json(p_campaign, campaign)
    save_json(p_pc, pc)
    save_json(p_hadvar, hadvar)

    # -------------------------
    # WARN ABOUT .bak CONTAMINATION (do not delete automatically)
    # -------------------------
    bak_files = list(REPO.rglob("*.bak*"))
    if bak_files:
        print("\\n[WARN] Found .bak/.bak_* files that may contain non-canon bleedover:")
        for b in bak_files[:25]:
            print(" -", b.relative_to(REPO))
        if len(bak_files) > 25:
            print(f" - ...and {len(bak_files)-25} more")

    print("\\n[OK] Patch applied.")
    print(" - Thieves Guild trust:", tg["current_trust"], tg["trust_level"])
    print(" - Whiterun TG job clocks:", clocks["guild_foothold_whiterun"]["current"], clocks["battleborn_strongbox"]["current"])
    print(" - FP:", pc["fate_points"])
    print(" - Bitter Mercy awakening:", bm["current_progress"], "/", bm["total_segments"])
    print(" - Session count (next session):", campaign["session_count"])
    print(" - Wrote log:", log_path.relative_to(REPO))

if __name__ == "__main__":
    main()
