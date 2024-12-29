from rapidfuzz import process

KNOWN_CITIES = {
    "Kyiv": ["Киев", "Kiev", "Kyiv"],
    "Tokyo": ["Токио", "Tokyo"],
    "London": ["Londn", "London"],
    "New York": ["New York", "NY", "NewYork"]
}

def clean_city_name(city):
    """Normalize and correct city names."""
    for correct_name, variants in KNOWN_CITIES.items():
        if city in variants:
            return correct_name
    # Fuzzy matching for unknown cities
    best_match = process.extractOne(city, KNOWN_CITIES.keys(), score_cutoff=80)
    return best_match[0] if best_match else city
