# Location Triggers Module

This module contains location-based trigger systems for various regions in Skyrim.

## Purpose

Location triggers provide:
- Atmospheric descriptions when entering new areas
- Context-aware NPC and companion commentary
- Dynamic events based on location and party composition
- Modular hooks for future expansion

## Current Implementations

### Whiterun Triggers (`whiterun_triggers.py`)

Handles all Whiterun Hold locations including:
- Whiterun City (general entrance)
- Plains District
- Wind District  
- Cloud District

Features companion commentary for Whiterun-based followers (currently Lydia).

### Windhelm Triggers (`windhelm_triggers.py`)

Handles all Windhelm and Eastmarch locations including:
- Windhelm City districts:
  - Palace of the Kings (Ulfric's throne room)
  - Gray Quarter (Dunmer district with racial tension)
  - Stone Quarter (market district)
  - Windhelm Docks (Argonian workers, East Empire Company)
- Eastmarch wilderness:
  - Hot Springs (volcanic tundra)
  - Dunmeth Pass (border with Morrowind)

Features one-time narrative events (e.g., Rolff Stone-Fist harassing Dunmer) and evolving ambient descriptions.

## Usage

```python
from triggers import whiterun_location_triggers, windhelm_location_triggers

campaign_state = {
    "companions": {
        "active_companions": ["Lydia"]
    }
}

# Whiterun triggers
events = whiterun_location_triggers("whiterun", campaign_state)

# Windhelm triggers
events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
```

## Future Expansions

Additional trigger modules can be added for other holds and locations:
- `riften_triggers.py` - Riften and the Rift Hold
- `solitude_triggers.py` - Solitude and Haafingar Hold
- ~~`windhelm_triggers.py` - Windhelm and Eastmarch Hold~~ ✓ Implemented
- `markarth_triggers.py` - Markarth and the Reach
- `winterhold_triggers.py` - Winterhold and its college
- `dawnstar_triggers.py` - Dawnstar and the Pale
- `falkreath_triggers.py` - Falkreath Hold
- `morthal_triggers.py` - Morthal and Hjaalmarch
- `wilderness_triggers.py` - Roads, forests, and wilderness areas

## Testing

Each trigger module should have corresponding tests in the `tests/` directory.

Test suites available:
- `tests/test_whiterun_triggers.py` - Whiterun triggers test suite
- `tests/test_windhelm_triggers.py` - Windhelm triggers test suite

## Documentation

For detailed information about the triggers, see:
- `docs/whiterun_triggers_guide.md`

For demo usage examples, run:
- `tests/demo_whiterun_triggers.py`
- `tests/demo_windhelm_triggers.py`
