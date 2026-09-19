import os

from groq import Groq


def generate_weather_explanation(weather):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is not configured.")

    client = Groq(api_key=api_key)

    prompt = f"""
You are an AI weather assistant.

Analyze ONLY the weather information provided below.

Weather information:
City: {weather["city"]}, {weather["country"]}
Temperature: {weather["temperature"]}°C
Feels like: {weather["feels_like"]}°C
Condition: {weather["condition"]}
Humidity: {weather["humidity"]}%
Wind speed: {weather["wind_speed"]} km/h
Wind direction: {weather["wind_direction"]}
Pressure: {weather["pressure"]} hPa
Visibility: {weather["visibility"]} km
Cloud coverage: {weather["cloud"]}%
UV index: {weather["uv"]}

Generate a short and easy-to-understand weather explanation.

Include:
1. Overall weather condition
2. How the temperature may feel
3. Humidity and wind interpretation
4. One practical general suggestion

Do not invent weather information.
Do not provide a weather forecast.
Do not claim that rain, storms, or other conditions will occur unless they are explicitly present in the supplied data.

Keep the response within 100 words.
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise and reliable weather "
                        "explanation assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq API error: {e}")

        raise ValueError(
            "Unable to generate the AI weather explanation."
        )