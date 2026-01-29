#!/usr/bin/env python3
"""
Whiterun-specific triggers and descriptions
This module defines events and descriptive text that fire based on the player's location in Whiterun City and surroundings.
"""


def whiterun_location_triggers(player_location, campaign_state):
    """
    Determine any special events or descriptive triggers when the player enters a location in Whiterun.
    
    Args:
        player_location (str): The current location of the player (e.g., "Whiterun - Plains District").
        campaign_state (dict): The campaign state, used to check flags (e.g., whether an event has already occurred).
    
    Returns:
        list of str: Descriptions or event prompts triggered by this location.
    """
    events = []
    loc = player_location.lower() if player_location else ""
    if not loc.startswith("whiterun"):
        # If not in Whiterun, no special Whiterun triggers
        return events

    # Descriptive trigger: entering the Plains District for the first time
    if "plains district" in loc:
        if not campaign_state.get("whiterun_plains_intro_done"):
            events.append("As you step through Whiterun's gates into the Plains District, you're greeted by a bustle of activity. Merchants hawk their wares in the open-air market ahead, the forge at Warmaiden's clangs with activity, and the comforting scent of baked bread wafts from The Bannered Mare. The heart of Skyrim's trade greets you warmly.")
            campaign_state["whiterun_plains_intro_done"] = True
        # Ongoing atmosphere in Plains District (repeatable flavor)
        else:
            events.append("You find yourself in Whiterun's lively Plains District. Citizens chatter around market stalls, a town guard strolls by with a watchful eye, and from somewhere nearby you hear the bard in The Bannered Mare begin a new song.")

        # Event trigger: Gray-Mane vs Battle-Born feud encounter (first visit)
        if not campaign_state.get("graymane_feud_seen"):
            events.append("Near the market, an argument is in progress: a sharp-tongued old woman in modest attire and a well-dressed Nord man are practically nose-to-nose.\n\n**Fralia Gray-Mane**: \"You Imperial sympathizers have done nothing to find my Thorald!\"\n**Idolaf Battle-Born**: \"Careful, old woman. The Empire has better uses for its time than searching for traitors. Maybe you should accept he's gone.\"\nThey notice you, a stranger, observing the commotion. The man turns, eyes narrowing. **Idolaf**: \"You there, newcomer – Battle-Born or Gray-Mane?\"")
            campaign_state["graymane_feud_seen"] = True
            # (This encounter lets the player choose a side; siding with Fralia can initiate the 'Missing in Action' quest.)
    
    # Descriptive trigger: entering the Wind District for the first time
    if "wind district" in loc:
        if not campaign_state.get("whiterun_wind_intro_done"):
            events.append("Climbing the steps into the Wind District, you immediately notice the change in atmosphere. The sounds of the market fade, replaced by the quiet of residential life. The great Gildergreen tree stands at the center, its leaves whispering in the mountain breeze. Around it, well-kept homes line the street. You see Jorrvaskr, the famous mead hall of the Companions, off to one side, and the tall spire of the Temple of Kynareth on the other. This is where Whiterun's people live and worship, steadied by tradition and community.")
            campaign_state["whiterun_wind_intro_done"] = True
        else:
            events.append("You walk through Whiterun's Wind District. The evening breeze carries the scent of the Gildergreen's sap. A couple of Companions, clad in wolf-emblazoned armor, stride past on their way to Jorrvaskr, and a priestess tends to the steps of the Temple of Kynareth. It's peaceful here above the city's bustle.")
        
        # Quest hook: Missing in Action (if player showed interest in Gray-Mane feud and hasn't started the quest yet)
        if campaign_state.get("graymane_feud_seen") and not campaign_state.get("missing_in_action_started"):
            # If the player sided with Fralia or otherwise showed concern, they might seek her out now.
            events.append("You recall Fralia Gray-Mane's plea about her missing son. Perhaps you could find her near her home in the Wind District if you wish to inquire further and possibly help with **\"Missing in Action\"**.")
            # (The actual quest start would be handled when the player talks to Fralia; this is a narrative nudge.)
    
    # Descriptive trigger: entering the Cloud District for the first time
    if "cloud district" in loc or "dragonsreach" in loc:
        # Cloud District and Dragonsreach are effectively the same area for triggers.
        if not campaign_state.get("whiterun_cloud_intro_done"):
            events.append("You ascend to the Cloud District, the highest terrace of Whiterun. The wind picks up slightly as you approach **Dragonsreach**, the grand keep perched above the city. Guards at the great wooden doors nod as you pass. From this height, the view of Whiterun and the plains beyond is breathtaking – you truly feel as though you walk among the clouds. Within Dragonsreach awaits Jarl Balgruuf's court, the seat of power in Whiterun Hold.")
            campaign_state["whiterun_cloud_intro_done"] = True
        else:
            events.append("You are in Whiterun's Cloud District, standing before the towering hall of Dragonsreach. The palace dominates the skyline, its great porch offering a view of the hold. Courtiers and guards move about quietly; this high up, the clamor of the city below is but a distant murmur.")
        
        # Event trigger: Audience with Jarl (if a major plot brings the player here for the first time, e.g., after dragon fight or for civil war)
        if campaign_state.get("dragon_rising_completed") and not campaign_state.get("jarl_audience_done"):
            events.append("*(An aide escorts you into the Great Hall where Jarl **Balgruuf** awaits, eager to hear news of the dragon attack and your role in it...)*")
            campaign_state["jarl_audience_done"] = True
            # (This represents the formal audience with Balgruuf after the Western Watchtower dragon battle.)
    
    return events
