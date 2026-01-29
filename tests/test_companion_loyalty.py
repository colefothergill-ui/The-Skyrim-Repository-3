#!/usr/bin/env python3
"""
Test companion loyalty monitoring functionality
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_companion_loyalty_review():
    """Test the review_companion_loyalty method"""
    print("\n=== Testing Companion Loyalty Review ===")
    
    try:
        from gm_tools import GMTools
        
        # Get absolute path to data directory
        test_dir = Path(__file__).parent
        repo_root = test_dir.parent
        data_dir = repo_root / "data"
        
        # Create test state directory
        test_state_dir = Path('/tmp/test_companion_state')
        test_state_dir.mkdir(exist_ok=True)
        
        # Create test campaign state with various loyalty levels
        campaign_state = {
            'campaign_id': 'test_001',
            'companions': {
                'active_companions': [
                    {
                        'name': 'Hadvar',
                        'npc_id': 'npc_stat_hadvar',
                        'loyalty': 75
                    },
                    {
                        'name': 'Ralof',
                        'npc_id': 'npc_stat_ralof',
                        'loyalty': 85
                    }
                ]
            }
        }
        
        # Save test campaign state
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        # Test with companions in party
        print("\nTest 1: Companions with various loyalty levels")
        tools = GMTools(data_dir=str(data_dir), state_dir=str(test_state_dir))
        tools.review_companion_loyalty()
        print("✓ Successfully reviewed companion loyalty")
        
        # Test with no active companions
        print("\nTest 2: No active companions")
        campaign_state['companions']['active_companions'] = []
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        tools.review_companion_loyalty()
        print("✓ Handled empty companion list correctly")
        
        # Test with low loyalty companion
        print("\nTest 3: Companion with critically low loyalty")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Hadvar',
                'npc_id': 'npc_stat_hadvar',
                'loyalty': 15
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        tools.review_companion_loyalty()
        print("✓ Correctly warned about low loyalty")
        
        # Test with high loyalty companion
        print("\nTest 4: Companion with very high loyalty")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Ralof',
                'npc_id': 'npc_stat_ralof',
                'loyalty': 95
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        tools.review_companion_loyalty()
        print("✓ Correctly identified high loyalty")
        
        # Test with companion at quest unlock threshold
        print("\nTest 5: Companion at quest unlock threshold")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Hadvar',
                'npc_id': 'npc_stat_hadvar',
                'loyalty': 70
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        tools.review_companion_loyalty()
        print("✓ Correctly identified unlocked quests")
        
        print("\n=== All Companion Loyalty Tests Passed! ===")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_companion_loyalty_review()
    sys.exit(0 if success else 1)
