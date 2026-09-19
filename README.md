# AI Weather Assistant

A Flask-based web application that retrieves current weather
information and uses Groq AI to generate an easy-to-understand
weather explanation.

## Technologies

- Python
- Flask
- HTML5
- CSS3
- OpenWeatherMap API
- Groq API
- Requests
- python-dotenv

## Features

- Search weather by city
- Display current weather
- Display temperature
- Display humidity
- Display wind information
- Display pressure
- Display visibility
- Display cloud coverage
- Generate AI weather explanation
- Error handling
- Responsive design

## Installation

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a `.env` file:

WEATHER_API_KEY=your_openweathermap_api_key
GROQ_API_KEY=your_groq_api_key

Run the application:

python app.py

Open the application in your browser:

http://127.0.0.1:5000