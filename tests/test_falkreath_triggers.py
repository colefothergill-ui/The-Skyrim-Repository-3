#!/usr/bin/env python3
"""
Tests for Falkreath Location Triggers

This module tests the Falkreath trigger functions to ensure
proper scene generation and quest trigger behavior.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.falkreath_triggers import (
    scene_falkreath_arrival,
    scene_falkreath_graveyard,
    trigger_siddgeir_bandit_bounty,
    trigger_dengeir_vampire_hunt,
    trigger_dark_brotherhood_contact,
    scene_astrid_abduction,
    trigger_sanctuary_discovery,
    trigger_sanctuary_entry
)


def test_falkreath_arrival():
    """Test Falkreath arrival scene"""
    print("\n=== Testing Falkreath Arrival Scene ===")
    
    party_state = {}
    scene_falkreath_arrival(party_state)
    
    assert party_state.get('seen_falkreath_intro') is True, "Expected seen_falkreath_intro flag to be set"
    print("✓ Falkreath arrival scene works and sets flag")


def test_graveyard_scene():
    """Test Falkreath graveyard scene"""
    print("\n=== Testing Graveyard Scene ===")
    
    party_state = {}
    scene_falkreath_graveyard(party_state)
    
    assert party_state.get('witnessed_graveyard_scene') is True, "Expected witnessed_graveyard_scene flag to be set"
    print("✓ Graveyard scene works and sets flag")


def test_siddgeir_bandit_bounty():
    """Test Siddgeir's bandit bounty quest trigger"""
    print("\n=== Testing Siddgeir Bandit Bounty ===")
    
    campaign_state = {}
    trigger_siddgeir_bandit_bounty(campaign_state)
    
    assert campaign_state.get('falkreath_bandit_quest_given') is True, "Expected quest flag to be set"
    print("✓ Siddgeir bandit bounty trigger works")
    
    # Test that it doesn't trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_siddgeir_bandit_bounty(campaign_state)
    assert campaign_state == campaign_state_copy, "Quest should not trigger twice"
    print("✓ Quest correctly does not trigger twice")


def test_dengeir_vampire_hunt():
    """Test Dengeir's vampire hunt quest trigger"""
    print("\n=== Testing Dengeir Vampire Hunt ===")
    
    campaign_state = {}
    trigger_dengeir_vampire_hunt(campaign_state)
    
    assert campaign_state.get('dengeir_vampire_quest_given') is True, "Expected quest flag to be set"
    print("✓ Dengeir vampire hunt trigger works")
    
    # Test that it doesn't trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_dengeir_vampire_hunt(campaign_state)
    assert campaign_state == campaign_state_copy, "Quest should not trigger twice"
    print("✓ Quest correctly does not trigger twice")


def test_dark_brotherhood_contact_innocence_lost():
    """Test Dark Brotherhood contact after Innocence Lost quest"""
    print("\n=== Testing DB Contact (Innocence Lost) ===")
    
    party_actions = {'innocence_lost_completed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is True, "Expected DB contact flag to be set"
    print("✓ Dark Brotherhood contact triggers after Innocence Lost")


def test_dark_brotherhood_contact_murder():
    """Test Dark Brotherhood contact after murder"""
    print("\n=== Testing DB Contact (Murder) ===")
    
    party_actions = {'murder_committed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is True, "Expected DB contact flag to be set"
    print("✓ Dark Brotherhood contact triggers after murder")


def test_dark_brotherhood_no_contact():
    """Test that DB contact doesn't trigger without qualifying actions"""
    print("\n=== Testing DB No Contact (No Qualifying Actions) ===")
    
    party_actions = {}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is not True, "DB contact should not trigger"
    print("✓ Dark Brotherhood correctly does not contact without qualifying actions")


def test_dark_brotherhood_contact_once():
    """Test that DB contact only happens once"""
    print("\n=== Testing DB Contact Only Once ===")
    
    party_actions = {'murder_committed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    assert campaign_state.get('dark_brotherhood_contacted') is True
    
    # Try to trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    assert campaign_state == campaign_state_copy, "DB contact should not trigger twice"
    print("✓ Dark Brotherhood contact correctly triggers only once")


def test_astrid_abduction():
    """Test Astrid abduction scene"""
    print("\n=== Testing Astrid Abduction Scene ===")
    
    campaign_state = {'dark_brotherhood_contacted': True}
    scene_astrid_abduction(campaign_state)
    
    assert campaign_state.get('astrid_abduction_scene') is True, "Expected abduction scene flag to be set"
    print("✓ Astrid abduction scene works")


def test_astrid_abduction_no_contact():
    """Test that abduction doesn't happen without DB contact"""
    print("\n=== Testing Astrid Abduction (No Contact) ===")
    
    campaign_state = {}
    scene_astrid_abduction(campaign_state)
    
    assert campaign_state.get('astrid_abduction_scene') is not True, "Abduction should not occur without DB contact"
    print("✓ Astrid abduction correctly doesn't trigger without DB contact")


def test_sanctuary_discovery():
    """Test sanctuary discovery trigger"""
    print("\n=== Testing Sanctuary Discovery ===")
    
    player_location = "Dark Brotherhood Sanctuary entrance"
    campaign_state = {}
    
    trigger_sanctuary_discovery(player_location, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_discovered') is True, "Expected sanctuary discovered flag"
    print("✓ Sanctuary discovery trigger works")


def test_sanctuary_discovery_once():
    """Test that sanctuary discovery only triggers once"""
    print("\n=== Testing Sanctuary Discovery Only Once ===")
    
    player_location = "Dark Brotherhood Sanctuary entrance"
    campaign_state = {}
    
    trigger_sanctuary_discovery(player_location, campaign_state)
    campaign_state_copy = campaign_state.copy()
    
    # Try to trigger again
    trigger_sanctuary_discovery(player_location, campaign_state)
    assert campaign_state == campaign_state_copy, "Sanctuary discovery should not trigger twice"
    print("✓ Sanctuary discovery correctly triggers only once")


def test_sanctuary_entry():
    """Test sanctuary entry scene"""
    print("\n=== Testing Sanctuary Entry ===")
    
    campaign_state = {'dark_brotherhood_member': True}
    trigger_sanctuary_entry(campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_entered') is True, "Expected sanctuary entered flag"
    print("✓ Sanctuary entry trigger works")


def test_sanctuary_entry_no_member():
    """Test that sanctuary entry doesn't trigger for non-members"""
    print("\n=== Testing Sanctuary Entry (Non-Member) ===")
    
    campaign_state = {}
    trigger_sanctuary_entry(campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_entered') is not True, "Entry should not occur for non-members"
    print("✓ Sanctuary entry correctly doesn't trigger for non-members")


def test_scene_functions_with_none_state():
    """Test that scene functions handle None state gracefully"""
    print("\n=== Testing Scene Functions with None State ===")
    
    try:
        scene_falkreath_arrival(None)
        scene_falkreath_graveyard(None)
        print("✓ Scene functions handle None state gracefully")
    except Exception as e:
        raise AssertionError(f"Scene functions should handle None state: {e}")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Falkreath Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_falkreath_arrival,
        test_graveyard_scene,
        test_siddgeir_bandit_bounty,
        test_dengeir_vampire_hunt,
        test_dark_brotherhood_contact_innocence_lost,
        test_dark_brotherhood_contact_murder,
        test_dark_brotherhood_no_contact,
        test_dark_brotherhood_contact_once,
        test_astrid_abduction,
        test_astrid_abduction_no_contact,
        test_sanctuary_discovery,
        test_sanctuary_discovery_once,
        test_sanctuary_entry,
        test_sanctuary_entry_no_member,
        test_scene_functions_with_none_state,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__} failed: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
