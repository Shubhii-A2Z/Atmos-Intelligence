import requests

from configs.config import FORECAST_URL, GEOCODE_URL, WEATHER_REQUEST_TIMEOUT

def lookup_weather(location: str)->str:
    geo=requests.get(
        GEOCODE_URL,
        params={"name": location, "count": 1},
        timeout=WEATHER_REQUEST_TIMEOUT
    )

    # If there is any error in the api call
    geo.raise_for_status()

    # fetching the "results" field from json
    matches=geo.json()["results"]

    if not matches:
        return f"We couldn't find a place named {location}"

    place=matches[0]
    latitude=place["latitude"], longitude=place["longitude"]

    # Joining the name and country with a comma
    label=", ".join(
        part for part in (place.get("name"), place.get("country")) if part
    )

    forecast=requests.get(
        FORECAST_URL,
        # Getting the current temperature, weather code and wind speed
        params={"latitude": latitude, "longitude": longitude, "current": "temperature_2m, weather_code, wind_speed_10m"},
        timeout=WEATHER_REQUEST_TIMEOUT
    )

    # If there is any error in the api call
    forecast.raise_for_status()

    # Fetching the "current: {}" json
    current=forecast.json().get("current")

    temperature=current.get("temperature_2m")
    weather_code=current.get("weather_code") # Unique weather code that represents the status of sky (clear, rainy etc..)
    wind_speed=current.get("wind_speed_10m")


    print(geo.json())

    return ""

print(lookup_weather("London"))