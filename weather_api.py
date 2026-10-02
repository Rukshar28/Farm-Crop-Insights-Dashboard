"""Retrieve current weather using Open-Meteo's public geocoding and forecast APIs.

Uses only Python's standard library. No API key is required.
"""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(RuntimeError):
    """Raised when a location or weather response cannot be retrieved."""


def _get_json(url, params, timeout=15):
    request = Request(
        f"{url}?{urlencode(params)}",
        headers={"User-Agent": "FarmCropInsightsDashboard/1.0"}
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise WeatherAPIError(f"Weather service request failed: {exc}") from exc


def fetch_current_weather(location):
    """Resolve a place name, then retrieve current weather for its coordinates."""
    location = location.strip()
    if not location:
        raise ValueError("Location cannot be blank.")

    geo = _get_json(GEOCODING_URL, {"name": location, "count": 1, "language": "en", "format": "json"})
    results = geo.get("results") or []
    if not results:
        raise WeatherAPIError(f"No matching location found for {location!r}.")

    place = results[0]
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "auto",
    }
    payload = _get_json(FORECAST_URL, params)
    current = payload.get("current")
    if not isinstance(current, dict):
        raise WeatherAPIError("Weather service response did not include current conditions.")

    return {
        "location_name": place.get("name", location),
        "country": place.get("country", ""),
        "latitude": float(place["latitude"]),
        "longitude": float(place["longitude"]),
        "observed_at": current.get("time", ""),
        "temperature_c": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "precipitation_mm": current.get("precipitation"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "source": "Open-Meteo",
    }
