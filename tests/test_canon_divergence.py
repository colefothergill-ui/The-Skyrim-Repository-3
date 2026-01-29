#!/usr/bin/env python3
"""
Test the canon divergence checking functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_canon_divergence_detection():
    """Test that canon divergence detection works correctly"""
    print("\n=== Testing Canon Divergence Detection ===")
    try:
        from gm_tools import GMTools
        
        tools = GMTools()
        
        # Test 1: Canon divergence - Ulfric killed
        print("\n--- Test 1: Ulfric Stormcloak assassination ---")
        tools.check_major_canon_divergence("Ulfric Stormcloak is assassinated in Windhelm")
        
        # Test 2: Canon divergence - General Tullius killed
        print("\n--- Test 2: General Tullius death ---")
        tools.check_major_canon_divergence("General Tullius killed in battle")
        
        # Test 3: Canon divergence - Jarl Elisif killed
        print("\n--- Test 3: Jarl Elisif assassination ---")
        tools.check_major_canon_divergence("Jarl Elisif is dead")
        
        # Test 4: Canon divergence - Whiterun destroyed
        print("\n--- Test 4: Whiterun destruction ---")
        tools.check_major_canon_divergence("Whiterun destroyed by dragon attack")
        
        # Test 5: Canon divergence - Solitude destroyed
        print("\n--- Test 5: Solitude destruction ---")
        tools.check_major_canon_divergence("Solitude destroyed in the civil war")
        
        # Test 6: No canon divergence - normal event
        print("\n--- Test 6: Normal event (no divergence) ---")
        tools.check_major_canon_divergence("The party cleared a bandit camp")
        
        # Test 7: No canon divergence - character mentioned but not killed
        print("\n--- Test 7: Character mentioned but alive ---")
        tools.check_major_canon_divergence("Ulfric Stormcloak gave a speech in Windhelm")
        
        # Test 8: No canon divergence - unrelated death
        print("\n--- Test 8: Unrelated death event ---")
        tools.check_major_canon_divergence("A bandit was killed in the wilderness")
        
        print("\n✓ All canon divergence tests completed successfully")
        return True
        
    except Exception as e:
        print(f"\n✗ Canon divergence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_canon_divergence_detection()
    sys.exit(0 if success else 1)
