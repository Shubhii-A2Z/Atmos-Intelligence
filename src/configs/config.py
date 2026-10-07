import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GEOCODE_URL=os.getenv("GEOCODE_URL")

FORECAST_URL=os.getenv("FORECAST_URL")

WEATHER_REQUEST_TIMEOUT=int(os.getenv("WEATHER_REQUEST_TIMEOUT"))

PROJECT_ROOT=Path(__file__).parent.parent

PROMPTS_DIR=PROJECT_ROOT/"prompts"