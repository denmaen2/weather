import logging
from weather.city_utils import clean_city_name
from weather.api_client import fetch_weather
from weather.region_mapper import determine_region
from pathlib import Path
import json

logging.basicConfig(filename="logs/weather.log", level=logging.ERROR)

def process_cities(cities):
    results_by_region = {}

    for city in cities:
        cleaned_city = clean_city_name(city)
        try:
            raw_data = fetch_weather(cleaned_city)
            if raw_data and validate_weather_data(raw_data):
                region = determine_region(cleaned_city)
                result = {
                    "city": cleaned_city,
                    "temperature": raw_data["temperature"]["value"],
                    "description": raw_data["weather"][0]["description"]
                }
                results_by_region.setdefault(region, []).append(result)
        except Exception as e:
            logging.error(f"Error processing city {city}: {e}")

    try:
        # Save results
        task_id = "default_task_id"  # Use task_id from Celery if available
        for region, results in results_by_region.items():
            save_results(task_id, region, results)
    except Exception as e:
        logging.error(f"Error save results: {e}")

    return results_by_region

def validate_weather_data(data):
    """Validate temperature and required fields."""
    if "temperature" not in data or "weather" not in data:
        return False
    temp = data["temperature"].get("value")
    return temp is not None and -50 <= temp <= 50

def save_results(task_id, region, results):
    """Save results in regional files."""
    output_dir = Path(f"weather_data/{region}")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"task_{task_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
