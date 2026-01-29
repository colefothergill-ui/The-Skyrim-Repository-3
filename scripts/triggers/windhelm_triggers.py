#!/usr/bin/env python3
"""
Windhelm Location Triggers

This module handles location-based triggers for Windhelm and Eastmarch.
It provides contextual events, NPC interactions, and companion commentary
specific to Windhelm Hold, including quest hooks for Blood on the Ice
and The White Phial.
"""


def _is_companion_present(active_companions, companion_name):
    """
    Check if a specific companion is present in the active companions list.
    
    Args:
        active_companions: List of active companions (can be strings or dicts)
        companion_name: Name of companion to check for (case-insensitive)
    
    Returns:
        bool: True if companion is present, False otherwise
    """
    companion_name_lower = companion_name.lower()
    
    for companion in active_companions:
        if isinstance(companion, dict):
            # Check dictionary companions by name or npc_id/id field
            comp_name = str(companion.get("name", "")).lower()
            comp_id = str(companion.get("npc_id", companion.get("id", ""))).lower()
            # Use startswith to allow variations like "Stenvar" or "Stenvar (Mercenary)"
            if comp_name.startswith(companion_name_lower) or comp_id.startswith(companion_name_lower):
                return True
        else:
            # Check string companions
            # Use startswith to allow variations like "Stenvar" or "Stenvar the Mercenary"
            if str(companion).lower().startswith(companion_name_lower):
                return True
    
    return False


def _is_quest_active(campaign_state, quest_id):
    """
    Check if a quest is currently active or completed.
    
    Args:
        campaign_state: Dictionary containing campaign state including quests
        quest_id: The ID of the quest to check
    
    Returns:
        bool: True if quest is active or completed, False otherwise
    """
    quests = campaign_state.get("quests", {})
    active_quests = quests.get("active", [])
    completed_quests = quests.get("completed", [])
    
    # Check if quest_id is in active or completed lists
    if quest_id in active_quests or quest_id in completed_quests:
        return True
    
    # Also check for dictionary format quests
    for quest in active_quests:
        if isinstance(quest, dict) and quest.get("id") == quest_id:
            return True
    
    for quest in completed_quests:
        if isinstance(quest, dict) and quest.get("id") == quest_id:
            return True
    
    return False


def _is_night_time(campaign_state):
    """
    Check if it's nighttime in the game.
    
    Args:
        campaign_state: Dictionary containing campaign state including time of day
    
    Returns:
        bool: True if it's night (8 PM to 6 AM), False otherwise
    """
    time_of_day = campaign_state.get("time_of_day", "")
    
    # Check various night indicators
    if isinstance(time_of_day, str):
        time_lower = time_of_day.lower()
        return "night" in time_lower or "evening" in time_lower or "midnight" in time_lower
    
    # If time is given as an hour (0-23)
    if isinstance(time_of_day, int):
        return time_of_day >= 20 or time_of_day < 6
    
    return False


def windhelm_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Windhelm locations.
    
    Args:
        loc: Current location string (e.g., "windhelm", "windhelm_graveyard")
        campaign_state: Dictionary containing campaign state including companions and quests
        
    Returns:
        List of event strings to be narrated to players
    """
    events = []
    
    # Normalize location for case-insensitive matching
    loc_lower = str(loc).lower()
    
    # Get active companions
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])
    
    # District/area-specific triggers
    if "gray_quarter" in loc_lower or "grey_quarter" in loc_lower:
        events.append("You enter the Gray Quarter, home to Windhelm's Dark Elf population. The air is thick with incense and the sounds of foreign tongues. Dilapidated buildings and suspicious glances speak to the Dunmer's treatment in this city.")
    
    elif "graveyard" in loc_lower and "windhelm" in loc_lower:
        events.append("The cold wind whistles through Windhelm's graveyard. Stone markers stand as silent witnesses to the city's dead, their names weathered by Skyrim's harsh winters.")
        
        # Blood on the Ice quest hook - nighttime graveyard visit
        if not _is_quest_active(campaign_state, "blood_on_the_ice"):
            if _is_night_time(campaign_state):
                events.append("You hear distant shouts near the graveyard... A guard's voice cuts through the night: 'Another one! Someone get the steward!' A crowd is gathering around something near the Hall of the Dead.")
            else:
                # Daytime hint
                events.append("A guard stationed nearby mutters to his companion: 'Three murders in as many weeks. The Butcher strikes again, they say. Keep your eyes open after dark.'")
    
    elif "market" in loc_lower and "windhelm" in loc_lower:
        events.append("The marketplace of Windhelm bustles with activity. Vendors hawk their wares while Nord shoppers barter loudly. The imposing Palace of the Kings looms over the district.")
        
        # White Phial shop hint
        if not _is_quest_active(campaign_state, "the_white_phial"):
            events.append("As you pass by the White Phial alchemy shop, you hear raised voices inside. An elderly voice rasps: 'I don't have much time, Quintus! The Phial must be found!' followed by a younger man's worried reply.")
    
    elif "palace_of_the_kings" in loc_lower or ("palace" in loc_lower and "windhelm" in loc_lower):
        events.append("You stand before the Palace of the Kings, seat of Jarl Ulfric Stormcloak. The ancient stone fortress radiates power and defiance, a symbol of Nordic tradition and the Stormcloak cause.")
    
    elif "candlehearth_hall" in loc_lower or ("candlehearth" in loc_lower and "windhelm" in loc_lower):
        events.append("Candlehearth Hall's warmth is a welcome respite from Windhelm's bitter cold. The inn is filled with the smell of roasting meat and the sound of travelers sharing tales.")
    
    # General Windhelm entrance
    elif loc_lower.startswith("windhelm") or "windhelm" in loc_lower:
        events.append("The ancient stone walls of Windhelm rise before you, weathered by countless winters. Known as the City of Kings, Windhelm stands as a bastion of Nordic tradition and the current seat of Ulfric Stormcloak's rebellion.")
        
        # General quest hooks when entering the city
        if not _is_quest_active(campaign_state, "blood_on_the_ice") and _is_night_time(campaign_state):
            events.append("The city feels tense at night. Shadows seem longer here, and few citizens walk the streets after dark. You overhear whispered conversations about recent murders...")
    
    # Companion commentary for Windhelm-relevant companions
    if _is_companion_present(active_companions, "stenvar"):
        if loc_lower.startswith("windhelm"):
            events.append('Stenvar grunts as you enter Windhelm. "Never cared much for this place. Too cold, too many politics. But the mead at Candlehearth Hall isn\'t bad."')
    
    # Companions with Nord heritage might comment on the city's history
    if _is_companion_present(active_companions, "uthgerd"):
        if loc_lower.startswith("windhelm"):
            events.append('Uthgerd looks around appreciatively. "Windhelm... the oldest city in Skyrim. Built by Ysgramor himself. Whatever you think of Ulfric, you can\'t deny this place has history."')
    
    return events
