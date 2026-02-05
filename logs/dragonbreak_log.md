# Dragonbreak Log

This file tracks all Dragonbreaks (timeline fractures) that occur during the campaign.

## What is a Dragonbreak?

A Dragonbreak is a narrative tool used when player actions irrevocably diverge from Elder Scrolls canon, creating parallel timelines where multiple contradictory truths exist simultaneously.

---

## Active Dragonbreaks

## Dragonbreak: Battle of Whiterun — Parallel Timelines

**Date**: 17th of Last Seed, 4E 201  
**Session**: Session 01 (Insaerndel) / Session 02 (Khagar Yal)  
**Cause**: Two player characters experience the Battle of Whiterun from opposing sides simultaneously  
**Canon Conflict**: A single battle cannot have two different outcomes, yet both campaigns are canonical

**Parallel Timelines**:
- **Timeline A (Khagar Yal - Stormcloak)**: Orsimer Warchief leads Stormcloak assault on Whiterun gates; defeats Hadvar in honorable combat; pushes toward Dragonsreach; public werebear transformation completes Thalmor scent-scry escalation
- **Timeline B (Insaerndel - Imperial)**: Thieves Guild operative defends western gate for Imperials; secures Battle-Born contract; neutralizes Thalmor intelligence node; routes captured ledger to Irileth

**Resolution Strategy**: 
Both timelines proceed independently with separate state files:
- `state/campaign_state.json` — Khagar Yal (Stormcloak perspective)
- `state/campaign_state_insaerndel.json` — Insaerndel (Imperial perspective)

**Affected Elements**:
- **NPCs**: Hadvar (captured in Timeline A, fighting in Timeline B), Olfrid Battle-Born (contacted in Timeline B), Commander Caius (Timeline B)
- **Factions**: Stormcloaks (advancing in Timeline A), Imperial Legion (defending in Timeline B), Thieves Guild (establishing foothold in Timeline B)
- **Locations**: Whiterun western gate, western barricade parapet
- **Key Events**: Thalmor node status (active in Timeline A, neutralized in Timeline B)

**Narrative Impact**: 
- Each timeline maintains internal consistency
- Clock systems (Guild foothold, faction trust, Thalmor operations) track independently
- Future sessions will continue separate timelines unless explicitly merged
- NPCs may have different fates in each timeline

**World Aspect Created**: "The Battle Has Two Truths"

**Status**: Active — Parallel campaigns ongoing

---

*No other active Dragonbreaks*

---

## Resolved/Historical Dragonbreaks

*This section will be populated as Dragonbreaks occur and are resolved during play*

---

## How to Document a Dragonbreak

When a Dragonbreak occurs, add an entry using this template:

```markdown
## Dragonbreak: [Event Name]

**Date**: [In-game date]
**Session**: [Session number]
**Cause**: [Description of player action that caused the timeline fracture]
**Canon Conflict**: [What "should" have happened according to Elder Scrolls lore]
**Resolution**: [How both timelines proceed in the campaign]
**Affected Elements**:
- NPCs: [List of affected NPCs]
- Factions: [List of affected factions]
- Quests: [List of affected quests]
**Narrative Impact**: [How this affects future gameplay and story]
**World Aspect Created**: [Any aspects added to world state]
**Status**: Active/Resolved
```

---

## Example Dragonbreak (Template)

## Dragonbreak: The Fate of Jarl Balgruuf

**Date**: 20th of Last Seed, 4E 201
**Session**: Session 3
**Cause**: Party assassinated Jarl Balgruuf in Dragonsreach during a tense negotiation gone wrong
**Canon Conflict**: Jarl Balgruuf should survive to lead Whiterun through the dragon crisis
**Resolution**: 
- Timeline A: Balgruuf died, Vignar Gray-Mane assumed control, Whiterun joined Stormcloaks
- Timeline B: Balgruuf survived, maintained neutral stance
- Going forward: NPCs have conflicting memories; Whiterun's allegiance remains ambiguous
**Affected Elements**:
- NPCs: Jarl Balgruuf, Vignar Gray-Mane, Irileth, Proventus Avenicci
- Factions: Whiterun Guard, Stormcloaks, Imperial Legion
- Quests: "Dragon Rising", "Battle for Whiterun"
**Narrative Impact**: 
- Whiterun's allegiance is now uncertain and depends on context
- Different NPCs remember different versions of events
- Future quests involving Whiterun will reference both possibilities
**World Aspect Created**: "Time Broke at Dragonsreach"
**Status**: Active

---

*This log should be updated after each session where major divergences from canon occur.*

## Dragonbreak: Test Civil War Split

**Date**: 2026-01-27 00:50:34  
**Timeline Branch**: branch_3  
**Trigger Event**: Test battle outcome

**Description**: Test timeline divergence

---

## Dragonbreak: Test Story Branch

**Date**: 2026-01-27 00:50:34  
**Timeline Branch**: branch_4  
**Trigger Event**: Test story event

**Description**: Test story divergence

---

## Dragonbreak: Test Civil War Split

**Date**: 2026-01-29 17:43:08  
**Timeline Branch**: branch_3  
**Trigger Event**: Test battle outcome

**Description**: Test timeline divergence

---

## Dragonbreak: Test Story Branch

**Date**: 2026-01-29 17:43:08  
**Timeline Branch**: branch_4  
**Trigger Event**: Test story event

**Description**: Test story divergence

---
