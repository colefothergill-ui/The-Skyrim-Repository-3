#!/usr/bin/env python3
"""
Windhelm Location Triggers

This module handles location-based triggers for Windhelm and the Palace of the Kings.
It provides contextual events, faction-based NPC interactions, and quest prompts
specific to Windhelm and Eastmarch Hold.
"""


def windhelm_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Windhelm locations.
    
    Args:
        loc: Current location string (e.g., "windhelm", "palace of the kings")
        campaign_state: Dictionary containing campaign state including faction alignment
        
    Returns:
        List of event strings to be narrated to players
    """
    events = []
    
    # Normalize location for case-insensitive matching
    loc_lower = str(loc).lower()
    
    # Stormcloak recruitment prompt if unaligned and first time in Palace
    # Handle Palace first to avoid triggering gate messages when entering Palace
    if "palace of the kings" in loc_lower and not campaign_state.get("stormcloaks_joined") and not campaign_state.get("imperial_legion_joined"):
        if not campaign_state.get("stormcloak_recruit_offer_seen"):
            events.append("Galmar Stone-Fist steps forward as you enter the hall, sizing you up with a warrior's gaze. \"You look like you can handle yourself,\" he growls in a tone that's almost an invitation. \"If you've come to Windhelm seeking purpose, speak to Jarl Ulfric. We've need of warriors with heart.\" It seems an opportunity to join the Stormcloaks is at hand.")
            campaign_state["stormcloak_recruit_offer_seen"] = True
    
    # Faction alignment reactions at Windhelm city gates (not Palace)
    elif "windhelm" in loc_lower and "palace" not in loc_lower:
        # Friendly greeting if player is a known Stormcloak ally
        if campaign_state.get("stormcloaks_joined") and not campaign_state.get("windhelm_stormcloak_welcome_done"):
            events.append("As you pass through the gates of Windhelm wearing the Stormcloak colors, a guard claps a hand to his heart in salute. \"Welcome, brother. Skyrim is a step closer to freedom thanks to warriors like you,\" he says gruffly, letting you through with a proud nod.")
            campaign_state["windhelm_stormcloak_welcome_done"] = True
        
        # Hostile reaction if player is known Imperial (but Windhelm is still Stormcloak-held)
        if campaign_state.get("imperial_legion_joined") and not campaign_state.get("windhelm_imperial_warning_done"):
            events.append("Upon entering Windhelm, you notice the mood shift. A pair of Stormcloak guards glare in your direction. One grips his axe tighter. \"Mind yourself, Imperial,\" he calls out coldly. \"You're walking among true Nords now.\" The warning is clear – your allegiance is noted here.")
            campaign_state["windhelm_imperial_warning_done"] = True
    
    return events
