import aiohttp
import random

API_KEYS = ["key1", "key2", "key3"]  # Replace with your actual API keys.

async def fetch_weather(city):
    """Fetch weather data using a random API key."""
    api_key = random.choice(API_KEYS)
    API_URL = f"https://api.example.com/weather?city={city}&appid={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status != 200:
                raise Exception(f"API error for {city}: {response.status}")
            return await response.json()
