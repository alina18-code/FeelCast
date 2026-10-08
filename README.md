# FeelCast 🌦️

> **Don't just see the weather — feel the weather.**

FeelCast is a weather web application that turns live weather data into a more immersive experience. Instead of showing only numbers and forecasts, FeelCast adapts its visual atmosphere to the weather so each condition has its own feeling.

## ✨ Features

* 🌍 Search weather by city
* 🌡️ Temperature and feels-like temperature
* 💧 Humidity and visibility
* 🌧️ Rain information
* 💨 Wind speed and direction
* 🌅 Sunrise and sunset
* 📊 Hourly weather information
* 🔄 Interactive weather cards
* 🎨 Weather-based themes and atmospheric effects
* 🔊 Optional weather ambience
* 📱 Responsive and accessible interface
* ⚠️ Handles invalid locations and API/network errors

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **Requests**
* **OpenWeather API**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Jinja**
* **python-dotenv**

## 📁 Project Structure

```text
Weather website/
│
├── app/
│   ├── __init__.py          
│   ├── routes.py            # Flask routes and request handling
│   ├── weather.py           # Geocoding and weather API calls
│   └── utils.py             # Helper utilities (timestamps, condition-to-theme mapping)
│
├── static/
│   ├── css/
│   │   └── style.css        # Core layout and weather-specific theme styling
│   ├── js/
│   │   └── script.js        # Form validation and dynamic frontend interactions
│   └── images/
│       ├── sunny_theme_image.png
│       ├── cloudy_theme_image.png
│       ├── rain_theme_image.png
│       ├── snow_theme_image.png
│       ├── storm_theme_image.png
│       └── night_theme_image.png
│
├── templates/
│   └── index.html           # Main user interface template
│
├── .env                     # Local environment file for secret API keys (git-ignored)
├── .gitignore               # Prevents tracking of sensitive and temporary files
├── requirements.txt         # Project Python dependencies
└── README.md                # Project documentation
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd FeelCast
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the project root:

```env
WEATHER_API=your_api_key_here
```

### 5. Run the application

```bash
python app.py
```

Open the local Flask address shown in your terminal.

## 🎨 The Idea

FeelCast is built around one simple idea:

**Weather should be something you experience, not just something you read.**

Clear skies can feel warm and bright. Rain can feel refreshing and peaceful. Cloudy weather can feel calm and breezy, while snow can create a quiet winter atmosphere.

The interface keeps the weather information clear while allowing the atmosphere to change naturally with the conditions.

## 🔮 Future Improvements

* More detailed hourly graphs
* Location detection
* More weather atmospheres
* Improved animations and sound
* Automated testing
* Production deployment

---

**FeelCast — weather information with a little more feeling.**
