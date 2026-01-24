"""
Utility functions for Skyrim TTRPG scripts
"""


def location_matches(search_location, sheet_location):
    """
    Check if a search location matches a stat sheet location.
    
    Uses bidirectional partial matching:
    - Returns True if search term is in sheet location
    - Returns True if sheet location is in search term
    - Case-insensitive comparison
    
    Args:
        search_location: Location to search for (e.g., "Whiterun", "ruins")
        sheet_location: Location from stat sheet (e.g., "Ancient Nordic Ruins")
    
    Returns:
        bool: True if locations match
    
    Examples:
        >>> location_matches("Whiterun", "Whiterun")
        True
        >>> location_matches("ruins", "Ancient Nordic Ruins")
        True
        >>> location_matches("Nordic ruins", "Ancient Nordic Ruins")
        True
        >>> location_matches("Solitude", "Whiterun")
        False
    """
    if not search_location or not sheet_location:
        return False
    
    search_lower = search_location.lower()
    sheet_lower = sheet_location.lower()
    
    # Bidirectional partial match
    return search_lower in sheet_lower or sheet_lower in search_lower
