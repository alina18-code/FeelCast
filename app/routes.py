from flask import Flask, render_template, request, jsonify
from weather import get_geocoding_info, get_weather_info
import requests
from dotenv import load_dotenv
import os
from utils import convert_unix_time, convert_meter_kilometre, get_theme, describe_humidity, describe_rain, describe_sunrise, describe_sunset, describe_visibility, describe_wind, describe_wind_direction


load_dotenv ()

API_KEY = os.getenv("WEATHER_API")


app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/")
def index():
    return render_template("index.html", theme="sunny")


@app.route("/search", methods=["GET", "POST"])
def search():
    get_city = request.values.get("city")
    if not get_city or len(get_city.strip()) < 4 or not get_city.replace(" ", "").isalpha():
        return render_template("index.html", theme="sunny", error="Please enter a valid city name.")
    city = get_city

    if not API_KEY:
        return render_template(
            "index.html",
            theme="sunny",
            error="Weather API key is missing. Set WEATHER_API in your .env file and restart the server.",
        )

    try:
        geocoding_results = get_geocoding_info(get_city, api_key=API_KEY)
    except requests.RequestException as error:
        app.logger.warning("Weather geocoding request failed (%s).", type(error).__name__)
        return render_template(
            "index.html",
            theme="sunny",
            error="Could not contact the weather service. Please try again.",
        )

    if not geocoding_results:
        return render_template("index.html", theme="sunny", error="City not found. Please check the spelling and try again.")

    latitude = geocoding_results[0]["lat"]
    longitude = geocoding_results[0]["lon"]

    try:
        weather_json = get_weather_info(API_KEY, latitude, longitude)
    except requests.RequestException as error:
        app.logger.warning("Weather data request failed (%s).", type(error).__name__)
        return render_template(
            "index.html",
            theme="sunny",
            error="Could not load weather data. Please try again.",
        )

    temperature = weather_json["main"]["temp"]
    condition = weather_json["weather"][0]["description"]

    condition_main = weather_json["weather"][0]["main"]
    theme = get_theme(condition_main)

    humidity = weather_json["main"]["humidity"]
    feels_like = weather_json["main"]["feels_like"]
    
    sunrise = weather_json["sys"]["sunrise"]
    readable_sunrise = convert_unix_time(sunrise)

    sunset = weather_json["sys"]["sunset"]
    readable_sunset = convert_unix_time(sunset)

    current_time = weather_json["dt"]
    is_night = current_time < sunrise or current_time > sunset

    if is_night and condition_main in ["Clear", "Clouds"]:
        theme = "night"

    wind_speed = weather_json["wind"]["speed"]
    wind_dir = weather_json["wind"]["deg"]

    visibility = weather_json["visibility"]
    update_visibility = convert_meter_kilometre(visibility)

    rain_data = weather_json.get("rain", {})
    rain = rain_data.get("1h", 0)

    humidity_desc = describe_humidity(humidity)
    visibility_desc = describe_visibility(float(update_visibility))
    wind_desc = describe_wind(wind_speed)
    rain_desc = describe_rain(rain)
    wind_dir_desc = describe_wind_direction(wind_dir)
    sunrise_desc = describe_sunrise(readable_sunrise)
    sunset_desc = describe_sunset(readable_sunset)


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
        theme = theme,
        humidity_desc = humidity_desc,
        visibility_desc = visibility_desc,
        wind_desc = wind_desc,
        rain_desc = rain_desc,
        wind_dir_desc = wind_dir_desc,
        sunrise_desc = sunrise_desc,
        sunset_desc = sunset_desc,
    )

@app.route("/autocomplete")
def autocomplete():
        query = request.args.get("q", "")

        if len(query.strip()) < 2:
            return jsonify([])

        results = get_geocoding_info(query, api_key=API_KEY, limit=5)

        if not results:
            return jsonify([])

        suggestions = []
        for place in results:
            name = place.get("name")
            country = place.get("country")
            state = place.get("state")

            if state:
                label = f"{name}, {state}, {country}"
            else:
                label = f"{name}, {country}"

            suggestions.append({"name": name, "label": label})

        return jsonify(suggestions)


if __name__ == "__main__":
    app.run(debug=True)
    