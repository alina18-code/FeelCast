from dotenv import load_dotenv
import os
import requests

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
latitude = 33.4
longitude = -94.04

weather_json = get_info(API_Key, latitude, longitude)

if weather_json:
    current_temp = weather_json["main"]["temp"]
    description = weather_json["weather"][0]["description"]
    feels_like = weather_json["main"]["feels_like"]
    humidity = weather_json["main"]["humidity"]
    sunrise = weather_json["sys"]["sunrise"]
    sunset = weather_json["sys"]["sunset"]
    wind_speed = weather_json["wind"]["speed"]
    wind_dir = weather_json["wind"]["deg"]
    
    print(f"Current Temperature: {current_temp}°C")
    print(f"Conditions: {description.title()}")
    print(f"Feels like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Sunries at: {sunrise}")
    print(f"Sunset at: {sunset}")
    print(f"Wind Speed: {wind_speed}m/s")
    print(f"Wind direction: {wind_dir} degrees")


    

    
