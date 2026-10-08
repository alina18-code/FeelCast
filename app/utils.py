from datetime import datetime

def convert_unix_time (timestamp = int) -> str:
    date_convert = datetime.fromtimestamp(timestamp).strftime("%I:%M:%p")

    if date_convert.startswith("0"):
        date_convert = date_convert[1:]
    
    return date_convert


def convert_meter_kilometre (meters = float) -> float:
    if meters is None:
        return 0.0

    kilometre = meters / 1000
    rounded_kilometre = round(kilometre, 1)

    if rounded_kilometre.is_integer():
        return str(int(rounded_kilometre))
        
    return str(rounded_kilometre)


def get_theme (condition_main):
    theme_map = {
        "Clear": "sunny",
        "Clouds": "cloudy",
        "Rain": "rain",
        "Drizzle": "rain",
        "Thunderstorm": "storm",
        "Snow": "snow",
    }
    return theme_map.get(condition_main, "cloudy")


def describe_humidity(humidity):
    if humidity < 30:
        return "The air is quite dry at the moment, which can make your skin and throat feel parched. Dry air also means sweat evaporates quickly, so heat can feel more intense than the thermometer suggests."

    elif humidity < 60:
        return "Humidity is at a comfortable, moderate level right now. This is generally the most pleasant range for the human body, with no extra dryness or stickiness in the air."

    elif humidity < 80:
        return "The air feels noticeably humid at this level. Sweat doesn't evaporate as easily, so temperatures can feel warmer than they actually are, especially during physical activity."

    else:
        return "Humidity is very high right now, making the air feel heavy and sticky. High humidity like this significantly increases how hot the weather actually feels."


def describe_visibility(visibility_km):
    if visibility_km >= 10:
        return "Visibility is excellent at the moment, with a clear view stretching for miles in every direction. Conditions like this are ideal for driving, flying, and outdoor activities."
    
    elif visibility_km >= 5:
        return "Visibility is good right now, allowing you to see distant landmarks clearly. Minor haze may be present, but it shouldn't meaningfully affect outdoor plans."
    
    elif visibility_km >= 1:
        return "Visibility is somewhat reduced at the moment, likely due to haze, mist, or light fog. It's worth taking extra care if you're driving or traveling long distances."
    
    else:
        return "Visibility is very poor right now, likely due to dense fog or heavy precipitation. Travel conditions may be hazardous, so extra caution is strongly recommended."


def describe_wind(wind_speed):
    if wind_speed < 2:
        return "The air is calm at the moment, with barely any breeze to speak of. Smoke would rise almost straight up, and leaves on trees should be completely still."
   
    elif wind_speed < 6:
        return "A gentle breeze is blowing right now, light enough to rustle leaves but not strong enough to cause any real disturbance outdoors. Comfortable conditions for most outdoor activities."
   
    elif wind_speed < 12:
        return "A moderate wind is picking up at the moment, strong enough to move small branches and raise dust on the ground. Loose objects outdoors may begin to shift."
   
    else:
        return "Strong winds are blowing right now, capable of swaying large branches and making walking noticeably more difficult. Caution is advised for outdoor activities and driving high-sided vehicles."


def describe_rain (rain_mm):
    if rain_mm == 0:
        return "There's no rainfall happening right now, so the ground should stay dry for the time being. Conditions are currently suitable for outdoor plans without rain gear."
    
    elif rain_mm < 2.5:
        return "Light rain is falling at the moment, enough to dampen surfaces but generally not disruptive. A light jacket or umbrella should be more than enough to stay comfortable."
    
    elif rain_mm < 7.6:
        return "Moderate rain is falling right now, enough to soak through light clothing fairly quickly. An umbrella or waterproof jacket is recommended if you're heading outside."
   
    else:
        return "Heavy rain is falling at the moment, which can reduce visibility and lead to localized flooding in low-lying areas. It's best to avoid unnecessary travel until conditions ease."


def describe_wind_direction(degrees):
    directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
    index = round(degrees / 45) % 8
    compass = directions[index]
    return f"The wind is currently blowing in from the {compass}, at a heading of roughly {degrees}°. Wind direction can hint at incoming weather changes, since many weather systems move in predictable patterns relative to their origin."


def describe_sunrise(readable_sunrise):
    return f"Sunrise today is at {readable_sunrise}, marking the moment the sun first climbs above the horizon. Mornings around sunrise often bring cooler temperatures and softer light, making it a popular time for a walk or a quiet start to the day."


def describe_sunset(readable_sunset):
    return f"Sunset today is at {readable_sunset}, marking the moment the sun dips below the horizon and daylight fades. Temperatures typically begin to cool noticeably afterward, and the sky often puts on its most colorful display in the minutes leading up to it."



