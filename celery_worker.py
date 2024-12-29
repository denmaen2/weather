import logging
from celery import Celery

# Setup logging for Celery
logging.basicConfig(
    level=logging.DEBUG,  # Adjust this to the desired log level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather2.log"),  # Log to weather2.log
        logging.StreamHandler()  # Optional: log to the console as well
    ]
)

logger = logging.getLogger(__name__)

app = Celery('weather_project', broker='redis://localhost:6379/0')


@app.task
def process_weather_task(cities):
    logger.info(f"Processing weather data for cities: {cities}")
    # Your weather processing logic
