import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks import process_weather_task
import json
from pathlib import Path
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather2.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

class WeatherRequest(BaseModel):
    cities: list[str]

@app.post("/weather")
def post_weather(request: WeatherRequest):  # Use the request model here
    cities = request.cities  # Extract the cities from the request model
    task = process_weather_task.delay(cities)
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    logger.info(f"Checking status for task ID: {task_id}")
    if task_result.state == "PENDING":
        logger.info("Task is still running")
        return {"status": "running"}
    elif task_result.state == "FAILURE":
        logger.error(f"Task failed: {task_result.info}")
        return {"status": "failed", "error": str(task_result.info)}
    elif task_result.state == "SUCCESS":
        logger.info(f"Task completed successfully: {task_result.result}")
        return {"status": "completed", "results": task_result.result}

@app.get("/results/{region}")
async def get_results(region: str):
    logger.info(f"Fetching results for region: {region}")
    output_dir = Path(f"weather_data/{region}")
    if not output_dir.exists():
        logger.error(f"Region not found: {region}")
        raise HTTPException(status_code=404, detail="Region not found")
    results = []
    for file in output_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            results.extend(json.load(f))
    logger.info(f"Results retrieved for region {region}: {results}")
    return results

