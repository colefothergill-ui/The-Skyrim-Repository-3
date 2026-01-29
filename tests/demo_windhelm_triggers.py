#!/usr/bin/env python3
"""
Demo script showing Windhelm triggers in action

This demonstrates the faction-aware triggers for Windhelm,
including Stormcloak welcome, Imperial warning, and recruitment prompts.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def demo_stormcloak_arrival():
    """Demonstrate Stormcloak-aligned player arriving in Windhelm"""
    print("\n" + "="*70)
    print("SCENARIO 1: Stormcloak warrior arrives in Windhelm")
    print("="*70)
    
    campaign_state = {
        "stormcloaks_joined": True
    }
    
    print("\nPlayer Status: Member of the Stormcloaks")
    print("Location: Entering Windhelm")
    print("\nTriggered Events:")
    events = windhelm_location_triggers("windhelm", campaign_state)
    for event in events:
        print(f"  → {event}")


def demo_imperial_arrival():
    """Demonstrate Imperial-aligned player arriving in Windhelm"""
    print("\n" + "="*70)
    print("SCENARIO 2: Imperial soldier arrives in Windhelm")
    print("="*70)
    
    campaign_state = {
        "imperial_legion_joined": True
    }
    
    print("\nPlayer Status: Member of the Imperial Legion")
    print("Location: Entering Windhelm")
    print("\nTriggered Events:")
    events = windhelm_location_triggers("windhelm", campaign_state)
    for event in events:
        print(f"  → {event}")


def demo_neutral_palace():
    """Demonstrate neutral player entering Palace of the Kings"""
    print("\n" + "="*70)
    print("SCENARIO 3: Neutral adventurer visits Palace of the Kings")
    print("="*70)
    
    campaign_state = {}
    
    print("\nPlayer Status: Neutral (no faction allegiance)")
    print("Location: Entering Palace of the Kings")
    print("\nTriggered Events:")
    events = windhelm_location_triggers("palace of the kings", campaign_state)
    for event in events:
        print(f"  → {event}")


def demo_return_visit():
    """Demonstrate that triggers only fire once"""
    print("\n" + "="*70)
    print("SCENARIO 4: Return visit - triggers don't repeat")
    print("="*70)
    
    campaign_state = {
        "stormcloaks_joined": True,
        "windhelm_stormcloak_welcome_done": True
    }
    
    print("\nPlayer Status: Stormcloak member (already welcomed)")
    print("Location: Returning to Windhelm")
    print("\nTriggered Events:")
    events = windhelm_location_triggers("windhelm", campaign_state)
    if not events:
        print("  → (No events - welcome already delivered)")
    else:
        for event in events:
            print(f"  → {event}")


def demo_npc_relationships():
    """Show the NPC relationship updates"""
    print("\n" + "="*70)
    print("SCENARIO 5: Key Eastmarch NPC relationships")
    print("="*70)
    
    print("\nUlfric Stormcloak's view of Brunwulf Free-Winter:")
    print("  → Political opponent in Windhelm who questions his policies;")
    print("     potential replacement Jarl if deposed")
    
    print("\nGalmar Stone-Fist's view of Brunwulf Free-Winter:")
    print("  → Views him with suspicion as an 'Imperial lover' who undermines Ulfric")
    
    print("\nBrunwulf Free-Winter's stance:")
    print("  → Respects Ulfric's love for Skyrim but deeply disagrees with")
    print("     his prejudices; could become Jarl if Ulfric is deposed.")
    print("  → Trusted ally to Windhelm's Dunmer families")


def run_demo():
    """Run all demo scenarios"""
    print("\n" + "="*70)
    print("WINDHELM TRIGGERS DEMONSTRATION")
    print("Showing faction-aware triggers and NPC relationships")
    print("="*70)
    
    demo_stormcloak_arrival()
    demo_imperial_arrival()
    demo_neutral_palace()
    demo_return_visit()
    demo_npc_relationships()
    
    print("\n" + "="*70)
    print("Demo complete! Windhelm now responds to faction allegiances.")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_demo()
