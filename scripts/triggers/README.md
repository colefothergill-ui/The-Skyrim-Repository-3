# Triggers Module

This module contains location-based narrative triggers and events for different areas in Skyrim.

## Overview

The triggers system provides dynamic, context-aware narrative descriptions and events that fire when players enter specific locations. It tracks campaign state to ensure events happen only once (or repeat appropriately) and integrates seamlessly with quest progression.

## Current Implementations

### whiterun_triggers.py

Handles all location-based triggers for Whiterun City and its districts.

**Districts covered:**
- **Plains District**: Market area, initial encounters
- **Wind District**: Residential area, Jorrvaskr, Temple of Kynareth
- **Cloud District / Dragonsreach**: Jarl's palace, formal audiences

## Usage

### Basic Usage

```python
from triggers.whiterun_triggers import whiterun_location_triggers

# Load or initialize campaign state
campaign_state = {
    # Flags tracking which events have occurred
}

# Get events for current location
player_location = "Whiterun - Plains District"
events = whiterun_location_triggers(player_location, campaign_state)

# Present events to players
for event in events:
    print(event)
    
# Campaign state is automatically updated with flags
# Save campaign_state to persist changes
```

### Integration with Story Manager

Add this to your story manager's location change handler:

```python
from triggers.whiterun_triggers import whiterun_location_triggers

class StoryManager:
    def handle_location_change(self, new_location):
        # Load campaign state
        campaign_state = self.load_campaign_state()
        
        # Get location triggers
        events = whiterun_location_triggers(new_location, campaign_state)
        
        # Present events to players
        for event in events:
            self.present_narrative(event)
        
        # Save updated campaign state
        self.save_campaign_state(campaign_state)
```

## Campaign State Flags

The triggers system uses these flags in `campaign_state`:

### Whiterun Flags

- `whiterun_plains_intro_done`: First visit to Plains District completed
- `whiterun_wind_intro_done`: First visit to Wind District completed
- `whiterun_cloud_intro_done`: First visit to Cloud District completed
- `graymane_feud_seen`: Witnessed the Battle-Born vs Gray-Mane argument
- `missing_in_action_started`: "Missing in Action" quest has begun
- `dragon_rising_completed`: Player defeated dragon at Western Watchtower
- `jarl_audience_done`: Had formal audience with Jarl Balgruuf

## Features

### First-Time Descriptions
Rich, atmospheric descriptions for first visits to each district that set the scene and establish the mood.

### Repeatable Flavor Text
Shorter, atmospheric descriptions for repeat visits that maintain immersion without repetition.

### Dynamic Events
Context-aware events that trigger based on:
- Location
- Campaign state flags
- Quest progression
- Story milestones

### Quest Hooks
Narrative nudges that remind players of available quests or suggest new avenues for exploration.

## Adding New Triggers

To add triggers for a new location:

1. Create a new file (e.g., `riften_triggers.py`)
2. Implement a function similar to `whiterun_location_triggers()`
3. Follow these patterns:
   - Check location string (case-insensitive)
   - Use campaign_state flags to track event occurrence
   - Return list of event strings
   - Update flags in campaign_state as needed
4. Add tests in `tests/test_<location>_triggers.py`
5. Update this README

### Example Template

```python
def location_triggers(player_location, campaign_state):
    """
    Determine events for a specific location.
    
    Args:
        player_location (str): Current location
        campaign_state (dict): Campaign state with flags
    
    Returns:
        list of str: Event descriptions
    """
    events = []
    loc = player_location.lower() if player_location else ""
    
    if not loc.startswith("location_name"):
        return events
    
    # Add your trigger logic here
    if not campaign_state.get("location_intro_done"):
        events.append("First time description...")
        campaign_state["location_intro_done"] = True
    
    return events
```

## Testing

Run the test suite:

```bash
cd /path/to/repo
python tests/test_whiterun_triggers.py
```

Run the demo:

```bash
python tests/demo_whiterun_triggers.py
```

## Design Principles

1. **Modular**: Each location has its own trigger file
2. **Non-intrusive**: Only appends to event list, doesn't modify game state directly
3. **State-aware**: Uses campaign_state to avoid repetition
4. **Context-sensitive**: Triggers based on both location and quest progress
5. **Narrative-first**: Focuses on storytelling and atmosphere
6. **Integration-ready**: Easy to call from existing story management systems

## Future Enhancements

Potential additions:
- Triggers for other major cities (Riften, Solitude, Windhelm)
- Time-of-day variations
- Weather-based descriptions
- Faction reputation influences
- Random encounter tables
- Seasonal variations
- NPC schedule-based events
