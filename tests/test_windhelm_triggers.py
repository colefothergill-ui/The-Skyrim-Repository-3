#!/usr/bin/env python3
"""
Tests for Windhelm (Eastmarch) Location Triggers

This module tests the windhelm_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def test_palace_of_the_kings_first_visit():
    """Test Palace of the Kings first visit trigger"""
    print("\n=== Testing Palace of the Kings First Visit ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Palace first visit"
    assert any("Jarl Ulfric Stormcloak" in event for event in events), "Expected Ulfric mention"
    assert any("throne" in event.lower() for event in events), "Expected throne mention"
    assert campaign_state.get("windhelm_palace_intro_done"), "Expected flag to be set"
    print(f"✓ Palace first visit trigger works: {events[0][:100]}...")


def test_palace_of_the_kings_repeat_visit():
    """Test Palace of the Kings repeat visit trigger"""
    print("\n=== Testing Palace of the Kings Repeat Visit ===")
    
    campaign_state = {"windhelm_palace_intro_done": True}
    
    events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Palace repeat visit"
    assert any("ancient stone walls" in event for event in events), "Expected different description"
    assert not any("all eyes turn to you" in event for event in events), "Expected no first-time greeting"
    print(f"✓ Palace repeat visit trigger works: {events[0][:100]}...")


def test_gray_quarter_first_visit():
    """Test Gray Quarter first visit with racial tension scene"""
    print("\n=== Testing Gray Quarter First Visit ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_gray_quarter", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Gray Quarter first visit"
    assert any("Rolff Stone-Fist" in event for event in events), "Expected Rolff encounter"
    assert any("Dark Elves" in event or "Dunmer" in event for event in events), "Expected Dunmer mention"
    assert campaign_state.get("windhelm_gray_quarter_intro_done"), "Expected flag to be set"
    print(f"✓ Gray Quarter first visit trigger works with racial tension scene")


def test_gray_quarter_repeat_visit():
    """Test Gray Quarter repeat visit trigger"""
    print("\n=== Testing Gray Quarter Repeat Visit ===")
    
    campaign_state = {"windhelm_gray_quarter_intro_done": True}
    
    events = windhelm_location_triggers("windhelm_gray_quarter", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Gray Quarter repeat visit"
    assert not any("Rolff" in event for event in events), "Expected no Rolff on repeat visit"
    assert any("narrow alleyways" in event for event in events), "Expected ambient description"
    print(f"✓ Gray Quarter repeat visit trigger works: {events[0][:100]}...")


def test_stone_quarter_first_visit():
    """Test Stone Quarter (market) first visit trigger"""
    print("\n=== Testing Stone Quarter First Visit ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_stone_quarter", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Stone Quarter first visit"
    assert any("market" in event.lower() for event in events), "Expected market description"
    assert any("Candlehearth Hall" in event for event in events), "Expected Candlehearth Hall mention"
    assert campaign_state.get("windhelm_market_intro_done"), "Expected flag to be set"
    print(f"✓ Stone Quarter first visit trigger works: {events[0][:100]}...")


def test_stone_quarter_market_variation():
    """Test Stone Quarter market location variation"""
    print("\n=== Testing Stone Quarter Market Variation ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_market", campaign_state)
    
    assert len(events) > 0, "Expected events for 'market' keyword"
    assert campaign_state.get("windhelm_market_intro_done"), "Expected flag to be set"
    print(f"✓ Market keyword variation works")


def test_stone_quarter_repeat_visit():
    """Test Stone Quarter repeat visit trigger"""
    print("\n=== Testing Stone Quarter Repeat Visit ===")
    
    campaign_state = {"windhelm_market_intro_done": True}
    
    events = windhelm_location_triggers("windhelm_stone_quarter", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Stone Quarter repeat visit"
    assert any("alive with activity" in event for event in events), "Expected ambient description"
    print(f"✓ Stone Quarter repeat visit trigger works: {events[0][:100]}...")


def test_windhelm_docks_first_visit():
    """Test Windhelm Docks first visit trigger"""
    print("\n=== Testing Windhelm Docks First Visit ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_docks", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Docks first visit"
    assert any("Argonian" in event for event in events), "Expected Argonian workers mention"
    assert any("East Empire Company" in event for event in events), "Expected EEC mention"
    assert campaign_state.get("windhelm_docks_intro_done"), "Expected flag to be set"
    print(f"✓ Docks first visit trigger works: {events[0][:100]}...")


def test_windhelm_docks_harbor_variation():
    """Test Windhelm Docks harbor location variation"""
    print("\n=== Testing Windhelm Harbor Variation ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm_harbor", campaign_state)
    
    assert len(events) > 0, "Expected events for 'harbor' keyword"
    assert campaign_state.get("windhelm_docks_intro_done"), "Expected flag to be set"
    print(f"✓ Harbor keyword variation works")


def test_windhelm_docks_repeat_visit():
    """Test Windhelm Docks repeat visit trigger"""
    print("\n=== Testing Windhelm Docks Repeat Visit ===")
    
    campaign_state = {"windhelm_docks_intro_done": True}
    
    events = windhelm_location_triggers("windhelm_docks", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Docks repeat visit"
    assert any("icy expanse" in event for event in events), "Expected ambient description"
    print(f"✓ Docks repeat visit trigger works: {events[0][:100]}...")


def test_hot_springs_first_visit():
    """Test Eastmarch hot springs first visit trigger"""
    print("\n=== Testing Hot Springs First Visit ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("eastmarch_hot_springs", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for hot springs first visit"
    assert any("hissing hot springs" in event or "bubbling mud pools" in event for event in events), "Expected hot springs description"
    assert any("giant" in event.lower() for event in events), "Expected giant mention"
    assert campaign_state.get("eastmarch_hot_springs_seen"), "Expected flag to be set"
    print(f"✓ Hot springs first visit trigger works: {events[0][:100]}...")


def test_hot_springs_steam_fields_variation():
    """Test hot springs steam fields location variation"""
    print("\n=== Testing Steam Fields Variation ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("eastmarch_steam_fields", campaign_state)
    
    assert len(events) > 0, "Expected events for 'steam fields' keyword"
    assert campaign_state.get("eastmarch_hot_springs_seen"), "Expected flag to be set"
    print(f"✓ Steam fields keyword variation works")


def test_hot_springs_repeat_visit():
    """Test hot springs repeat visit trigger"""
    print("\n=== Testing Hot Springs Repeat Visit ===")
    
    campaign_state = {"eastmarch_hot_springs_seen": True}
    
    events = windhelm_location_triggers("eastmarch_hot_springs", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for hot springs repeat visit"
    assert any("Steam vents" in event or "thermal water" in event for event in events), "Expected steam vents or thermal water description"
    print(f"✓ Hot springs repeat visit trigger works: {events[0][:100]}...")


def test_dunmeth_pass():
    """Test Dunmeth Pass trigger (no first-visit flag, always same)"""
    print("\n=== Testing Dunmeth Pass ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("eastmarch_dunmeth_pass", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Dunmeth Pass"
    assert any("Morrowind" in event for event in events), "Expected Morrowind mention"
    assert any("border" in event.lower() for event in events), "Expected border mention"
    print(f"✓ Dunmeth Pass trigger works: {events[0][:100]}...")


def test_morrowind_border_variation():
    """Test Morrowind border location variation"""
    print("\n=== Testing Morrowind Border Variation ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("eastmarch_morrowind_border", campaign_state)
    
    assert len(events) > 0, "Expected events for 'morrowind border' keyword"
    print(f"✓ Morrowind border keyword variation works")


def test_non_windhelm_location():
    """Test that non-Windhelm/Eastmarch locations return no events"""
    print("\n=== Testing Non-Windhelm Location ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("whiterun", campaign_state)
    
    assert len(events) == 0, "Expected no events for non-Windhelm location"
    print(f"✓ Non-Windhelm location correctly returns no events")


def test_case_insensitive_location():
    """Test that location matching is case-insensitive"""
    print("\n=== Testing Case-Insensitive Location ===")
    
    campaign_state = {}
    
    # Test with uppercase
    events = windhelm_location_triggers("WINDHELM_PALACE_OF_THE_KINGS", campaign_state)
    
    assert len(events) > 0, "Expected events with uppercase location"
    assert campaign_state.get("windhelm_palace_intro_done"), "Expected flag to be set"
    print(f"✓ Case-insensitive location matching works")


def test_empty_location():
    """Test handling of empty/None location"""
    print("\n=== Testing Empty Location ===")
    
    campaign_state = {}
    
    # Test with None
    events = windhelm_location_triggers(None, campaign_state)
    assert len(events) == 0, "Expected no events for None location"
    
    # Test with empty string
    events = windhelm_location_triggers("", campaign_state)
    assert len(events) == 0, "Expected no events for empty location"
    
    print(f"✓ Empty location handling works correctly")


def test_multiple_location_keywords():
    """Test that location can match multiple keywords"""
    print("\n=== Testing Multiple Location Keywords ===")
    
    campaign_state = {}
    
    # Location that starts with "windhelm" and contains "market"
    events = windhelm_location_triggers("windhelm_stone_quarter_market", campaign_state)
    
    assert len(events) > 0, "Expected events for combined location"
    print(f"✓ Multiple keyword matching works")


def test_no_state_pollution():
    """Test that flags are only set for visited locations"""
    print("\n=== Testing No State Pollution ===")
    
    campaign_state = {}
    
    # Visit only one location
    events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
    
    # Only palace flag should be set
    assert campaign_state.get("windhelm_palace_intro_done"), "Expected palace flag"
    assert not campaign_state.get("windhelm_gray_quarter_intro_done"), "Expected no gray quarter flag"
    assert not campaign_state.get("windhelm_market_intro_done"), "Expected no market flag"
    assert not campaign_state.get("windhelm_docks_intro_done"), "Expected no docks flag"
    
    print(f"✓ Flags are set only for visited locations")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Windhelm Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_palace_of_the_kings_first_visit,
        test_palace_of_the_kings_repeat_visit,
        test_gray_quarter_first_visit,
        test_gray_quarter_repeat_visit,
        test_stone_quarter_first_visit,
        test_stone_quarter_market_variation,
        test_stone_quarter_repeat_visit,
        test_windhelm_docks_first_visit,
        test_windhelm_docks_harbor_variation,
        test_windhelm_docks_repeat_visit,
        test_hot_springs_first_visit,
        test_hot_springs_steam_fields_variation,
        test_hot_springs_repeat_visit,
        test_dunmeth_pass,
        test_morrowind_border_variation,
        test_non_windhelm_location,
        test_case_insensitive_location,
        test_empty_location,
        test_multiple_location_keywords,
        test_no_state_pollution,
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
