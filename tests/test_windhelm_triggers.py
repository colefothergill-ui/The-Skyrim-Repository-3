#!/usr/bin/env python3
"""
Tests for Windhelm Location Triggers

This module tests the windhelm_location_triggers function to ensure
proper event generation based on location and campaign state, including
faction-based reactions and recruitment prompts.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def test_stormcloak_welcome():
    """Test that Stormcloak-aligned players get a friendly welcome"""
    print("\n=== Testing Stormcloak Welcome Trigger ===")
    
    campaign_state = {
        "stormcloaks_joined": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Stormcloak welcome"
    assert any("Stormcloak colors" in event for event in events), "Expected Stormcloak welcome message"
    assert campaign_state.get("windhelm_stormcloak_welcome_done"), "Expected welcome flag to be set"
    print(f"✓ Stormcloak welcome trigger works: {events}")


def test_imperial_warning():
    """Test that Imperial-aligned players get a hostile warning"""
    print("\n=== Testing Imperial Warning Trigger ===")
    
    campaign_state = {
        "imperial_legion_joined": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Imperial warning"
    assert any("Imperial" in event and "Mind yourself" in event for event in events), "Expected Imperial warning message"
    assert campaign_state.get("windhelm_imperial_warning_done"), "Expected warning flag to be set"
    print(f"✓ Imperial warning trigger works: {events}")


def test_stormcloak_recruitment_prompt():
    """Test that unaligned players get recruitment prompt at Palace"""
    print("\n=== Testing Stormcloak Recruitment Prompt ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("palace of the kings", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for recruitment prompt"
    assert any("Galmar Stone-Fist" in event for event in events), "Expected Galmar recruitment message"
    assert campaign_state.get("stormcloak_recruit_offer_seen"), "Expected recruitment flag to be set"
    print(f"✓ Stormcloak recruitment prompt works: {events}")


def test_no_duplicate_welcome():
    """Test that welcome message only appears once"""
    print("\n=== Testing No Duplicate Welcome ===")
    
    campaign_state = {
        "stormcloaks_joined": True,
        "windhelm_stormcloak_welcome_done": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) == 0, "Expected no events when welcome already done"
    print(f"✓ No duplicate welcome: {events}")


def test_no_duplicate_warning():
    """Test that warning message only appears once"""
    print("\n=== Testing No Duplicate Warning ===")
    
    campaign_state = {
        "imperial_legion_joined": True,
        "windhelm_imperial_warning_done": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) == 0, "Expected no events when warning already done"
    print(f"✓ No duplicate warning: {events}")


def test_no_duplicate_recruitment():
    """Test that recruitment prompt only appears once"""
    print("\n=== Testing No Duplicate Recruitment ===")
    
    campaign_state = {
        "stormcloak_recruit_offer_seen": True
    }
    
    events = windhelm_location_triggers("palace of the kings", campaign_state)
    
    assert len(events) == 0, "Expected no events when recruitment already seen"
    print(f"✓ No duplicate recruitment: {events}")


def test_no_recruitment_if_joined():
    """Test that recruitment prompt doesn't appear if already joined Stormcloaks"""
    print("\n=== Testing No Recruitment if Already Joined ===")
    
    campaign_state = {
        "stormcloaks_joined": True
    }
    
    events = windhelm_location_triggers("palace of the kings", campaign_state)
    
    assert not any("Galmar Stone-Fist steps forward" in event for event in events), "Expected no recruitment if already joined"
    print(f"✓ No recruitment when already joined: {events}")


def test_no_recruitment_if_imperial():
    """Test that recruitment prompt doesn't appear if joined Imperial Legion"""
    print("\n=== Testing No Recruitment if Imperial Legion Member ===")
    
    campaign_state = {
        "imperial_legion_joined": True
    }
    
    events = windhelm_location_triggers("palace of the kings", campaign_state)
    
    assert not any("Galmar Stone-Fist steps forward" in event for event in events), "Expected no recruitment if Imperial Legion member"
    print(f"✓ No recruitment when Imperial Legion member: {events}")


def test_neutral_player():
    """Test neutral player with no faction alignment"""
    print("\n=== Testing Neutral Player ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should not trigger faction-specific messages outside Palace
    assert not any("Stormcloak colors" in event for event in events), "Expected no Stormcloak welcome for neutral"
    assert not any("Mind yourself, Imperial" in event for event in events), "Expected no Imperial warning for neutral"
    print(f"✓ Neutral player gets no faction messages: {events}")


def test_case_insensitive_location():
    """Test that location matching is case-insensitive"""
    print("\n=== Testing Case-Insensitive Location Matching ===")
    
    campaign_state = {
        "stormcloaks_joined": True
    }
    
    # Test various case variations
    events1 = windhelm_location_triggers("WINDHELM", campaign_state)
    campaign_state["windhelm_stormcloak_welcome_done"] = False
    events2 = windhelm_location_triggers("Windhelm", campaign_state)
    campaign_state["windhelm_stormcloak_welcome_done"] = False
    events3 = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events1) > 0 and len(events2) > 0 and len(events3) > 0, "Expected events for all case variations"
    print(f"✓ Case-insensitive matching works")


def test_palace_location_variants():
    """Test that Palace location triggers work with variants including comma format"""
    print("\n=== Testing Palace Location Variants ===")
    
    campaign_state = {}
    
    events1 = windhelm_location_triggers("palace of the kings", campaign_state)
    campaign_state["stormcloak_recruit_offer_seen"] = False
    events2 = windhelm_location_triggers("Palace of the Kings", campaign_state)
    campaign_state["stormcloak_recruit_offer_seen"] = False
    events3 = windhelm_location_triggers("PALACE OF THE KINGS", campaign_state)
    campaign_state["stormcloak_recruit_offer_seen"] = False
    # Test actual format used in data files
    events4 = windhelm_location_triggers("Palace of the Kings, Windhelm", campaign_state)
    campaign_state["stormcloak_recruit_offer_seen"] = False
    events5 = windhelm_location_triggers("Windhelm, Palace of the Kings", campaign_state)
    
    assert all(len(events) > 0 for events in [events1, events2, events3, events4, events5]), "Expected recruitment for all Palace variants"
    print(f"✓ Palace location variants work (including comma formats)")


def test_palace_does_not_trigger_gate_messages():
    """Test that entering Palace with comma format doesn't trigger gate welcome/warning"""
    print("\n=== Testing Palace Doesn't Trigger Gate Messages ===")
    
    # Test Stormcloak member entering Palace shouldn't get gate welcome
    campaign_state = {"stormcloaks_joined": True}
    events = windhelm_location_triggers("Palace of the Kings, Windhelm", campaign_state)
    assert not any("gates of Windhelm" in event for event in events), "Palace entry should not trigger gate welcome"
    assert not campaign_state.get("windhelm_stormcloak_welcome_done"), "Gate welcome flag should not be set at Palace"
    
    # Test Imperial member entering Palace shouldn't get gate warning
    campaign_state = {"imperial_legion_joined": True}
    events = windhelm_location_triggers("Windhelm, Palace of the Kings", campaign_state)
    assert not any("Mind yourself, Imperial" in event for event in events), "Palace entry should not trigger gate warning"
    assert not campaign_state.get("windhelm_imperial_warning_done"), "Gate warning flag should not be set at Palace"
    
    print(f"✓ Palace entry doesn't trigger gate messages")


def run_all_tests():
    """Run all windhelm trigger tests"""
    print("\n" + "="*60)
    print("WINDHELM TRIGGERS TEST SUITE")
    print("="*60)
    
    tests = [
        test_stormcloak_welcome,
        test_imperial_warning,
        test_stormcloak_recruitment_prompt,
        test_no_duplicate_welcome,
        test_no_duplicate_warning,
        test_no_duplicate_recruitment,
        test_no_recruitment_if_joined,
        test_no_recruitment_if_imperial,
        test_neutral_player,
        test_case_insensitive_location,
        test_palace_location_variants,
        test_palace_does_not_trigger_gate_messages
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
