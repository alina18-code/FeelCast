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

    



