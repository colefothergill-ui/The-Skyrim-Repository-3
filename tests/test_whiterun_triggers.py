#!/usr/bin/env python3
"""
Test for Whiterun location triggers
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.whiterun_triggers import whiterun_location_triggers


def test_plains_district_first_visit():
    """Test Plains District first visit trigger"""
    print("\n=== Testing Plains District First Visit ===")
    
    campaign_state = {}
    location = "Whiterun - Plains District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have 2 events: intro and feud
    assert len(events) == 2, f"Expected 2 events, got {len(events)}"
    assert "bustle of activity" in events[0], "Missing Plains District intro"
    assert "Gray-Mane" in events[1], "Missing feud encounter"
    assert campaign_state.get("whiterun_plains_intro_done") == True, "Intro flag not set"
    assert campaign_state.get("graymane_feud_seen") == True, "Feud flag not set"
    
    print("✓ Plains District first visit works correctly")
    return True


def test_plains_district_repeat_visit():
    """Test Plains District repeat visit"""
    print("\n=== Testing Plains District Repeat Visit ===")
    
    campaign_state = {
        "whiterun_plains_intro_done": True,
        "graymane_feud_seen": True
    }
    location = "Whiterun - Plains District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should only have repeatable flavor
    assert len(events) == 1, f"Expected 1 event, got {len(events)}"
    assert "lively Plains District" in events[0], "Missing repeatable flavor"
    
    print("✓ Plains District repeat visit works correctly")
    return True


def test_wind_district_first_visit():
    """Test Wind District first visit"""
    print("\n=== Testing Wind District First Visit ===")
    
    campaign_state = {}
    location = "Whiterun - Wind District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have intro only (no quest hook yet)
    assert len(events) == 1, f"Expected 1 event, got {len(events)}"
    assert "Gildergreen" in events[0], "Missing Wind District intro"
    assert campaign_state.get("whiterun_wind_intro_done") == True, "Intro flag not set"
    
    print("✓ Wind District first visit works correctly")
    return True


def test_wind_district_with_quest_hook():
    """Test Wind District with quest hook"""
    print("\n=== Testing Wind District Quest Hook ===")
    
    campaign_state = {
        "whiterun_wind_intro_done": True,
        "graymane_feud_seen": True
    }
    location = "Whiterun - Wind District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have repeatable flavor + quest hook
    assert len(events) == 2, f"Expected 2 events, got {len(events)}"
    assert "Wind District" in events[0], "Missing repeatable flavor"
    assert "Missing in Action" in events[1], "Missing quest hook"
    
    print("✓ Wind District quest hook works correctly")
    return True


def test_cloud_district_first_visit():
    """Test Cloud District first visit"""
    print("\n=== Testing Cloud District First Visit ===")
    
    campaign_state = {}
    location = "Whiterun - Cloud District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have intro only
    assert len(events) == 1, f"Expected 1 event, got {len(events)}"
    assert "Dragonsreach" in events[0], "Missing Cloud District intro"
    assert campaign_state.get("whiterun_cloud_intro_done") == True, "Intro flag not set"
    
    print("✓ Cloud District first visit works correctly")
    return True


def test_cloud_district_with_jarl_audience():
    """Test Cloud District with Jarl audience trigger"""
    print("\n=== Testing Cloud District Jarl Audience ===")
    
    campaign_state = {
        "whiterun_cloud_intro_done": True,
        "dragon_rising_completed": True
    }
    location = "Whiterun - Cloud District"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have repeatable flavor + jarl audience
    assert len(events) == 2, f"Expected 2 events, got {len(events)}"
    assert "Cloud District" in events[0], "Missing repeatable flavor"
    assert "Balgruuf" in events[1], "Missing jarl audience"
    assert campaign_state.get("jarl_audience_done") == True, "Jarl audience flag not set"
    
    print("✓ Cloud District jarl audience works correctly")
    return True


def test_dragonsreach_location():
    """Test Dragonsreach as location name"""
    print("\n=== Testing Dragonsreach Location ===")
    
    campaign_state = {}
    location = "Whiterun - Dragonsreach"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should trigger Cloud District intro
    assert len(events) == 1, f"Expected 1 event, got {len(events)}"
    assert "Dragonsreach" in events[0], "Missing Dragonsreach intro"
    assert campaign_state.get("whiterun_cloud_intro_done") == True, "Intro flag not set"
    
    print("✓ Dragonsreach location works correctly")
    return True


def test_non_whiterun_location():
    """Test non-Whiterun location"""
    print("\n=== Testing Non-Whiterun Location ===")
    
    campaign_state = {}
    location = "Riverwood"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have no events
    assert len(events) == 0, f"Expected 0 events, got {len(events)}"
    
    print("✓ Non-Whiterun location correctly returns no events")
    return True


def test_case_insensitive():
    """Test case insensitivity"""
    print("\n=== Testing Case Insensitivity ===")
    
    campaign_state = {}
    location = "WHITERUN - PLAINS DISTRICT"
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should still trigger events
    assert len(events) == 2, f"Expected 2 events, got {len(events)}"
    
    print("✓ Case insensitivity works correctly")
    return True


def test_none_location():
    """Test None as location"""
    print("\n=== Testing None Location ===")
    
    campaign_state = {}
    location = None
    
    events = whiterun_location_triggers(location, campaign_state)
    
    # Should have no events and not crash
    assert len(events) == 0, f"Expected 0 events, got {len(events)}"
    
    print("✓ None location handled correctly")
    return True


def test_state_persistence():
    """Test that state changes persist across calls"""
    print("\n=== Testing State Persistence ===")
    
    campaign_state = {}
    
    # First visit to Plains District
    events1 = whiterun_location_triggers("Whiterun - Plains District", campaign_state)
    assert len(events1) == 2, "First visit should have 2 events"
    
    # Second visit to Plains District
    events2 = whiterun_location_triggers("Whiterun - Plains District", campaign_state)
    assert len(events2) == 1, "Second visit should have 1 event"
    
    # Visit to Wind District should see feud
    events3 = whiterun_location_triggers("Whiterun - Wind District", campaign_state)
    assert len(events3) == 2, "Wind District should have 2 events (intro + quest hook)"
    
    print("✓ State persistence works correctly")
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("WHITERUN TRIGGERS TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    try:
        results.append(("Plains District First Visit", test_plains_district_first_visit()))
        results.append(("Plains District Repeat Visit", test_plains_district_repeat_visit()))
        results.append(("Wind District First Visit", test_wind_district_first_visit()))
        results.append(("Wind District Quest Hook", test_wind_district_with_quest_hook()))
        results.append(("Cloud District First Visit", test_cloud_district_first_visit()))
        results.append(("Cloud District Jarl Audience", test_cloud_district_with_jarl_audience()))
        results.append(("Dragonsreach Location", test_dragonsreach_location()))
        results.append(("Non-Whiterun Location", test_non_whiterun_location()))
        results.append(("Case Insensitivity", test_case_insensitive()))
        results.append(("None Location", test_none_location()))
        results.append(("State Persistence", test_state_persistence()))
    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
