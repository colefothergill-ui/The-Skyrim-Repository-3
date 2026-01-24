# Elder Scrolls TTRPG Campaign Module - GM Guide

## Overview

This document provides comprehensive instructions for running the **Elder Scrolls: Skyrim - Fate Core Campaign Module**, the foundational narrative framework for your Skyrim TTRPG campaign. This module integrates the main Dragonborn questline with the civil war and Thalmor conspiracy into a cohesive, Act-based epic.

## Campaign Structure

### Three-Act Framework

The campaign is structured in three acts, each with distinct themes and story focus:

#### **Act I: The Dragon Crisis Begins** (Sessions 1-6)
- **Theme**: Discovery, survival, and choice
- **Focus**: Dragons return, Dragonborn revealed, civil war pressures mount
- **Climax**: Battle of Whiterun (typically session 4-6)
- **Key NPCs**: Jarl Balgruuf, Irileth, Greybeards, Delphine
- **Player Agency**: Party's choice of sides (or neutrality) shapes future story

#### **Act II: Shadows and Secrets** (Sessions 7-14)
- **Theme**: Conspiracy, ancient knowledge, divided loyalties
- **Focus**: Thalmor manipulation revealed, Elder Scrolls sought, civil war escalates
- **Climax**: Season Unending (if civil war unresolved) or continued war
- **Key NPCs**: Elenwen, Delphine, Esbern, Paarthurnax, Legate Rikke or Galmar Stone-Fist
- **Player Agency**: Blades vs. Greybeards choice, civil war commitment or peace

#### **Act III: The World-Eater's Return** (Sessions 15-20)
- **Theme**: Sacrifice, unity, destiny
- **Focus**: Final push to defeat Alduin, civil war resolution
- **Climax**: Sovngarde and battle with Alduin
- **Key NPCs**: Odahviing, ancient heroes, faction leaders
- **Player Agency**: How to unite Skyrim (or not), final stand against Alduin

---

## Main Quest Integration

### Quest Progression Overview

The main questline consists of 15 quests divided across three acts:

**Act I Quests**:
1. Unbound
2. Before the Storm
3. Bleak Falls Barrow
4. Dragon Rising
5. The Way of the Voice
6. The Horn of Jurgen Windcaller
7. A Blade in the Dark

**Act II Quests**:
8. Diplomatic Immunity
9. A Cornered Rat
10. Alduin's Wall
11. The Throat of the World
12. Elder Knowledge
13. The Fallen

**Act III Quests**:
14. The World-Eater's Eyrie
15. Sovngarde

### Key Story Hooks by Quest

Each quest includes story hooks in `/data/quests/main_quests.json`. Here are the critical integration points:

#### **Before the Storm**
- **Hook**: Jarl Balgruuf is under immense pressure from both Imperials and Stormcloaks
- **GM Guidance**: Show the political tension. Both sides want Whiterun's allegiance. Balgruuf tries to stay neutral but knows he can't forever.
- **Foreshadowing**: The Battle of Whiterun is coming

#### **Dragon Rising**
- **Hook**: Dragonborn revealed, all factions want party's allegiance
- **GM Guidance**: This is the "I am Dragonborn" moment. Make it epic. The Greybeards' summons should shake the world.
- **Thalmor Connection**: Thalmor spies begin tracking the Dragonborn

#### **A Blade in the Dark**
- **Hook**: Alduin's true power revealed - he's resurrecting dragons
- **GM Guidance**: The sight of Alduin should be terrifying. This ends Act I and transitions to the conspiracy focus of Act II.

#### **Diplomatic Immunity**
- **Hook**: Thalmor manipulation of the civil war is exposed
- **GM Guidance**: This is the conspiracy reveal. The Thalmor want neither side to win decisively. They're playing both sides.
- **Documents**: Ulfric's dossier should be shocking - he's an unwitting asset

#### **The Throat of the World**
- **Hook**: Paarthurnax revealed, Blades vs. Greybeards conflict begins
- **GM Guidance**: Major moral choice. Paarthurnax represents redemption. The Blades represent justice. Neither is wrong.

#### **The Fallen**
- **Hook**: Civil war and dragon crisis intersect - must pause war if unresolved
- **GM Guidance**: If civil war is still raging, trigger Season Unending. This is where both plot threads collide.

---

## Civil War Integration

### The Battle of Whiterun

**Timing**: Typically occurs during Act I/II transition (sessions 4-6)

**Trigger**: When "Battle of Whiterun Countdown" clock reaches 8/8, or when party advances civil war quests

**Setup**:
- Ulfric issues ultimatum to Balgruuf: "Join us or face attack"
- Balgruuf must choose: Imperial or Stormcloak
- Party may influence this decision based on their relationship with Balgruuf

**Possible Outcomes**:
1. **Imperial Victory**: Whiterun remains neutral/Imperial, Stormcloak momentum slowed
2. **Stormcloak Victory**: Whiterun falls, Ulfric gains major strategic position
3. **Stalemate**: Both sides weakened, Thalmor benefit most

**Integration with Main Quest**:
- If party is pursuing main quest actively, the battle may occur while they're away (at High Hrothgar, etc.)
- Party can return to find Whiterun's allegiance has shifted
- This creates urgency - the world moves forward whether party is there or not

### Civil War Questlines

**Parallel Progression**: Civil war quests run parallel to the main quest. Party can pursue both simultaneously or focus on one.

**Key Civil War Quests** (see `/data/quests/civil_war_quests.json`):
- Joining the Legion/Stormcloaks
- The Jagged Crown
- Message to Whiterun / Battle for Whiterun
- Regional hold battles
- Final assault (Windhelm or Solitude)

**GM Guidance**:
- Don't force the party to choose immediately
- Neutrality is valid but has consequences (pressure from both sides)
- If civil war unresolved by Act III, Season Unending becomes mandatory

### Season Unending (Optional Quest)

**Trigger**: Party needs to use Dragonsreach for "The Fallen" quest, but civil war is still raging

**Purpose**: Temporary truce to allow main quest progression

**Setup**:
- Greybeards host peace conference at High Hrothgar
- Party mediates between Imperials and Stormcloaks
- Thalmor represented by Elenwen (if invited)

**Outcomes**:
- Temporary truce achieved (both sides make concessions)
- Civil war resumes after Alduin is defeated
- Party's negotiation skills affect terms

---

## Thalmor Arcs

### The Thalmor as Villains

The Thalmor are sophisticated antagonists operating on multiple levels:

1. **Public Face**: Diplomatic representatives enforcing the White-Gold Concordat
2. **Secret Agenda**: Prolong civil war, eliminate Talos worship, hunt Blades, investigate dragons
3. **Long Game**: Weaken both Empire and Skyrim for eventual Dominion takeover

### Key Thalmor Schemes (Track with Clocks)

See `/data/clocks/thalmor_influence_clocks.json` for detailed tracking.

#### **Civil War Manipulation**
- **Goal**: Neither side wins decisively
- **Methods**: Intelligence to losing side, sabotage peace efforts, assassinate moderates
- **Exposure**: Diplomatic Immunity quest reveals documents
- **Party Impact**: Exposing this can unite Imperials and Stormcloaks against Thalmor

#### **Talos Persecution**
- **Goal**: Eliminate Talos worship completely
- **Methods**: Justiciar patrols, arrests, shrine destruction
- **Visibility**: High - creates moral dilemmas for party
- **Party Impact**: Defending Talos worshippers increases Thalmor hostility

#### **Blades Elimination**
- **Goal**: Exterminate remaining Blades members
- **Methods**: Active hunting, interrogation, informant networks
- **Connection**: Main quest (Delphine, Esbern, Sky Haven Temple)
- **Party Impact**: Protecting Blades makes party Thalmor enemies

#### **Dragon Crisis Investigation**
- **Goal**: Understand and potentially exploit dragon return
- **Methods**: Intelligence gathering, interrogation, ancient text research
- **Key Question**: Can Dragonborn be controlled or must be eliminated?
- **Party Impact**: Thalmor assess Dragonborn as asset or threat

### Key Thalmor NPCs

#### **Elenwen** (First Emissary)
- **Role**: Spy mistress and political manipulator
- **Location**: Thalmor Embassy
- **Key Scenes**: Helgen (Act I), Diplomatic Immunity (Act II), Season Unending (Act III)
- **Tactics**: Information, leverage, diplomatic immunity
- **Vulnerability**: Exposure of her schemes

#### **Thalmor Justiciars**
- **Role**: Talos worship enforcers
- **Location**: Road patrols, Talos shrines
- **Key Scenes**: Random encounters, enforcing Concordat
- **Tactics**: Shock magic, arrests, intimidation
- **Vulnerability**: Isolated patrols can be ambushed

#### **Ancano** (College Agent)
- **Role**: Thalmor operative at College of Winterhold
- **Location**: College of Winterhold
- **Key Scenes**: College questline (separate from main module)
- **Connection**: Shows Thalmor presence in all major institutions

### Running Thalmor Encounters

**Frequency**: Sparingly - make each encounter meaningful

**Moral Complexity**: Not all Thalmor are cartoonish villains. Some truly believe in their mission.

**Consequences**: Attacking Thalmor has serious repercussions:
- Diplomatic incidents
- Increased patrols
- Price on party's heads
- Imperial cooperation becomes difficult

**Opportunities**: Thalmor can be:
- Sources of intelligence (if captured)
- Temporary allies against greater threats (dragons)
- Diplomatic obstacles
- Direct combat encounters

---

## NPC Overview

### Act I Key NPCs

#### **Jarl Balgruuf the Greater** (Whiterun)
- **Role**: Neutral Jarl under pressure
- **Key Scenes**: Before the Storm, Dragon Rising, Battle for Whiterun
- **Relationship**: Can become strong ally if party proves themselves
- **Conflict**: Must choose sides eventually

#### **Irileth** (Whiterun Housecarl)
- **Role**: Balgruuf's advisor and military commander
- **Key Scenes**: Dragon Rising, Battle for Whiterun
- **Relationship**: Respects strength and loyalty

#### **Greybeards** (High Hrothgar)
- **Role**: Teaches the Way of the Voice
- **Key Scenes**: The Way of the Voice, The Throat of the World
- **Philosophy**: Peace through the Voice, protect Paarthurnax

#### **Delphine** (Blade Agent)
- **Role**: Last Blade operative, dragon hunter
- **Key Scenes**: The Horn of Jurgen Windcaller, A Blade in the Dark, all of Act II
- **Conflict**: Wants Paarthurnax dead

### Act II Key NPCs

#### **Elenwen** (Thalmor First Emissary)
- **Stat Sheet**: `/data/npc_stat_sheets/elenwen.json`
- **Role**: Master manipulator, spy mistress
- **Key Scenes**: Diplomatic Immunity, Season Unending
- **Tactics**: Political pressure, intelligence networks

#### **Esbern** (Blades Historian)
- **Role**: Knowledge of dragon lore and prophecy
- **Key Scenes**: A Cornered Rat, Alduin's Wall
- **Value**: Interprets Alduin's Wall, reveals Dragonrend

#### **Paarthurnax** (Dragon Mentor)
- **Role**: Teaches Dragonborn, reformed dragon
- **Key Scenes**: The Throat of the World
- **Conflict**: Blades want him dead, Greybeards defend him

#### **Legate Rikke** (Imperial Commander)
- **Stat Sheet**: `/data/npc_stat_sheets/legate_rikke.json`
- **Role**: Imperial military leader, secret Talos worshipper
- **Key Scenes**: Civil war quests (Imperial side)
- **Complexity**: Nord serving Empire, conflicted loyalties

#### **Galmar Stone-Fist** (Stormcloak Commander)
- **Stat Sheet**: `/data/npc_stat_sheets/galmar_stonefist.json`
- **Role**: Ulfric's housecarl and war chief
- **Key Scenes**: Civil war quests (Stormcloak side)
- **Personality**: Direct, traditional, absolutely loyal to Ulfric

### Act III Key NPCs

#### **Odahviing** (Dragon Ally)
- **Role**: Captured dragon who becomes ally
- **Key Scenes**: The Fallen, The World-Eater's Eyrie
- **Relationship**: Respects strength, provides transport to Skuldafn

#### **Ancient Heroes** (Sovngarde)
- **Role**: Aid in final battle with Alduin
- **Key Scenes**: Sovngarde
- **Inspiration**: Legendary Nord heroes join the fight

---

## Faction Dynamics

### Trust Clocks

Track party standing with each faction using `/data/clocks/faction_trust_clocks.json`.

**Trust Levels**:
- **0-2**: Stranger (neutral/suspicious)
- **3-5**: Ally (trusted, offers aid)
- **6-8**: Champion (hero status, major support)
- **9-10**: Legend (highest honor, full resources)

### Mutually Exclusive Factions

Some factions cannot both be at high trust:
- **Imperial Legion** vs **Stormcloaks**: Joining one makes the other hostile
- **Blades** vs **Greybeards**: Killing Paarthurnax destroys Greybeard trust
- **Dark Brotherhood**: Destroying them ends that faction path

### Neutral Factions

These don't take sides in the civil war:
- Companions
- Thieves Guild
- College of Winterhold
- Dark Brotherhood (cares only about contracts)

---

## Clock System

### Civil War Clocks

See `/data/clocks/civil_war_clocks.json` for full details.

**Primary Clocks**:
1. **Imperial Military Dominance** (3/10): Imperial progress toward victory
2. **Stormcloak Rebellion Momentum** (4/10): Stormcloak progress toward victory
3. **Battle of Whiterun Countdown** (2/8): Tension builds toward pivotal battle
4. **Thalmor Civil War Manipulation** (2/8): Thalmor efforts to prolong war
5. **Civilian War Weariness** (5/10): Toll on common people

**Advancement Guidance**:
- Advance clocks every 2-3 sessions or after major events
- Player actions should significantly impact progression
- Keep both sides roughly balanced until party commits or Act III

### Thalmor Influence Clocks

See `/data/clocks/thalmor_influence_clocks.json` for full details.

**Primary Clocks**:
1. **Thalmor Influence in Skyrim** (3/10)
2. **Talos Persecution Campaign** (5/10)
3. **Intelligence Network** (4/8)
4. **Blades Elimination** (7/10)
5. **Dragon Crisis Investigation** (2/8)
6. **Ulfric Manipulation** (6/8)

**Advancement Guidance**:
- Advance Thalmor clocks slowly but steadily
- Major setbacks require significant player action (infiltrating embassy, exposing schemes)
- Thalmor plans are long-term

### Faction Trust Clocks

See `/data/clocks/faction_trust_clocks.json` for full details.

Track individual faction relationships:
- Imperial Legion (0/10)
- Stormcloaks (0/10)
- Companions (0/10)
- Thieves Guild (0/10)
- College of Winterhold (0/10)
- Greybeards (0/10)
- Blades (0/10)
- Whiterun (0/10)
- Dark Brotherhood (0/10)

**Update After**:
- Completing faction quests
- Major decisions affecting factions
- Defending/attacking faction members
- Showing respect/disrespect for faction values

---

## GM Best Practices

### Session Structure

**Opening**:
1. Recap previous session
2. Review active clocks and world state
3. Ask: "What are you doing?"

**During Play**:
- Advance clocks based on time passage and player actions
- Show consequences of clock progression (e.g., civilians fleeing Whiterun as Battle clock advances)
- Create urgency through multiple advancing threats

**Closing**:
- Update campaign state
- Advance appropriate clocks
- Foreshadow next session's content

### Pacing Recommendations

**Act I** (4-6 sessions):
- Focus on establishing the world and threats
- Introduce civil war tension but don't force commitment
- Culminate in Dragon Rising (Dragonborn reveal)
- Optional: Battle of Whiterun near end of Act I

**Act II** (6-8 sessions):
- Slower pace for investigation and conspiracy
- Diplomatic Immunity should feel like a heist
- Multiple side quests and faction work
- Build toward The Fallen and potential Season Unending

**Act III** (4-6 sessions):
- Accelerate pace for climax
- Focus on main quest completion
- Resolve civil war (either through victory or peace)
- Epic finale in Sovngarde

### Player Agency

**Respect Choices**:
- Don't force civil war allegiance
- Allow neutrality (with consequences)
- Support creative solutions to problems

**Branching Paths**:
- Paarthurnax: Kill or spare (both valid)
- Civil War: Imperial, Stormcloak, or peace
- Thalmor: Expose, ignore, or work with (reluctantly)

**Consequences Matter**:
- Choices should have lasting impact
- Update world state based on decisions
- NPCs remember party's actions

### Integrating Side Content

**Faction Questlines**: Can run parallel to main quest. Companions, Thieves Guild, College, Dark Brotherhood all have their own arcs.

**Daedric Quests**: Provide moral complexity and powerful rewards. See `/data/daedric_quests.json`.

**Random Encounters**: Use Thalmor Justiciars, civil war patrols, dragon attacks to keep world feeling alive.

---

## Troubleshooting

### "Players Won't Choose a Side"

**Solution**: That's valid! Neutrality has consequences:
- Both sides pressure them
- Battle of Whiterun happens without them
- Season Unending becomes mandatory
- NPCs question their commitment

### "Civil War Is Overshadowing Main Quest"

**Solution**: Use dragons to remind everyone of the real threat:
- Dragon attacks during civil war battles
- NPCs beg party to focus on dragons
- Season Unending: Both sides realize dragons are more important

### "Party Killed Elenwen/Major NPC"

**Solution**: Roll with it!
- Killing Elenwen: Major diplomatic incident, new Thalmor leader (possibly worse)
- Killing Delphine: Lose Blades questline, but creative players might rebuild
- Killing Jarl Balgruuf: Whiterun gets new leader, major story shift

### "Players Want to Skip Main Quest"

**Solution**: That's their choice!
- Dragons continue attacking
- Alduin remains a threat
- World deteriorates without Dragonborn intervention
- Show consequences through NPC suffering

---

## Quick Reference

### Essential Files
- **Main Quests**: `/data/quests/main_quests.json`
- **Civil War Quests**: `/data/quests/civil_war_quests.json`
- **Civil War Clocks**: `/data/clocks/civil_war_clocks.json`
- **Thalmor Clocks**: `/data/clocks/thalmor_influence_clocks.json`
- **Faction Trust**: `/data/clocks/faction_trust_clocks.json`
- **Campaign State**: `/state/campaign_state.json`

### Key NPCs Stat Sheets
- **Galmar Stone-Fist**: `/data/npc_stat_sheets/galmar_stonefist.json`
- **Legate Rikke**: `/data/npc_stat_sheets/legate_rikke.json`
- **Elenwen**: `/data/npc_stat_sheets/elenwen.json`
- **Thalmor Justiciar**: `/data/npc_stat_sheets/thalmor_justiciar.json`

### Python Tools
- **story_manager.py**: Track quest progression, branching decisions
- **faction_logic.py**: Update faction clocks and relationships
- **gm_tools.py**: Campaign overview and suggestions

---

## Conclusion

The Elder Scrolls TTRPG Campaign Module provides a rich, branching narrative that respects player agency while delivering an epic story. The three-act structure, integrated civil war and Thalmor conspiracy, and dynamic clock system create a living world that responds to player choices.

Remember: The best campaigns emerge from the intersection of your preparation and your players' creativity. Use this module as a framework, not a script. Adapt, improvise, and most importantly, have fun!

**May your road lead you to warm sands, and may the Dragonborn's legend be worthy of song.**

---

*For additional guidance, see:*
- `/docs/how_to_gm.md` - Comprehensive GM protocols
- `/CAMPAIGN_INTEGRATION.md` - Technical integration details
- `/README.md` - Repository overview
