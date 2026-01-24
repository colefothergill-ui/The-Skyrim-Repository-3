#!/usr/bin/env python3
"""
NPC Manager for Skyrim TTRPG

This script manages:
- NPC stats and abilities
- NPC loyalty and relationships
- NPC progression
- Companion management
"""

import json
import os
from pathlib import Path
from datetime import datetime


class NPCManager:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.npcs_dir = self.data_dir / "npcs"
        self.relationships_path = self.data_dir / "npc_relationships.json"
        
    def load_npc(self, npc_id):
        """Load an NPC file"""
        npc_file = self.npcs_dir / f"{npc_id}.json"
        if npc_file.exists():
            with open(npc_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_npc(self, npc_data):
        """Save NPC data"""
        npc_id = npc_data.get('id')
        if not npc_id:
            print("Error: NPC must have an 'id' field")
            return False
        
        self.npcs_dir.mkdir(exist_ok=True)
        npc_file = self.npcs_dir / f"{npc_id}.json"
        
        with open(npc_file, 'w') as f:
            json.dump(npc_data, f, indent=2)
        
        print(f"Saved NPC: {npc_data.get('name', npc_id)}")
        return True
    
    def load_relationships(self):
        """Load NPC relationships data"""
        if self.relationships_path.exists():
            with open(self.relationships_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_relationships(self, data):
        """Save relationships data"""
        with open(self.relationships_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_loyalty(self, npc_id, change, reason=""):
        """
        Update an NPC's loyalty to the party
        
        Args:
            npc_id: ID of the NPC
            change: Amount to change loyalty (+/-)
            reason: Why loyalty changed
        """
        npc = self.load_npc(npc_id)
        if not npc:
            print(f"NPC '{npc_id}' not found")
            return False
        
        # Initialize loyalty if not present
        if 'loyalty' not in npc:
            npc['loyalty'] = 50
        
        old_loyalty = npc['loyalty']
        npc['loyalty'] = max(0, min(100, npc['loyalty'] + change))
        
        print(f"\n{npc['name']} - Loyalty Update")
        print(f"Loyalty: {old_loyalty} -> {npc['loyalty']}")
        if reason:
            print(f"Reason: {reason}")
        
        # Check loyalty thresholds
        if npc['loyalty'] >= 80:
            status = "Deeply loyal - will sacrifice for party"
        elif npc['loyalty'] >= 60:
            status = "Loyal companion"
        elif npc['loyalty'] >= 40:
            status = "Questioning loyalty"
        elif npc['loyalty'] >= 20:
            status = "May refuse dangerous orders"
        else:
            status = "⚠️ At risk of leaving!"
        
        print(f"Status: {status}")
        
        # Record the change
        if 'loyalty_history' not in npc:
            npc['loyalty_history'] = []
        
        npc['loyalty_history'].append({
            'change': change,
            'reason': reason,
            'new_loyalty': npc['loyalty'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.save_npc(npc)
        return True
    
    def update_relationship(self, npc1_id, npc2_id, change, reason=""):
        """
        Update relationship between two NPCs
        
        Args:
            npc1_id: ID of first NPC
            npc2_id: ID of second NPC
            change: Amount to change relationship
            reason: Why it changed
        """
        relationships = self.load_relationships()
        if not relationships:
            print("Relationships data not found")
            return False
        
        # Find or create relationship entry
        # This is simplified - real implementation would be more complex
        print(f"\nRelationship Update: {npc1_id} <-> {npc2_id}")
        print(f"Change: {change:+d}")
        if reason:
            print(f"Reason: {reason}")
        
        # Would update the relationships.json here
        return True
    
    def check_companion_status(self, npc_id):
        """
        Check companion's current status and loyalty
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return None
        
        print(f"\n{'='*60}")
        print(f"COMPANION: {npc['name']}")
        print(f"{'='*60}")
        
        # Basic info
        print(f"Role: {npc.get('role', 'Unknown')}")
        print(f"Faction: {npc.get('faction', 'None')}")
        
        # Loyalty
        loyalty = npc.get('loyalty', 50)
        print(f"\nLoyalty: {loyalty}/100")
        
        loyalty_bar = '█' * (loyalty // 5) + '░' * (20 - (loyalty // 5))
        print(f"[{loyalty_bar}]")
        
        # Stats
        if 'skills' in npc:
            print(f"\n--- Skills ---")
            for skill, value in npc['skills'].items():
                print(f"{skill}: {value}")
        
        # Equipment
        if 'equipment' in npc:
            print(f"\n--- Equipment ---")
            for item_type, items in npc['equipment'].items():
                if items:
                    print(f"{item_type}: {', '.join(items) if isinstance(items, list) else items}")
        
        # Special abilities
        if 'special_abilities' in npc:
            print(f"\n--- Special Abilities ---")
            for ability in npc['special_abilities']:
                print(f"- {ability}")
        
        # Recent loyalty changes
        if 'loyalty_history' in npc and npc['loyalty_history']:
            print(f"\n--- Recent Loyalty Changes ---")
            for entry in npc['loyalty_history'][-5:]:  # Last 5
                print(f"[{entry['timestamp']}] {entry['change']:+d}: {entry['reason']}")
        
        return npc
    
    def create_npc_template(self, name, role, faction=None):
        """
        Create a basic NPC template
        
        Args:
            name: NPC name
            role: NPC role (companion, quest_giver, vendor, etc.)
            faction: Associated faction
        """
        import re
        
        # Create ID from name
        npc_id = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
        npc_id = re.sub(r'_+', '_', npc_id).strip('_')
        
        npc = {
            "id": npc_id,
            "name": name,
            "role": role,
            "faction": faction,
            "level": 1,
            "race": "Nord",
            "class": "Warrior",
            "aspects": {
                "high_concept": f"{role}",
                "trouble": "[To be defined]",
                "aspect_3": "[To be defined]"
            },
            "skills": {
                "Great (+4)": [],
                "Good (+3)": [],
                "Fair (+2)": [],
                "Average (+1)": []
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
            "equipment": {
                "weapons": [],
                "armor": [],
                "items": []
            },
            "personality": "[To be defined]",
            "goals": [],
            "relationships": {},
            "loyalty": 50,
            "notes": f"Created: {datetime.now().strftime('%Y-%m-%d')}"
        }
        
        self.save_npc(npc)
        print(f"Created NPC template: {name} ({npc_id})")
        return npc
    
    def list_npcs(self):
        """List all NPCs in the system"""
        if not self.npcs_dir.exists():
            print("No NPCs directory found")
            return []
        
        npc_files = list(self.npcs_dir.glob("*.json"))
        
        print(f"\n=== NPCs ({len(npc_files)}) ===\n")
        
        npcs = []
        for npc_file in sorted(npc_files):
            with open(npc_file, 'r') as f:
                npc = json.load(f)
                print(f"{npc['id']}: {npc['name']}")
                print(f"  Role: {npc.get('role', 'Unknown')}")
                if 'loyalty' in npc:
                    print(f"  Loyalty: {npc['loyalty']}/100")
                print()
                npcs.append((npc['id'], npc['name']))
        
        return npcs
    
    def companion_loyalty_check(self, npc_id, situation):
        """
        Check if companion will follow through in a difficult situation
        
        Args:
            npc_id: ID of the companion
            situation: Description of the situation
        
        Returns:
            Boolean indicating if companion will comply
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return False
        
        loyalty = npc.get('loyalty', 50)
        
        print(f"\n{npc['name']} - Loyalty Check")
        print(f"Situation: {situation}")
        print(f"Current Loyalty: {loyalty}/100")
        
        # Simple threshold check
        if loyalty >= 80:
            result = "Will follow without question"
            will_comply = True
        elif loyalty >= 60:
            result = "Will follow orders"
            will_comply = True
        elif loyalty >= 40:
            result = "May hesitate or question"
            will_comply = True
        elif loyalty >= 20:
            result = "Likely to refuse dangerous/immoral orders"
            will_comply = False
        else:
            result = "Will refuse and may leave"
            will_comply = False
        
        print(f"Result: {result}")
        return will_comply


def main():
    """Main function for testing"""
    manager = NPCManager()
    
    print("Skyrim NPC Manager")
    print("==================\n")
    
    print("1. List All NPCs")
    print("2. Check NPC/Companion Status")
    print("3. Update Loyalty")
    print("4. Create NPC Template")
    print("5. Loyalty Check for Situation")
    print("6. Exit")
    
    while True:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            manager.list_npcs()
        
        elif choice == "2":
            npc_id = input("NPC ID: ").strip()
            manager.check_companion_status(npc_id)
        
        elif choice == "3":
            npc_id = input("NPC ID: ").strip()
            change = input("Loyalty change (+/-): ").strip()
            reason = input("Reason: ").strip()
            manager.update_loyalty(npc_id, int(change), reason)
        
        elif choice == "4":
            name = input("NPC Name: ").strip()
            role = input("Role: ").strip()
            faction = input("Faction (or blank): ").strip()
            manager.create_npc_template(name, role, faction if faction else None)
        
        elif choice == "5":
            npc_id = input("NPC ID: ").strip()
            situation = input("Situation description: ").strip()
            manager.companion_loyalty_check(npc_id, situation)
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
