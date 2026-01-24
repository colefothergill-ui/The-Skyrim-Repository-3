#!/usr/bin/env python3
"""
Session Zero Script for Skyrim TTRPG

This script guides players through:
- Character creation
- Race selection
- Standing Stone choice
- Faction alignment
- Backstory development
- Campaign setup
"""

import json
import os
from pathlib import Path
from datetime import datetime


class SessionZeroManager:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.source_material_dir = self.data_dir.parent / "source_material" / "converted_pdfs"
        
    def load_races(self):
        """Load race data from converted PDFs"""
        races_file = self.source_material_dir / "races.json"
        if races_file.exists():
            with open(races_file, 'r') as f:
                data = json.load(f)
                return data.get('races', [])
        return []
    
    def load_standing_stones(self):
        """Load standing stone data from converted PDFs"""
        stones_file = self.source_material_dir / "standing_stones.md"
        if stones_file.exists():
            with open(stones_file, 'r') as f:
                content = f.read()
                return content
        return ""
    
    def display_races(self):
        """Display available races"""
        print("\n" + "="*60)
        print("PLAYABLE RACES IN SKYRIM")
        print("="*60)
        
        races = self.load_races()
        for i, race in enumerate(races, 1):
            print(f"\n{i}. {race['name']}")
            print(f"   {race['description']}")
            print(f"   Racial Ability: {race['racial_ability']['name']}")
            print(f"   - {race['racial_ability']['effect']}")
            if 'power' in race:
                print(f"   Racial Power: {race['power']['name']}")
                print(f"   - {race['power']['effect']}")
            print(f"   Skill Bonuses: {', '.join(race['skill_bonuses'])}")
        
        print("\n" + "="*60)
    
    def display_standing_stones(self):
        """Display standing stones information"""
        print("\n" + "="*60)
        print("STANDING STONES OF SKYRIM")
        print("="*60)
        
        # Display summary of main stones
        stones_summary = [
            {
                "name": "The Warrior Stone",
                "effect": "Once per session, +2 to Fight, Shoot, or Athletics in combat",
                "for": "Warriors, Berserkers, Soldiers"
            },
            {
                "name": "The Mage Stone",
                "effect": "Once per session, +2 to Lore for magic or spellcasting",
                "for": "Wizards, Healers, Scholars"
            },
            {
                "name": "The Thief Stone",
                "effect": "Once per session, +2 to Stealth, Deceive, or Notice",
                "for": "Thieves, Assassins, Scouts"
            },
            {
                "name": "The Ritual Stone",
                "effect": "Once per session, reanimate dead to fight for you",
                "for": "Necromancers, Dark mages"
            },
            {
                "name": "The Serpent Stone",
                "effect": "Once per session, paralyze an enemy",
                "for": "Assassins, Control specialists"
            },
            {
                "name": "The Shadow Stone",
                "effect": "Once per session, become invisible",
                "for": "Thieves, Spies"
            },
            {
                "name": "The Steed Stone",
                "effect": "+1 Athletics, ignore armor stealth penalties",
                "for": "Mobile fighters, Scouts"
            },
            {
                "name": "The Lord Stone",
                "effect": "+1 Defend vs physical, +1 Will vs magic",
                "for": "Tanks, Defenders"
            },
            {
                "name": "The Lady Stone",
                "effect": "Recover 1 extra physical stress per scene",
                "for": "Sustained fighters"
            },
            {
                "name": "The Lover Stone",
                "effect": "Bonus milestone progress",
                "for": "Versatile characters"
            },
            {
                "name": "The Atronach Stone",
                "effect": "+2 Lore for magic, but magicka doesn't regenerate naturally",
                "for": "Power mages willing to trade"
            },
            {
                "name": "The Tower Stone",
                "effect": "Once per session, auto-open Average lock",
                "for": "Thieves, Explorers"
            }
        ]
        
        for stone in stones_summary:
            print(f"\n{stone['name']}")
            print(f"  Effect: {stone['effect']}")
            print(f"  Best for: {stone['for']}")
        
        print("\n" + "="*60)
        print("Note: You can change your Standing Stone during play by visiting it in-game")
        print("="*60)
    
    def display_factions(self):
        """Display major factions for alignment"""
        print("\n" + "="*60)
        print("MAJOR FACTIONS IN SKYRIM")
        print("="*60)
        
        factions = [
            {
                "name": "Imperial Legion",
                "description": "The military force of the Empire, fighting to keep Skyrim united",
                "alignment": "Lawful, Order-focused",
                "leader": "General Tullius"
            },
            {
                "name": "Stormcloaks",
                "description": "Rebel faction fighting for Skyrim's independence from the Empire",
                "alignment": "Freedom fighters, Nord-focused",
                "leader": "Ulfric Stormcloak"
            },
            {
                "name": "The Companions",
                "description": "Ancient warrior guild based in Whiterun, honor-bound fighters",
                "alignment": "Neutral, Honor-focused",
                "leader": "Kodlak Whitemane"
            },
            {
                "name": "Thieves Guild",
                "description": "Criminal organization based in Riften, dedicated to stealth and thievery",
                "alignment": "Chaotic Neutral, Profit-focused",
                "leader": "Mercer Frey"
            },
            {
                "name": "Dark Brotherhood",
                "description": "Assassins guild devoted to Sithis and the Night Mother",
                "alignment": "Chaotic Evil, Murder-for-hire",
                "leader": "Astrid (Sanctuary leader)"
            },
            {
                "name": "College of Winterhold",
                "description": "Mages guild dedicated to magical study and research",
                "alignment": "Neutral, Knowledge-focused",
                "leader": "Arch-Mage Savos Aren"
            },
            {
                "name": "The Greybeards",
                "description": "Monks who study the Way of the Voice atop High Hrothgar",
                "alignment": "Lawful Neutral, Peace-focused",
                "leader": "Master Arngeir"
            }
        ]
        
        for faction in factions:
            print(f"\n{faction['name']}")
            print(f"  Description: {faction['description']}")
            print(f"  Alignment: {faction['alignment']}")
            print(f"  Leader: {faction['leader']}")
        
        print("\n" + "="*60)
        print("Note: You can join multiple factions during play")
        print("Some factions conflict with each other (Imperial vs Stormcloak)")
        print("="*60)
    
    def create_character_template(self, player_name, character_name, race, standing_stone):
        """Create a character template JSON"""
        races = self.load_races()
        selected_race = None
        
        for r in races:
            if r['name'].lower() == race.lower():
                selected_race = r
                break
        
        if not selected_race:
            print(f"Warning: Race '{race}' not found in data")
            return None
        
        # Sanitize character name for ID generation
        import re
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', character_name.lower())
        sanitized_name = re.sub(r'_+', '_', sanitized_name).strip('_')
        
        character = {
            "name": character_name,
            "id": f"pc_{sanitized_name}",
            "player": player_name,
            "race": selected_race['name'],
            "standing_stone": standing_stone,
            "level": 1,
            "aspects": {
                "high_concept": f"{selected_race['starting_aspect']}",
                "trouble": "[Player to define]",
                "aspect_3": f"Blessed by {standing_stone}",
                "aspect_4": "[Player to define]",
                "aspect_5": "[Player to define]"
            },
            "skills": {
                "Great (+4)": [],
                "Good (+3)": [],
                "Fair (+2)": [],
                "Average (+1)": []
            },
            "racial_bonuses": {
                "ability": selected_race['racial_ability'],
                "power": selected_race.get('power', {}),
                "skill_bonuses": selected_race['skill_bonuses']
            },
            "stress": {
                "physical": [False, False],
                "mental": [False, False]
            },
            "consequences": {
                "mild": None,
                "moderate": None,
                "severe": None
            },
            "stunts": [],
            "refresh": 3,
            "fate_points": 3,
            "equipment": {
                "weapons": [],
                "armor": [],
                "items": []
            },
            "gold": 100,
            "experience": 0,
            "backstory": "[Player to define during Session Zero]",
            "relationships": {},
            "quests": [],
            "session_history": [],
            "notes": "Created during Session Zero"
        }
        
        return character
    
    def save_character(self, character):
        """Save character to data/pcs/ directory"""
        pcs_dir = self.data_dir / "pcs"
        pcs_dir.mkdir(exist_ok=True)
        
        filename = f"{character['id']}.json"
        filepath = pcs_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(character, f, indent=2)
        
        print(f"\nCharacter saved to: {filepath}")
        return filepath
    
    def create_session_zero_log(self, characters, campaign_info):
        """Create a session zero log file"""
        logs_dir = self.data_dir.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_session-00_Session-Zero.md"
        filepath = logs_dir / filename
        
        log_content = f"""# Session 0: Session Zero - Campaign Setup

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**In-Game Date**: 17th of Last Seed, 4E 201 (Day of Helgen Attack)
**GM**: {campaign_info.get('gm', '[GM Name]')}
**Players Present**: {', '.join([c['player'] for c in characters])}

## Session Summary

This is Session Zero for our Skyrim Fate Core campaign. Players created their characters,
chose their races and Standing Stones, discussed faction alignments, and developed their
backstories.

## Character Creation

"""
        
        for character in characters:
            log_content += f"""### {character['name']} (played by {character['player']})
- **Race**: {character['race']}
- **Standing Stone**: {character['standing_stone']}
- **High Concept**: {character['aspects']['high_concept']}
- **Backstory Summary**: {character.get('backstory', '[To be developed]')}

"""
        
        log_content += f"""
## Campaign Setup

### Campaign Premise
{campaign_info.get('premise', 'Dragons have returned to Skyrim. The civil war between Imperials and Stormcloaks threatens to tear the province apart. Ancient forces stir in the depths of Nordic ruins.')}

### Starting Location
{campaign_info.get('starting_location', 'Riverwood, after escaping Helgen')}

### Initial Hooks
{campaign_info.get('hooks', "- Deliver news of Helgen's destruction to Jarl Balgruuf\n- Investigate dragon sightings\n- Choose a side in the civil war")}

### House Rules Discussed
- Standing Stones can be changed during play by visiting the physical location
- Dragonbreaks will be used for major canon divergences
- Fate Point economy: Compels will be frequent, players encouraged to accept
- Session format: Mix of combat, investigation, and social encounters

### Faction Alignments Discussed
"""
        
        for character in characters:
            factions = character.get('initial_factions', {})
            if factions:
                log_content += f"\n**{character['name']}**: {factions}"
            else:
                log_content += f"\n**{character['name']}**: Undecided on factional loyalties"
        
        log_content += """

## Next Session Preview

The party will begin in Riverwood, having just escaped the destruction of Helgen.
They need to warn Jarl Balgruuf about the dragon attack and decide their next steps.

---

**Session End Time**: Campaign start (pre-adventure)
**Real World Duration**: Session Zero setup
"""
        
        with open(filepath, 'w') as f:
            f.write(log_content)
        
        print(f"\nSession Zero log created: {filepath}")
        return filepath
    
    def run_interactive_session_zero(self):
        """Run interactive Session Zero process"""
        print("\n" + "="*60)
        print("WELCOME TO SKYRIM FATE CORE - SESSION ZERO")
        print("="*60)
        print("\nThis script will guide you through character creation.")
        print("Let's begin!\n")
        
        # Get GM name
        gm_name = input("GM Name: ").strip()
        
        # Get campaign info
        print("\n--- Campaign Setup ---")
        campaign_premise = input("Campaign Premise (or press Enter for default): ").strip()
        if not campaign_premise:
            campaign_premise = "Dragons have returned to Skyrim. The civil war rages. Your story begins..."
        
        starting_location = input("Starting Location (or press Enter for 'Riverwood'): ").strip()
        if not starting_location:
            starting_location = "Riverwood, after escaping Helgen"
        
        campaign_info = {
            'gm': gm_name,
            'premise': campaign_premise,
            'starting_location': starting_location,
            'hooks': '- Warn Jarl Balgruuf about dragons\n- Investigate Helgen\'s destruction\n- Navigate the civil war'
        }
        
        # Get number of players
        while True:
            try:
                num_players = int(input("\nHow many players? "))
                if num_players > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        characters = []
        
        # Create each character
        for i in range(num_players):
            print(f"\n{'='*60}")
            print(f"CHARACTER {i+1} OF {num_players}")
            print("="*60)
            
            player_name = input("Player Name: ").strip()
            character_name = input("Character Name: ").strip()
            
            # Show races
            self.display_races()
            race = input("\nChoose your race (name): ").strip()
            
            # Show standing stones
            self.display_standing_stones()
            standing_stone = input("\nChoose your Standing Stone (name): ").strip()
            
            # Create character
            character = self.create_character_template(
                player_name, character_name, race, standing_stone
            )
            
            if character:
                # Additional backstory prompts
                print("\n--- Backstory Development ---")
                print("Answer these questions to flesh out your character:")
                
                print("\n1. Why were you at Helgen when the dragons attacked?")
                helgen_reason = input("   > ").strip()
                
                print("\n2. What is your relationship to the civil war?")
                civil_war_stance = input("   > ").strip()
                
                print("\n3. What drives you? What are your goals?")
                motivation = input("   > ").strip()
                
                print("\n4. Do you have any significant relationships or connections?")
                connections = input("   > ").strip()
                
                # Build backstory
                backstory = f"""
**Helgen Incident**: {helgen_reason}

**Civil War Stance**: {civil_war_stance}

**Motivation**: {motivation}

**Connections**: {connections}
"""
                character['backstory'] = backstory.strip()
                
                # Faction preferences
                print("\n--- Faction Interests ---")
                self.display_factions()
                faction_interest = input("\nAre you interested in any factions? ").strip()
                character['initial_factions'] = faction_interest
                
                # Save character
                self.save_character(character)
                characters.append(character)
                
                print(f"\n✓ Character '{character_name}' created successfully!")
        
        # Create session zero log
        print("\n--- Creating Session Zero Log ---")
        self.create_session_zero_log(characters, campaign_info)
        
        print("\n" + "="*60)
        print("SESSION ZERO COMPLETE!")
        print("="*60)
        print(f"\nCreated {len(characters)} character(s)")
        print("Character files saved in: data/pcs/")
        print("Session log saved in: logs/")
        print("\nYou're ready to begin your Skyrim adventure!")
        print("="*60)


def main():
    """Main function"""
    print("Skyrim Fate Core - Session Zero Manager")
    print("Choose an option:")
    print("1. Interactive Session Zero (guided character creation)")
    print("2. Display Races")
    print("3. Display Standing Stones")
    print("4. Display Factions")
    print("5. Exit")
    
    manager = SessionZeroManager()
    
    while True:
        try:
            choice = input("\nEnter choice (1-5): ").strip()
        except EOFError:
            print("Goodbye!")
            break
        
        if choice == "1":
            manager.run_interactive_session_zero()
            break
        elif choice == "2":
            manager.display_races()
        elif choice == "3":
            manager.display_standing_stones()
        elif choice == "4":
            manager.display_factions()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
