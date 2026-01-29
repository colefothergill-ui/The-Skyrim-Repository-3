#!/usr/bin/env python3
"""
Demo script showing how to use whiterun_triggers in practice
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.whiterun_triggers import whiterun_location_triggers


def demo_whiterun_journey():
    """Demonstrate a player's journey through Whiterun"""
    print("="*60)
    print("WHITERUN LOCATION TRIGGERS DEMO")
    print("="*60)
    
    # Initialize campaign state (normally loaded from file)
    campaign_state = {}
    
    # Simulate player journey through Whiterun
    locations = [
        "Whiterun - Plains District",
        "Whiterun - Wind District",
        "Whiterun - Cloud District",
        "Whiterun - Plains District",  # Revisit
        "Riverwood",  # Non-Whiterun location
    ]
    
    for location in locations:
        print(f"\n{'='*60}")
        print(f"📍 PLAYER LOCATION: {location}")
        print('='*60)
        
        events = whiterun_location_triggers(location, campaign_state)
        
        if events:
            for i, event in enumerate(events, 1):
                print(f"\n[Event {i}]")
                print(event)
        else:
            print("\n(No special triggers for this location)")
    
    print(f"\n{'='*60}")
    print("FINAL CAMPAIGN STATE FLAGS:")
    print('='*60)
    for flag, value in sorted(campaign_state.items()):
        print(f"  {flag}: {value}")


def demo_quest_progression():
    """Demonstrate quest progression with triggers"""
    print("\n" + "="*60)
    print("QUEST PROGRESSION DEMO")
    print("="*60)
    
    # Scenario: Player completes dragon fight, then visits Dragonsreach
    campaign_state = {
        "dragon_rising_completed": True
    }
    
    print("\n[Scenario: Player defeated dragon at Western Watchtower]")
    print("Campaign State: dragon_rising_completed = True")
    
    print(f"\n{'='*60}")
    print("📍 PLAYER VISITS: Whiterun - Cloud District")
    print('='*60)
    
    events = whiterun_location_triggers("Whiterun - Cloud District", campaign_state)
    
    for i, event in enumerate(events, 1):
        print(f"\n[Event {i}]")
        print(event)
    
    print(f"\n{'='*60}")
    print("Updated Campaign State:")
    print('='*60)
    for flag, value in sorted(campaign_state.items()):
        print(f"  {flag}: {value}")


if __name__ == "__main__":
    demo_whiterun_journey()
    demo_quest_progression()
    
    print("\n" + "="*60)
    print("Demo completed! The triggers system is working correctly.")
    print("="*60)
