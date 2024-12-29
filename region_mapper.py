REGIONS = {
    "Europe": ["Kyiv", "London", "Paris"],
    "America": ["New York", "Los Angeles"],
    "Asia": ["Tokyo", "Beijing"]
}

def determine_region(city):
    """Map city to a region."""
    for region, cities in REGIONS.items():
        if city in cities:
            return region
    return "Unknown"

