#!/usr/bin/env python3
"""
Demo script for Windhelm location triggers
Shows how the triggers work in various Windhelm and Eastmarch locations.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def demo_location(location, campaign_state, title):
    """Demo a specific location trigger"""
    print("\n" + "=" * 70)
    print(f"LOCATION: {title}")
    print("=" * 70)
    
    events = windhelm_location_triggers(location, campaign_state)
    
    if events:
        for i, event in enumerate(events, 1):
            print(f"\n[Event {i}]")
            print(event)
    else:
        print("(No events triggered for this location)")
    
    print("\n" + "-" * 70)


def main():
    """Run a demonstration of Windhelm triggers"""
    print("\n" + "#" * 70)
    print("# WINDHELM & EASTMARCH LOCATION TRIGGERS DEMONSTRATION")
    print("#" * 70)
    
    # Create a fresh campaign state for the demo
    campaign_state = {}
    
    # Demonstrate each location
    print("\n\n### WINDHELM CITY DISTRICTS ###\n")
    
    demo_location(
        "windhelm_palace_of_the_kings",
        campaign_state,
        "Palace of the Kings (First Visit)"
    )
    
    demo_location(
        "windhelm_palace_of_the_kings",
        campaign_state,
        "Palace of the Kings (Repeat Visit)"
    )
    
    demo_location(
        "windhelm_gray_quarter",
        campaign_state,
        "Gray Quarter (First Visit)"
    )
    
    demo_location(
        "windhelm_gray_quarter",
        campaign_state,
        "Gray Quarter (Repeat Visit)"
    )
    
    demo_location(
        "windhelm_stone_quarter",
        campaign_state,
        "Stone Quarter Market (First Visit)"
    )
    
    demo_location(
        "windhelm_stone_quarter",
        campaign_state,
        "Stone Quarter Market (Repeat Visit)"
    )
    
    demo_location(
        "windhelm_docks",
        campaign_state,
        "Windhelm Docks (First Visit)"
    )
    
    demo_location(
        "windhelm_docks",
        campaign_state,
        "Windhelm Docks (Repeat Visit)"
    )
    
    print("\n\n### EASTMARCH WILDERNESS ###\n")
    
    demo_location(
        "eastmarch_hot_springs",
        campaign_state,
        "Hot Springs Area (First Visit)"
    )
    
    demo_location(
        "eastmarch_hot_springs",
        campaign_state,
        "Hot Springs Area (Repeat Visit)"
    )
    
    demo_location(
        "eastmarch_dunmeth_pass",
        campaign_state,
        "Dunmeth Pass (Border with Morrowind)"
    )
    
    print("\n\n" + "#" * 70)
    print("# DEMONSTRATION COMPLETE")
    print("#" * 70)
    print(f"\nCampaign state flags set during demo:")
    for key, value in sorted(campaign_state.items()):
        print(f"  - {key}: {value}")
    print()


if __name__ == "__main__":
    main()
