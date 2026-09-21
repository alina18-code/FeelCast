from dotenv import load_dotenv
import os
import requests
from utils import convert_unix_time, convert_meter_kilometre

load_dotenv()

api_key = os.getenv("WEATHER_API")

print(f"API key loaded finally: {api_key is not None} ")


def get_info (appid, lat, lon, unit="metric"):
    url ="https://api.openweathermap.org/data/2.5/weather"

    parameters ={
        "lat": lat,
        "lon": lon,
        "appid": appid,
        "units": unit,
    }

    try: 
        response = requests.get (url, parameters, timeout=5 )
        response.raise_for_status ()

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"https error occured {http_err}")
    except Exception as err:
        print(f"error occured {err}")



API_Key = api_key
latitude = 24.8607
longitude = 67.0104

weather_json = get_info(API_Key, latitude, longitude)

if weather_json:
    current_temp = weather_json["main"]["temp"]
    description = weather_json["weather"][0]["description"]

    feels_like = weather_json["main"]["feels_like"]
    humidity = weather_json["main"]["humidity"]

    sunrise = weather_json["sys"]["sunrise"]
    readable_sunrise = convert_unix_time(sunrise)

    sunset = weather_json["sys"]["sunset"]
    readable_sunset = convert_unix_time(sunset)

    wind_speed = weather_json["wind"]["speed"]
    wind_dir = weather_json["wind"]["deg"]

    visibility = weather_json["visibility"]
    update_visibility = convert_meter_kilometre(visibility)

    rain_data = weather_json.get('rain', {})
    rain = rain_data.get('1h', 0)


    print(f"Current Temperature: {current_temp}°C")
    print(f"Conditions: {description.title()}")
    print(f"Feels like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Sunries at: {readable_sunrise}")
    print(f"Sunset at: {readable_sunset}")
    print(f"Wind Speed: {wind_speed}m/s")
    print(f"Wind direction: {wind_dir} degrees")
    print(f"Visibility: {update_visibility} Km")
    print(f"Rain: {rain} mm/h")

    

    
