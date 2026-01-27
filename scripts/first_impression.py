#!/usr/bin/env python3
import json
import random
from pathlib import Path
from datetime import datetime

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def maybe_first_impression(state_path, appearance_path, npc_id, disposition="neutral"):
    """
    Records first impressions so NPCs can comment once, then recognize later.
    disposition: neutral|positive|negative (GM decides based on context)
    """
    state = load_json(state_path)
    appearance = load_json(appearance_path)

    state.setdefault("npc_first_impressions", {})
    state["npc_first_impressions"].setdefault(npc_id, {})

    pc_id = appearance.get("pc_id", "unknown_pc")

    # Already recorded? do nothing.
    if pc_id in state["npc_first_impressions"][npc_id]:
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
