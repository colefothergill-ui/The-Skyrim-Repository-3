#!/usr/bin/env python3
"""
Story Progression Script for Skyrim TTRPG

This script automates story progression by:
- Updating faction clocks
- Advancing time and world state
- Generating story events based on current state
- Managing quest progression
"""

import json
import os
from datetime import datetime
from pathlib import Path


class StoryProgressionManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.world_state_path = self.data_dir / "world_state" / "current_state.json"
        self.factions_dir = self.data_dir / "factions"
        self.quests_dir = self.data_dir / "quests"
        
    def load_world_state(self):
        """Load the current world state"""
        if self.world_state_path.exists():
            with open(self.world_state_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_world_state(self, state):
        """Save the world state"""
        with open(self.world_state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def advance_time(self, days=1):
        """Advance the in-game time by specified days"""
        state = self.load_world_state()
        if state:
            state['in_game_days_passed'] += days
            print(f"Advanced time by {days} day(s). Total days: {state['in_game_days_passed']}")
            self.save_world_state(state)
            return True
        return False
    
    def update_faction_clock(self, faction_id, progress_change):
        """Update a faction's clock progress"""
        faction_path = self.factions_dir / f"{faction_id}.json"
        if faction_path.exists():
            with open(faction_path, 'r') as f:
                faction = json.load(f)
            
            if 'clock' in faction:
                old_progress = faction['clock']['progress']
                faction['clock']['progress'] = min(
                    faction['clock']['segments'],
                    max(0, old_progress + progress_change)
                )
                
                with open(faction_path, 'w') as f:
                    json.dump(faction, f, indent=2)
                
                print(f"Updated {faction['name']} clock: {old_progress} -> {faction['clock']['progress']}/{faction['clock']['segments']}")
                
                if faction['clock']['progress'] >= faction['clock']['segments']:
                    print(f"WARNING: {faction['name']} has completed their clock: {faction['clock']['name']}")
                
                return True
        return False
    
    def generate_story_events(self):
        """Generate story events based on world state"""
        state = self.load_world_state()
        if not state:
            return []
        
        events = []
        
        # Check dragon crisis status
        if state['dragon_crisis']['status'] == 'Beginning':
            events.append({
                'type': 'dragon_sighting',
                'description': 'Reports of dragon sightings increase across Skyrim',
                'impact': 'Civilian morale decreases, guards on high alert'
            })
        
        # Check faction standings
        for faction_name, data in state['faction_standings'].items():
            if data['morale'] < 40:
                events.append({
                    'type': 'low_morale',
                    'faction': faction_name,
                    'description': f'{faction_name} morale is critically low',
                    'impact': 'Potential desertions or surrenders'
                })
        
        # Civil war progression
        if state['political_situation']['skyrim_status'] == 'Civil War in progress':
            events.append({
                'type': 'civil_war',
                'description': 'Skirmishes continue along faction borders',
                'impact': 'Trade routes disrupted, civilian casualties'
            })
        
        return events
    
    def progress_quests(self, session_data):
        """Update quest states based on session data"""
        if 'quests_updated' not in session_data:
            return
        
        for quest_update in session_data['quests_updated']:
            quest_files = list(self.quests_dir.glob("*.json"))
            for quest_file in quest_files:
                with open(quest_file, 'r') as f:
                    quest = json.load(f)
                
                if quest['name'] == quest_update['quest']:
                    quest['status'] = quest_update['status']
                    with open(quest_file, 'w') as f:
                        json.dump(quest, f, indent=2)
                    print(f"Updated quest '{quest['name']}' status to: {quest['status']}")
    
    def add_major_event(self, event_description):
        """Add a major event to the world state"""
        state = self.load_world_state()
        if state:
            state['major_events'].append(event_description)
            self.save_world_state(state)
            print(f"Added major event: {event_description}")
            return True
        return False
    
    def generate_rumors(self):
        """Generate new rumors based on current world state"""
        state = self.load_world_state()
        if not state:
            return []
        
        rumors = []
        
        # Dragon-related rumors
        if len(state['dragon_crisis']['dragon_attacks']) > 0:
            rumors.append("I heard the dragons are back. Just like in the old tales!")
            rumors.append("They say someone who can speak the dragon language has appeared.")
        
        # Civil war rumors
        if state['political_situation']['skyrim_status'] == 'Civil War in progress':
            rumors.append("The Stormcloaks are gaining ground in the east.")
            rumors.append("General Tullius is planning a major offensive.")
        
        # Faction-based rumors
        factions = list(self.factions_dir.glob("*.json"))
        for faction_file in factions:
            with open(faction_file, 'r') as f:
                faction = json.load(f)
            if 'clock' in faction and faction['clock']['progress'] > faction['clock']['segments'] * 0.5:
                rumors.append(f"The {faction['name']} are up to something...")
        
        return rumors


def main():
    """Main function to demonstrate story progression capabilities"""
    print("=== Skyrim TTRPG Story Progression Manager ===\n")
    
    manager = StoryProgressionManager()
    
    # Example: Advance time
    print("1. Advancing time...")
    manager.advance_time(1)
    print()
    
    # Example: Update faction clock
    print("2. Updating faction clock...")
    manager.update_faction_clock('whiterun_guard', 1)
    print()
    
    # Example: Generate story events
    print("3. Generating story events...")
    events = manager.generate_story_events()
    for event in events:
        print(f"- [{event['type']}] {event['description']}")
        print(f"  Impact: {event['impact']}")
    print()
    
    # Example: Generate rumors
    print("4. Generating rumors...")
    rumors = manager.generate_rumors()
    for rumor in rumors:
        print(f"- {rumor}")
    print()
    
    print("Story progression complete!")


if __name__ == "__main__":
    main()
