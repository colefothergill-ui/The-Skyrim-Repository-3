#!/usr/bin/env python3
"""
Windhelm (Eastmarch) specific triggers and descriptive events.
Fires narrative events when the player enters Windhelm's districts or notable Eastmarch locations.
"""


def windhelm_location_triggers(player_location, campaign_state):
    """
    Generate location-specific triggers for Windhelm and Eastmarch locations.
    
    Args:
        player_location: Current location string (e.g., "windhelm", "windhelm_palace_of_the_kings")
        campaign_state: Dictionary containing campaign state including flags and companions
        
    Returns:
        List of event strings to be narrated to players
    """
    events = []
    loc = player_location.lower() if player_location else ""
    
    # Normalize location string to replace underscores with spaces for easier matching
    loc_normalized = loc.replace("_", " ")
    
    # Only proceed if location is Windhelm or Eastmarch-related
    if "windhelm" not in loc_normalized and "eastmarch" not in loc_normalized:
        return events

    # Windhelm City triggers - use if statements (not elif) as they are independent checks
    if "windhelm" in loc_normalized:
        # Palace of the Kings – first entry
        if "palace of the kings" in loc_normalized or ("palace" in loc_normalized and "windhelm" in loc_normalized):
            if not campaign_state.get("windhelm_palace_intro_done"):
                events.append("You step into the great hall of the Palace of the Kings. The air is thick with the smell of burning wood and politics. Jarl Ulfric Stormcloak sits upon the throne at the far end, his presence imposing. Courtiers and Stormcloak officers huddle in quiet discussion, war maps sprawled over a long table. For a moment, all eyes turn to you, a stranger in Ulfric's hall.")
                campaign_state["windhelm_palace_intro_done"] = True
            else:
                events.append("The Palace of the Kings looms around you, its ancient stone walls bearing the weight of countless winters. Ulfric's throne is occupied by the Jarl or his steward, overseeing the daily matters of war and governance. The murmurs of Windhelm's court echo in the vast chamber as the rebellion's plans continue to unfold.")
        
        # Gray Quarter – first entry event
        if "gray quarter" in loc_normalized or ("gray" in loc_normalized and "windhelm" in loc_normalized and "palace" not in loc_normalized):
            if not campaign_state.get("windhelm_gray_quarter_intro_done"):
                events.append("As you enter Windhelm's Gray Quarter, you notice the change immediately – the buildings are shabbier and the warmth of hearths is scarce. A few Nords shoot hard glances your way, then at the Dark Elves tending small merchant stands. Suddenly, a commotion draws your eye: a burly Nord with a scarred face is shouting at an elderly Dunmer woman on her doorstep.\n\n**Rolff Stone-Fist**: \"Why don't you just leave, Gray-Skin? Skyrim doesn't want you!\"\nThe woman shrinks back, anger and hurt in her eyes. Other residents watch silently from the shadows. This tension is palpable – you've walked into a city divided.")
                campaign_state["windhelm_gray_quarter_intro_done"] = True
                # (This encounter highlights Windhelm's racial tension. The player could intervene or observe.)
            else:
                events.append("The Gray Quarter's narrow alleyways feel claustrophobic. Dunmer residents pass by with cautious looks, and you catch whispered conversations dying as Nords walk past. Soot stains and old Dunmeri banners adorn the walls, remnants of a culture persevering under adversity.")
        
        # Stone Quarter (Market) – descriptive triggers
        if "stone quarter" in loc_normalized or ("stone" in loc_normalized and "windhelm" in loc_normalized) or ("market" in loc_normalized and "windhelm" in loc_normalized):
            if not campaign_state.get("windhelm_market_intro_done"):
                events.append("You arrive at Windhelm's open market in the Stone Quarter. Despite the biting cold, the square bustles. A blacksmith's hammer rings out from Oengul War-Anvil's forge near the gate, and merchants call out about fresh fish and sturdy Nord craftsmanship. At the center stands Candlehearth Hall, its great fire lantern above the door casting a warm glow over snow-dusted cobbles. The mix of voices—Nord, Dunmer, Argonian—reminds you that even this war-torn city still trades and lives each day.")
                campaign_state["windhelm_market_intro_done"] = True
            else:
                events.append("Windhelm's Stone Quarter is alive with activity. A guard is barking out the day's news near the old Talos statue, and a few children chase each other around market stalls despite the cold. The comforting aroma of stew wafts from Candlehearth Hall, momentarily overcoming the ever-present chill in the air.")
        
        # Windhelm Docks – descriptive trigger
        if "docks" in loc_normalized or ("harbor" in loc_normalized and "windhelm" in loc_normalized):
            if not campaign_state.get("windhelm_docks_intro_done"):
                events.append("The wind bites harder as you make your way to the Windhelm docks. Ice floes drift along the River Yorgrim as it meets the sea. Argonian dockworkers lug crates from a moored ship, their breath visible in the frigid air. A pair of East Empire Company mercantile flags hang limply on the warehouse, though business is slow – rumors of pirates on the trade routes abound. You sense that life here on the docks is as harsh as the cold itself, especially for those not welcome behind Windhelm's walls.")
                campaign_state["windhelm_docks_intro_done"] = True
            else:
                events.append("Down at the Windhelm docks, the river's icy expanse reflects a gray sky. Workers, mostly Argonians, move methodically unloading goods. A Nord overseer eyes them from a distance. The creaking of wooden hulls and the clink of chains are the dock's constant refrain, underscoring the isolation of this frozen port.")
    
    # Eastmarch wilderness triggers
    # Hot Springs area
    if "hot springs" in loc_normalized or "steam fields" in loc_normalized:
        if not campaign_state.get("eastmarch_hot_springs_seen"):
            events.append("You traverse into a valley of hissing hot springs and bubbling mud pools. A thin mist hangs over the land where ice and fire meet – snow drifts lie adjacent to steaming, sulfur-scented ponds. In the distance, a giant lazily watches his mammoths bathe in a boiling mire. The ground is warm underfoot despite the cold air. Eastmarch's volcanic tundra is as beautiful as it is eerie.")
            campaign_state["eastmarch_hot_springs_seen"] = True
        else:
            events.append("Steam vents puff gently around you on Eastmarch's volcanic tundra. Pools of turquoise thermal water break up the snowy landscape. Now and then, you hear a distant rumble as the earth releases its heat. The area is alive with both danger and strange serenity.")
    
    # Mountain pass to Morrowind (Dunmeth Pass)
    if "dunmeth pass" in loc_normalized or "morrowind border" in loc_normalized:
        events.append("High in the eastern mountains, you find the path known as Dunmeth Pass. The wind howls between jagged peaks. Far ahead, an old stone arch marks the border between Skyrim and Morrowind, watched by a few wary guards on Skyrim's side. The road beyond is officially closed, but the air carries the scent of ash from the Morrowind side. This lonely pass stands as a quiet reminder of how close the wider world looms beyond Eastmarch.")
    
    # (Additional Eastmarch location triggers, e.g. Kynesgrove or Orc stronghold Narzulbur, can be added similarly)
    
    return events
