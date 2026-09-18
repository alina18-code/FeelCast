from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("WEATHER_API")

print(f"API key loaded finally: {api_key is not None}")