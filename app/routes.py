from flask import Flask, render_template, request
from weather import get_geocoding_info, get_weather_info
from dotenv import load_dotenv
import os

load_dotenv ()

API_KEY = os.getenv("WEATHER_API")


app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    city = request.values.get("city")
    geocoding_results = get_geocoding_info(city, api_key= API_KEY)
    latitude = geocoding_results[0]["lat"]
    longitude = geocoding_results[0]["lon"]
    weather_json = get_weather_info(API_KEY,latitude, longitude,)
    #print(weather_json)
    temperature = weather_json["main"]["temp"]
    condition = weather_json["weather"][0]["description"]
    humidity = weather_json["main"]["humidity"]


    return render_template(
        "index.html",
        temperature = temperature,
        condition = condition,
        humidity = humidity
    )


if __name__ == "__main__":
    app.run(debug=True)