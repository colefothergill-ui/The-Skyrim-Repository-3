#!/usr/bin/env python3
"""
Mid-Session Protocol for Skyrim TTRPG

Handles resume-simulation functionality and clock progress tracking.
Supports various clock formats including total_segments.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


def _as_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to an integer.
    
    Args:
        value: The value to convert
        default: Default value if conversion fails
        
    Returns:
        int: The converted integer or default value
    """
    if isinstance(value, int):
        return value
    if isinstance(value, (float, str)):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    return default


def detect_clock_format(obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Detect if an object is a clock and normalize its format.
    
    Supports various clock formats:
    - current/max
    - progress/maximum
    - current/max_progress
    - current/max_segments
    - current/total_segments
    
    Args:
        obj: Dictionary that might represent a clock
        
    Returns:
        Optional[Dict]: Normalized clock dict with 'current' and 'max' keys,
                       or None if not a valid clock
    """
    if not isinstance(obj, dict):
        return None
    
    # Check if this looks like a clock
    has_current = any(k in obj for k in ("current", "progress"))
    has_max = any(k in obj for k in ("max", "maximum", "max_progress", "max_segments", "total_segments"))
    
    if not (has_current and has_max):
        return None
    
    # Normalize to current/max format
    current = _as_int(obj.get("current", obj.get("progress", 0)), 0)
    mx = _as_int(obj.get("max", obj.get("maximum", obj.get("max_progress", obj.get("max_segments", obj.get("total_segments", 0))))), 0)
    
    if mx <= 0:
        return None
    
    return {
        "current": current,
        "max": mx,
        "name": obj.get("name", "Unknown Clock"),
        "description": obj.get("description", "")
    }


def advance_clock(clock: Dict[str, Any], amount: int = 1) -> Dict[str, Any]:
    """
    Advance a clock by a specified amount.
    
    Args:
        clock: Clock dictionary with current/max keys
        amount: Amount to advance (can be negative for setbacks)
        
    Returns:
        Dict: Updated clock dictionary
    """
    normalized = detect_clock_format(clock)
    if not normalized:
        raise ValueError("Invalid clock format")
    
    new_current = max(0, min(normalized["max"], normalized["current"] + amount))
    
    # Update original clock object
    if "current" in clock:
        clock["current"] = new_current
    elif "progress" in clock:
        clock["progress"] = new_current
    
    return clock


def is_clock_complete(clock: Dict[str, Any]) -> bool:
    """
    Check if a clock is complete.
    
    Args:
        clock: Clock dictionary
        
    Returns:
        bool: True if current >= max
    """
    normalized = detect_clock_format(clock)
    if not normalized:
        return False
    
    return normalized["current"] >= normalized["max"]


def get_clock_progress(clock: Dict[str, Any]) -> str:
    """
    Get a human-readable progress string for a clock.
    
    Args:
        clock: Clock dictionary
        
    Returns:
        str: Progress string like "3/5" or "Complete"
    """
    normalized = detect_clock_format(clock)
    if not normalized:
        return "Invalid Clock"
    
    if is_clock_complete(clock):
        return f"Complete ({normalized['current']}/{normalized['max']})"
    
    return f"{normalized['current']}/{normalized['max']}"


def load_clocks_from_file(file_path: Path) -> Dict[str, Any]:
    """
    Load clocks from a JSON file.
    
    Args:
        file_path: Path to the clock file
        
    Returns:
        Dict: Clock data
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Clock file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_clocks_to_file(file_path: Path, data: Dict[str, Any]) -> None:
    """
    Save clocks to a JSON file.
    
    Args:
        file_path: Path to the clock file
        data: Clock data to save
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def find_all_clocks(data: Dict[str, Any], path: str = "") -> Dict[str, Dict[str, Any]]:
    """
    Recursively find all clocks in a data structure.
    
    Args:
        data: Data structure to search
        path: Current path (for tracking location)
        
    Returns:
        Dict: Dictionary mapping paths to clock objects
    """
    clocks = {}
    
    if isinstance(data, dict):
        # Check if this dict itself is a clock
        normalized = detect_clock_format(data)
        if normalized:
            clocks[path] = data
        
        # Recursively check nested structures
        for key, value in data.items():
            new_path = f"{path}/{key}" if path else key
            clocks.update(find_all_clocks(value, new_path))
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            clocks.update(find_all_clocks(item, new_path))
    
    return clocks


def main():
    """Main function for testing the protocol"""
    print("=== Mid-Session Protocol Test ===\n")
    
    # Test clock detection with various formats
    test_clocks = [
        {"name": "Test Clock 1", "current": 3, "max": 5},
        {"name": "Test Clock 2", "progress": 2, "maximum": 8},
        {"name": "Test Clock 3", "current": 1, "max_segments": 4},
        {"name": "Test Clock 4", "current": 2, "total_segments": 6},
    ]
    
    for clock in test_clocks:
        normalized = detect_clock_format(clock)
        if normalized:
            print(f"{normalized['name']}: {get_clock_progress(clock)}")
            print(f"  Complete: {is_clock_complete(clock)}")
        else:
            print(f"Invalid clock: {clock}")
    
    print("\n=== Testing Clock Advancement ===\n")
    test_clock = {"name": "Advancement Test", "current": 2, "max": 5}
    print(f"Initial: {get_clock_progress(test_clock)}")
    advance_clock(test_clock, 1)
    print(f"After +1: {get_clock_progress(test_clock)}")
    advance_clock(test_clock, 2)
    print(f"After +2: {get_clock_progress(test_clock)}")
    

if __name__ == "__main__":
    main()
