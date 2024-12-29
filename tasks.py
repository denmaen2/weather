from celery import Celery
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather2.log"),
        logging.StreamHandler()
    ]
)

app = Celery(
    "weather_project",
    broker="redis://localhost:6379/0",  # Message broker
    backend="redis://localhost:6379/0",  # Result backend
)

@app.task
def process_weather_task(cities):
    # Simulate some processing
    results = {city: f"Weather data for {city}" for city in cities}
    return results

