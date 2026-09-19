import os
from datetime import datetime, timezone

import requests


WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


def _wind_direction(degrees):
    directions = (
        "N", "NNE", "NE", "ENE", "E", "ESE",
        "SE", "SSE", "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    )
    return directions[round(degrees / 22.5) % 16] if degrees is not None else "N/A"


def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise ValueError("Weather API key is not configured.")

    params = {
        "appid": api_key,
        "q": city,
        "units": "metric"
    }

    try:
        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            raise ValueError(
                "City not found. Please check the city name."
            )

        if response.status_code in (401, 403):
            raise ValueError(
                "Weather API key is invalid or unauthorized."
            )

        if response.status_code == 429:
            raise ValueError(
                "Weather API request limit reached. Please try again later."
            )

        response.raise_for_status()

        data = response.json()

        location = data["name"]
        system = data["sys"]
        current = data["main"]
        condition = data["weather"][0]
        wind = data.get("wind", {})

        weather = {
            "city": location,
            "region": "",
            "country": system["country"],
            "temperature": current["temp"],
            "feels_like": current["feels_like"],
            "condition": condition["description"].title(),
            "humidity": current["humidity"],
            "wind_speed": round(wind.get("speed", 0) * 3.6, 1),
            "wind_direction": _wind_direction(wind.get("deg")),
            "pressure": current["pressure"],
            "visibility": round(data.get("visibility", 0) / 1000, 1),
            "cloud": data.get("clouds", {}).get("all", 0),
            "uv": "N/A",
            "last_updated": datetime.fromtimestamp(
                data["dt"], timezone.utc
            ).strftime("%Y-%m-%d %H:%M UTC"),
            "icon": (
                "https://openweathermap.org/img/wn/"
                f"{condition['icon']}@2x.png"
            )
        }

        return weather

    except requests.exceptions.Timeout:
        raise ValueError(
            "Weather service timed out. Please try again."
        )

    except requests.exceptions.RequestException:
        raise ValueError(
            "Unable to connect to the weather service."
        )

    except KeyError:
        raise ValueError(
            "Unexpected weather data received."
        )