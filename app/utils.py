from datetime import datetime

def convert_unix_time (timestamp = int) -> str:
    date_convert = datetime.fromtimestamp(timestamp).strftime("%I:%M:%p")

    if date_convert.startswith("0"):
        date_convert = date_convert[1:]
    
    return date_convert


