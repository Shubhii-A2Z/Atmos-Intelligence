import os
from dotenv import load_dotenv

load_dotenv()

GEOCODE_URL=os.getenv("GEOCODE_URL")

FORECAST_URL=os.getenv("FORECAST_URL")

WEATHER_REQUEST_TIMEOUT=int(os.getenv("WEATHER_REQUEST_TIMEOUT"))