import os

from flask import Flask, render_template, request
from dotenv import load_dotenv

from services.weather_service import get_weather
from services.groq_service import generate_weather_explanation


load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    explanation = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                # Fetch weather information
                weather = get_weather(city)

                # Generate AI explanation
                explanation = generate_weather_explanation(weather)

            except ValueError as e:
                error = str(e)

            except Exception as e:
                print(f"Application error: {e}")
                error = "Something went wrong. Please try again."

    return render_template(
        "index.html",
        weather=weather,
        explanation=explanation,
        error=error,
        city=city
    )


if __name__ == "__main__":
    app.run(debug=True)