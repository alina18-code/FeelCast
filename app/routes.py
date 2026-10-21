
from flask import Flask, render_template, request, jsonify
from app.weather import get_geocoding_info, get_weather_info, get_forecast_weather
import requests
from dotenv import load_dotenv
import os
from app.utils import convert_unix_time, convert_meter_kilometre, get_theme, describe_humidity, describe_rain, describe_sunrise, describe_sunset, describe_visibility, describe_wind, describe_wind_direction, get_daily_forecast
from datetime import datetime

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

    

    forecast_json = get_forecast_weather(latitude, longitude, api_key=API_KEY)
    daily_forecast = get_daily_forecast(forecast_json["list"])

    hourly_forecast = []
    for entry in forecast_json["list"][:8]:
        time_label = datetime.fromtimestamp(entry["dt"]).strftime("%I %p").lstrip("0")
        temp_kelvin = entry["main"]["temp"]
        temp_celsius = round(temp_kelvin - 273.15) if temp_kelvin > 100 else round(temp_kelvin)
        entry_hour = datetime.fromtimestamp(entry["dt"]).hour
        icon = "🌙" if entry_hour < 6 or entry_hour >= 19 else "☀️"

        hourly_forecast.append({"time": time_label, "temp": temp_celsius, "icon": icon})


    temps = [hour["temp"] for hour in hourly_forecast]
    graph_axis_min = (min(temps) // 5 - 1) * 5
    graph_axis_max = (max(temps) // 5 + 1) * 5
    graph_plot_left = 82
    graph_plot_right = 670
    graph_plot_top = 34
    graph_plot_bottom = 145
    graph_axis_range = graph_axis_max - graph_axis_min

    graph_points = []
    for i, hour in enumerate(hourly_forecast):
        x = round(
            graph_plot_left
            + i * (graph_plot_right - graph_plot_left) / (len(hourly_forecast) - 1)
        )
        y = round(
            graph_plot_bottom
            - (hour["temp"] - graph_axis_min)
            / graph_axis_range
            * (graph_plot_bottom - graph_plot_top)
        )
        graph_points.append({"x": x, "y": y})

    graph_axis_ticks = [
        {
            "value": temperature,
            "y": round(
                graph_plot_bottom
                - (temperature - graph_axis_min)
                / graph_axis_range
                * (graph_plot_bottom - graph_plot_top)
            ),
        }
        for temperature in range(graph_axis_min, graph_axis_max + 1, 5)
    ]

    polyline_points = " ".join([f"{p['x']},{p['y']}" for p in graph_points])

    


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
        hourly_forecast = hourly_forecast, 
        graph_points = graph_points,
        graph_axis_ticks = graph_axis_ticks,
        graph_plot_left = graph_plot_left,
        graph_plot_right = graph_plot_right,
        polyline_points = polyline_points,
        daily_forecast = daily_forecast,
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    