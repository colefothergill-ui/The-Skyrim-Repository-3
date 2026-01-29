"""
Falkreath Hold & Dark Brotherhood Triggers Script

This script defines scene triggers and events for Falkreath Hold, including its somber local flavor and the Dark Brotherhood Sanctuary integration.
When certain conditions are met (entering Falkreath, visiting specific locations, or key quest choices), these functions can be called to produce narrative scenes or update the game state.
"""

def scene_falkreath_arrival(party_state=None):
    """
    Scene trigger: Party arrives in Falkreath for the first time.
    Describes the town's mournful atmosphere and expansive graveyard.
    """
    description = ("The road descends into Falkreath, a quiet town shrouded in mist. "
                   "Dozens of weathered gravestones line the outskirts – Falkreath's legendary graveyard. "
                   "Villagers cast cautious, melancholic glances as you pass. "
                   "The air smells of rain and freshly turned earth, and an almost tangible sadness clings to the town.")
    print(description)
    if party_state is not None:
        party_state['seen_falkreath_intro'] = True  # mark that Falkreath's intro scene has been shown

def scene_falkreath_graveyard(party_state=None):
    """
    Scene trigger: Party visits the Falkreath graveyard.
    Provides a somber descriptive event reflecting Falkreath's theme of mortality.
    """
    scene = ("You wander between rows of tombstones in Falkreath's great graveyard. "
             "A soft fog rolls over the grass. Under a gnarled tree, a grieving couple whispers prayers to Arkay for a recently lost daughter. "
             "Nearby, Runil the priest methodically tends to each headstone, his lips moving in silent rites. "
             "In the distance, a lone wolf howls – a lonely sound that underscores the pervasive silence of the dead.")
    print(scene)
    if party_state is not None:
        party_state['witnessed_graveyard_scene'] = True  # flag that graveyard scene occurred

def trigger_siddgeir_bandit_bounty(campaign_state):
    """
    Event trigger: Jarl Siddgeir offers his bandit bounty quest if not already taken.
    """
    if not campaign_state.get('falkreath_bandit_quest_given'):
        dialogue = ("Jarl Siddgeir lounges on his throne, swirling a mug of ale. He eyes you with lazy interest. "
                    "\"You there,\" he drawls, \"Word has it you can handle yourself. Falkreath has a little bandit problem – "
                    "some ruffians holed up in Bilegulch Mine. Deal with them for me. Do it well, and maybe I'll reward you. Perhaps even make you Thane, if I'm impressed.\"")
        print(dialogue)
        campaign_state['falkreath_bandit_quest_given'] = True

def trigger_dengeir_vampire_hunt(campaign_state):
    """
    Event trigger: Dengeir of Stuhn requests a vampire hunt.
    Should be called if Dengeir is in a position to give quests (either as an ex-Jarl in town or as the reinstated Jarl).
    """
    if not campaign_state.get('dengeir_vampire_quest_given'):
        request = ("Dengeir of Stuhn pulls you aside with a conspiratorial whisper. Despite the daylight, he looks over his shoulder nervously. "
                   "\"There's evil in the shadows of this town,\" he insists. \"When I was Jarl, I kept an eye out for it. I suspect a vampire lives among us, or in the hills nearby. "
                   "Find it. Destroy it. Do this, and you'll be doing Falkreath – and me – a great service.\"")
        print(request)
        campaign_state['dengeir_vampire_quest_given'] = True

def trigger_dark_brotherhood_contact(party_actions, campaign_state):
    """
    Event trigger: Initiates Dark Brotherhood contact if conditions are met.
    Call when the party commits a significant murder or completes the 'Innocence Lost' quest (Aventus Aretino).
    """
    if (party_actions.get('innocence_lost_completed') or party_actions.get('murder_committed')) and not campaign_state.get('dark_brotherhood_contacted'):
        note_scene = ("Late at night, as you settle in to rest, a courier delivers a small, black-sealed note. "
                      "Breaking the seal, you find only a scrawled handprint and the words, \"We Know.\" "
                      "A chill runs down your spine – the Dark Brotherhood has taken notice of your actions.")
        print(note_scene)
        campaign_state['dark_brotherhood_contacted'] = True
        # The next time the party sleeps, Astrid's abduction scene should be triggered.

def scene_astrid_abduction(campaign_state):
    """
    Scene trigger: Astrid abducts the party for the Dark Brotherhood initiation.
    To be invoked when the party sleeps after Brotherhood contact.
    """
    if campaign_state.get('dark_brotherhood_contacted') and not campaign_state.get('dark_brotherhood_joined'):
        scene = ("You awaken groggily, wrists stiff, to the scent of pine and… old blood. "
                 "As your eyes adjust, you realize you're in a dimly lit shack somewhere in the woods. "
                 "Three figures kneel before you, bound and blindfolded, whimpering. "
                 "Behind you, a woman's voice: \"Good. You're awake.\" Turning, you see Astrid – leader of the Dark Brotherhood in Skyrim – leaning casually against the wall. "
                 "She smirks. \"I'm Astrid. And you, my friend, are here because someone wants these people dead. Let's see if you're Dark Brotherhood material…\"")
        print(scene)
        campaign_state['astrid_abduction_scene'] = True
        # At this point, the player must choose how to resolve Astrid's test (kill a captive or even attempt to attack Astrid).

def trigger_sanctuary_discovery(player_location, campaign_state):
    """
    Event trigger: Party discovers the Dark Brotherhood Sanctuary door if in vicinity and Sanctuary still hidden.
    Should be called when the party explores near the sanctuary location in Falkreath's woods.
    """
    if "Dark Brotherhood Sanctuary" in player_location and not campaign_state.get('dark_brotherhood_sanctuary_discovered'):
        riddle = ("Tucked into a hillside, you notice an ominous black door adorned with a skull carving. "
                  "As you draw near, the door itself seems to speak, a cold whisper: \"What is the music of life?\"")
        print(riddle)
        campaign_state['dark_brotherhood_sanctuary_discovered'] = True
        # The correct answer is required to enter. If the party knows the passphrase or has a member, they can respond and gain entry.

def trigger_sanctuary_entry(campaign_state):
    """
    Event trigger: Party enters the Dark Brotherhood Sanctuary for the first time as members.
    Prints a scene welcoming them inside the Sanctuary.
    """
    if campaign_state.get('dark_brotherhood_member') and not campaign_state.get('dark_brotherhood_sanctuary_entered'):
        scene = ("The Black Door swings open, revealing a torch-lit cavern. Inside, whispers cease as you step into the Dark Brotherhood Sanctuary. "
                 "Shrouded figures move in the shadows. Nazir approaches with a nod, Babette gives a childish grin from atop a crate, and a large armored man (Arnbjorn) watches silently. "
                 "Astrid strides forward, hands on her hips. \"Welcome home,\" she says coolly. \"Your new family greets you.\"")
        print(scene)
        campaign_state['dark_brotherhood_sanctuary_entered'] = True

# End of Falkreath triggers script.
# These functions can be invoked by the game master or automated engine when appropriate conditions are met, 
# ensuring ChatGPT 5.2 is prompted with the correct narrative scenes or quest hook dialogues.
