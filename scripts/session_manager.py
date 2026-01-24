#!/usr/bin/env python3
"""
Session Context Manager for Skyrim TTRPG

This script manages session context by:
- Creating new session logs
- Tracking session progress
- Managing character states during sessions
- Generating session summaries
"""

import json
import os
from datetime import datetime
from pathlib import Path


class SessionContextManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.pcs_dir = self.data_dir / "pcs"
        self.npcs_dir = self.data_dir / "npcs"
        
    def create_session(self, session_number, title, gm, players_present):
        """Create a new session log"""
        session_data = {
            "session_number": session_number,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": title,
            "gm": gm,
            "players_present": players_present,
            "characters_present": [],
            "session_summary": "",
            "key_events": [],
            "npcs_encountered": [],
            "locations_visited": [],
            "quests_updated": [],
            "loot_acquired": [],
            "experience_gained": 0,
            "fate_points_awarded": 0,
            "notes": "",
            "next_session_prep": []
        }
        
        session_file = self.sessions_dir / f"session_{session_number:03d}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"Created session {session_number}: {title}")
        return session_data
    
    def update_session(self, session_number, updates):
        """Update an existing session log"""
        session_file = self.sessions_dir / f"session_{session_number:03d}.json"
        
        if not session_file.exists():
            print(f"Session {session_number} not found!")
            return False
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # Update fields
        for key, value in updates.items():
            if key in session_data:
                if isinstance(session_data[key], list) and isinstance(value, list):
                    # Extend lists
                    session_data[key].extend(value)
                else:
                    # Replace value
                    session_data[key] = value
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"Updated session {session_number}")
        return True
    
    def get_session(self, session_number):
        """Get a session log"""
        session_file = self.sessions_dir / f"session_{session_number:03d}.json"
        
        if session_file.exists():
            with open(session_file, 'r') as f:
                return json.load(f)
        return None
    
    def get_latest_session(self):
        """Get the most recent session"""
        session_files = sorted(self.sessions_dir.glob("session_*.json"))
        if session_files:
            with open(session_files[-1], 'r') as f:
                return json.load(f)
        return None
    
    def update_character_from_session(self, session_number):
        """Update character data based on session results"""
        session = self.get_session(session_number)
        if not session:
            return False
        
        # Update PCs with experience and fate points
        for char_id in session.get('characters_present', []):
            pc_files = list(self.pcs_dir.glob("*.json"))
            for pc_file in pc_files:
                with open(pc_file, 'r') as f:
                    pc = json.load(f)
                
                if pc.get('id') == char_id:
                    # Add experience
                    if 'experience' in pc and 'experience_gained' in session:
                        pc['experience'] += session['experience_gained']
                    
                    # Reset fate points
                    if 'refresh' in pc:
                        pc['fate_points'] = pc['refresh']
                    
                    # Clear stress and mild consequences
                    if 'stress' in pc:
                        pc['stress']['physical'] = [False] * len(pc['stress']['physical'])
                        pc['stress']['mental'] = [False] * len(pc['stress']['mental'])
                    
                    if 'consequences' in pc and pc['consequences'].get('mild'):
                        pc['consequences']['mild'] = None
                    
                    with open(pc_file, 'w') as f:
                        json.dump(pc, f, indent=2)
                    
                    print(f"Updated {pc['name']} from session {session_number}")
        
        return True
    
    def generate_session_summary(self, session_number):
        """Generate a session summary"""
        session = self.get_session(session_number)
        if not session:
            return None
        
        summary = f"# Session {session['session_number']}: {session['title']}\n\n"
        summary += f"**Date**: {session['date']}\n"
        summary += f"**GM**: {session['gm']}\n"
        summary += f"**Players**: {', '.join(session['players_present'])}\n\n"
        
        summary += f"## Summary\n{session.get('session_summary', 'No summary available')}\n\n"
        
        if session.get('key_events'):
            summary += "## Key Events\n"
            for event in session['key_events']:
                summary += f"- {event}\n"
            summary += "\n"
        
        if session.get('npcs_encountered'):
            summary += "## NPCs Encountered\n"
            for npc in session['npcs_encountered']:
                summary += f"- {npc}\n"
            summary += "\n"
        
        if session.get('locations_visited'):
            summary += "## Locations Visited\n"
            for location in session['locations_visited']:
                summary += f"- {location}\n"
            summary += "\n"
        
        if session.get('quests_updated'):
            summary += "## Quest Progress\n"
            for quest in session['quests_updated']:
                summary += f"- {quest['quest']}: {quest['status']}\n"
            summary += "\n"
        
        if session.get('loot_acquired'):
            summary += "## Loot Acquired\n"
            for loot in session['loot_acquired']:
                summary += f"- {loot}\n"
            summary += "\n"
        
        summary += f"## Rewards\n"
        summary += f"- Experience: {session.get('experience_gained', 0)}\n"
        summary += f"- Fate Points: {session.get('fate_points_awarded', 0)}\n\n"
        
        if session.get('notes'):
            summary += f"## GM Notes\n{session['notes']}\n\n"
        
        if session.get('next_session_prep'):
            summary += "## Next Session Preparation\n"
            for prep in session['next_session_prep']:
                summary += f"- {prep}\n"
        
        return summary
    
    def get_campaign_timeline(self):
        """Get a timeline of all sessions"""
        sessions = []
        for session_file in sorted(self.sessions_dir.glob("session_*.json")):
            with open(session_file, 'r') as f:
                session = json.load(f)
            sessions.append({
                'number': session['session_number'],
                'date': session['date'],
                'title': session['title'],
                'key_events': session.get('key_events', [])
            })
        return sessions
    
    def get_character_session_history(self, character_id):
        """Get all sessions a character participated in"""
        sessions = []
        for session_file in sorted(self.sessions_dir.glob("session_*.json")):
            with open(session_file, 'r') as f:
                session = json.load(f)
            if character_id in session.get('characters_present', []):
                sessions.append(session)
        return sessions


def main():
    """Main function to demonstrate session management capabilities"""
    print("=== Skyrim TTRPG Session Context Manager ===\n")
    
    manager = SessionContextManager()
    
    # Example: Get latest session
    print("1. Getting latest session...")
    latest = manager.get_latest_session()
    if latest:
        print(f"Session {latest['session_number']}: {latest['title']}")
        print(f"Date: {latest['date']}")
        print(f"Players: {', '.join(latest['players_present'])}")
    
    # Example: Generate session summary
    print("\n2. Generating session summary...")
    summary = manager.generate_session_summary(1)
    if summary:
        print(summary)
    
    # Example: Get campaign timeline
    print("\n3. Getting campaign timeline...")
    timeline = manager.get_campaign_timeline()
    for session in timeline:
        print(f"\nSession {session['number']} ({session['date']}): {session['title']}")
        if session['key_events']:
            print("  Key Events:")
            for event in session['key_events'][:3]:  # Show first 3
                print(f"    - {event}")
    
    print("\nSession management complete!")


if __name__ == "__main__":
    main()
