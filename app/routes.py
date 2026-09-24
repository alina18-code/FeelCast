from flask import Flask, render_template, request
from weather import get_geocoding_info, get_weather_info
from dotenv import load_dotenv
import os
from utils import convert_unix_time, convert_meter_kilometre

load_dotenv ()

API_KEY = os.getenv("WEATHER_API")


app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    get_city = request.values.get("city")
    city = get_city

    geocoding_results = get_geocoding_info(get_city, api_key= API_KEY)
    latitude = geocoding_results[0]["lat"]
    longitude = geocoding_results[0]["lon"]


    weather_json = get_weather_info(API_KEY,latitude, longitude,)

    temperature = weather_json["main"]["temp"]
    condition = weather_json["weather"][0]["description"]

    humidity = weather_json["main"]["humidity"]
    feels_like = weather_json["main"]["feels_like"]
    
    sunrise = weather_json["sys"]["sunrise"]
    readable_sunrise = convert_unix_time(sunrise)

    sunset = weather_json["sys"]["sunset"]
    readable_sunset = convert_unix_time(sunset)

    wind_speed = weather_json["wind"]["speed"]
    wind_dir = weather_json["wind"]["deg"]

    visibility = weather_json["visibility"]
    update_visibility = convert_meter_kilometre(visibility)

    rain_data = weather_json.get("rain", {})
    rain = rain_data.get("1h", 0)



    return render_template(
        "index.html",
        city = city,
        temperature = temperature,
        condition = condition,
        humidity = humidity,
        feels_like = feels_like,
        wind_speed = wind_speed,
        readable_sunrise = readable_sunrise,
        readable_sunset = readable_sunset,
        wind_dir = wind_dir,
        update_visibility = update_visibility,
        rain = rain,
    )


if __name__ == "__main__":
    app.run(debug=True)