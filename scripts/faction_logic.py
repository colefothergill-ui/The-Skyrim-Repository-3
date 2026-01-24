#!/usr/bin/env python3
"""
Faction Logic Manager for Skyrim TTRPG

This script manages:
- Faction trust clocks
- Faction progression and ranks
- Faction relationships
- Faction rewards and consequences
"""

import json
import os
from pathlib import Path
from datetime import datetime


class FactionManager:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.factions_path = self.data_dir / "factions.json"
        self.factions_dir = self.data_dir / "factions"
        
    def load_factions_data(self):
        """Load comprehensive factions data"""
        if self.factions_path.exists():
            with open(self.factions_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_factions_data(self, data):
        """Save factions data"""
        with open(self.factions_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_individual_faction(self, faction_id):
        """Load individual faction file if it exists"""
        faction_file = self.factions_dir / f"{faction_id}.json"
        if faction_file.exists():
            with open(faction_file, 'r') as f:
                return json.load(f)
        return None
    
    def update_faction_clock(self, faction_id, clock_name, progress_change):
        """
        Update a faction's clock
        
        Args:
            faction_id: ID of the faction
            clock_name: Name of the clock to update
            progress_change: Amount to change (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        # Find faction
        faction = None
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
        
        if not faction or 'clocks' not in faction:
            print(f"Faction '{faction_id}' or its clocks not found")
            return False
        
        # Update the clock
        for clock in faction['clocks']:
            if clock['name'] == clock_name:
                old_progress = clock['progress']
                clock['progress'] = max(0, min(clock['segments'], 
                                              clock['progress'] + progress_change))
                
                print(f"\n{faction['name']} - {clock_name}")
                print(f"Progress: {old_progress} -> {clock['progress']}/{clock['segments']}")
                
                # Check if clock is filled
                if clock['progress'] >= clock['segments']:
                    print(f"⚠️  Clock filled! Effect: {clock['effect']}")
                
                self.save_factions_data(data)
                return True
        
        print(f"Clock '{clock_name}' not found in faction '{faction_id}'")
        return False
    
    def update_faction_relationship(self, faction_id, other_faction, change):
        """
        Update relationship between factions
        
        Args:
            faction_id: ID of the faction
            other_faction: ID of the other faction
            change: Amount to change relationship (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
            
            if 'relationships' in faction:
                old_value = faction['relationships'].get(other_faction, 0)
                new_value = max(-100, min(100, old_value + change))
                faction['relationships'][other_faction] = new_value
                
                print(f"\n{faction['name']} <-> {other_faction}")
                print(f"Relationship: {old_value} -> {new_value}")
                
                self.save_factions_data(data)
                return True
        
        return False
    
    def update_faction_resources(self, faction_id, resource_type, change):
        """
        Update faction resources
        
        Args:
            faction_id: ID of the faction
            resource_type: Type of resource (military_strength, gold, etc.)
            change: Amount to change (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
            
            if 'resources' in faction and resource_type in faction['resources']:
                old_value = faction['resources'][resource_type]
                
                # Handle numeric vs string values
                if isinstance(old_value, (int, float)):
                    new_value = max(0, old_value + change)
                    faction['resources'][resource_type] = new_value
                    print(f"\n{faction['name']} - {resource_type}")
                    print(f"{old_value} -> {new_value}")
                else:
                    print(f"Resource '{resource_type}' is not numeric (value: {old_value})")
                    return False
                
                self.save_factions_data(data)
                return True
        
        return False
    
    def check_faction_status(self, faction_id):
        """
        Display comprehensive faction status
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        faction = None
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
        
        if not faction:
            print(f"Faction '{faction_id}' not found")
            return None
        
        print(f"\n{'='*60}")
        print(f"FACTION: {faction['name']}")
        print(f"{'='*60}")
        print(f"Description: {faction['description']}")
        print(f"Headquarters: {faction['headquarters']}")
        print(f"Leader: {faction['leader']['name']} ({faction['leader']['role']})")
        print(f"Alignment: {faction['alignment']}")
        
        print(f"\n--- Goals ---")
        for i, goal in enumerate(faction['goals'], 1):
            print(f"{i}. {goal}")
        
        print(f"\n--- Clocks ---")
        for clock in faction.get('clocks', []):
            progress_bar = '█' * clock['progress'] + '░' * (clock['segments'] - clock['progress'])
            print(f"{clock['name']}: [{progress_bar}] {clock['progress']}/{clock['segments']}")
            print(f"  Effect: {clock['effect']}")
        
        print(f"\n--- Resources ---")
        for resource, value in faction.get('resources', {}).items():
            print(f"{resource}: {value}")
        
        print(f"\n--- Relationships ---")
        for other_faction, value in faction.get('relationships', {}).items():
            if value >= 50:
                status = "Allied"
            elif value >= 20:
                status = "Friendly"
            elif value >= -20:
                status = "Neutral"
            elif value >= -50:
                status = "Unfriendly"
            else:
                status = "Hostile"
            print(f"{other_faction}: {value} ({status})")
        
        if faction.get('joinable'):
            print(f"\n--- Ranks ---")
            for i, rank in enumerate(faction.get('ranks', []), 1):
                print(f"{i}. {rank}")
        
        return faction
    
    def list_all_factions(self):
        """
        List all major factions
        """
        data = self.load_factions_data()
        if not data:
            return []
        
        print("\n=== Major Factions ===\n")
        factions = []
        
        for faction_id, faction in data.get('major_factions', {}).items():
            print(f"{faction_id}: {faction['name']}")
            print(f"  {faction['description']}")
            print(f"  Leader: {faction['leader']['name']}")
            print()
            factions.append((faction_id, faction['name']))
        
        return factions
    
    def track_player_faction_standing(self, faction_id, player_reputation):
        """
        Track a player's standing with a faction
        
        Args:
            faction_id: ID of the faction
            player_reputation: Reputation score (0-100)
        """
        # This would integrate with PC files
        print(f"Player reputation with {faction_id}: {player_reputation}")
        
        # Determine rank eligibility
        if player_reputation >= 80:
            rank_level = "Highest rank eligible"
        elif player_reputation >= 60:
            rank_level = "High rank eligible"
        elif player_reputation >= 40:
            rank_level = "Mid rank eligible"
        elif player_reputation >= 20:
            rank_level = "Entry rank eligible"
        else:
            rank_level = "Not yet eligible"
        
        print(f"Rank status: {rank_level}")
        return rank_level
    
    def simulate_faction_turn(self, faction_id):
        """
        Simulate a faction's actions in the background
        Advances clocks based on faction's active goals
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id not in data.get('major_factions', {}):
            return False
        
        faction = data['major_factions'][faction_id]
        print(f"\n=== {faction['name']} Turn ===")
        
        # Advance clocks by default amount (1 per turn unless interfered with)
        changes_made = False
        for clock in faction.get('clocks', []):
            if clock['progress'] < clock['segments']:
                old_progress = clock['progress']
                clock['progress'] = min(clock['segments'], clock['progress'] + 1)
                print(f"{clock['name']}: {old_progress} -> {clock['progress']}/{clock['segments']}")
                changes_made = True
                
                if clock['progress'] >= clock['segments']:
                    print(f"⚠️  {clock['name']} completed! {clock['effect']}")
        
        if changes_made:
            self.save_factions_data(data)
        else:
            print("No clock changes this turn")
        
        return changes_made
    
    def faction_conflict_resolution(self, faction1_id, faction2_id):
        """
        Resolve conflict between two factions
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        f1 = data['major_factions'].get(faction1_id)
        f2 = data['major_factions'].get(faction2_id)
        
        if not f1 or not f2:
            return None
        
        print(f"\n=== Faction Conflict: {f1['name']} vs {f2['name']} ===")
        
        # Compare military strength
        str1 = f1['resources'].get('military_strength', 50)
        str2 = f2['resources'].get('military_strength', 50)
        
        print(f"{f1['name']} strength: {str1}")
        print(f"{f2['name']} strength: {str2}")
        
        # Determine outcome
        if str1 > str2:
            winner = f1['name']
            margin = str1 - str2
        elif str2 > str1:
            winner = f2['name']
            margin = str2 - str1
        else:
            winner = "Stalemate"
            margin = 0
        
        print(f"\nOutcome: {winner} (margin: {margin})")
        
        return {
            'winner': winner,
            'margin': margin,
            'f1_strength': str1,
            'f2_strength': str2
        }


def main():
    """Main function for testing"""
    manager = FactionManager()
    
    print("Skyrim Faction Logic Manager")
    print("============================\n")
    
    print("1. List All Factions")
    print("2. Check Faction Status")
    print("3. Update Faction Clock")
    print("4. Update Faction Relationship")
    print("5. Update Faction Resources")
    print("6. Simulate Faction Turn")
    print("7. Faction Conflict Resolution")
    print("8. Exit")
    
    while True:
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            manager.list_all_factions()
        
        elif choice == "2":
            faction_id = input("Faction ID: ").strip()
            manager.check_faction_status(faction_id)
        
        elif choice == "3":
            faction_id = input("Faction ID: ").strip()
            clock_name = input("Clock name: ").strip()
            change = input("Progress change (+/-): ").strip()
            manager.update_faction_clock(faction_id, clock_name, int(change))
        
        elif choice == "4":
            faction_id = input("Faction ID: ").strip()
            other_faction = input("Other faction ID: ").strip()
            change = input("Relationship change (+/-): ").strip()
            manager.update_faction_relationship(faction_id, other_faction, int(change))
        
        elif choice == "5":
            faction_id = input("Faction ID: ").strip()
            resource_type = input("Resource type: ").strip()
            change = input("Change amount (+/-): ").strip()
            manager.update_faction_resources(faction_id, resource_type, int(change))
        
        elif choice == "6":
            faction_id = input("Faction ID: ").strip()
            manager.simulate_faction_turn(faction_id)
        
        elif choice == "7":
            faction1 = input("Faction 1 ID: ").strip()
            faction2 = input("Faction 2 ID: ").strip()
            manager.faction_conflict_resolution(faction1, faction2)
        
        elif choice == "8":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
