from flask import Flask,request,jsonify
from flask_cors import CORS
import requests
from datetime import datetime,timezone
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
import os



app = Flask(__name__)

REQUEST_COUNT = Counter('weather_api_requests_total', 'Συνολικός αριθμός αιτημάτων στο /weather')
REQUEST_DURATION = Histogram('weather_api_response_duration_seconds', 'Χρονική διάρκεια απόκρισης αιτημάτων στο /weather')

CORS(app)   #access σε όλους τους clients


@app.route("/", methods=["GET"])
def home():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        return """
            <pre>
            ----------------------------------------------
             Welcome to the Weather Monitoring API 
            ----------------------------------------------
            Available Endpoints:
                 /weather  - Get real-time weather data
                 /metrics  - View Prometheus metrics
      
             Built with Flask, Prometheus, and Azure
            ----------------------------------------------
            </pre>
            """



@app.route("/weather", methods = ["GET"])
def weather():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        try:
            # Ανίχνευση latitude και longtitude χρήστη
            user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            if "," in user_ip:  # Αν υπάρχει πολλαπλή IP 
                user_ip = user_ip.split(",")[0]
            if ":" in user_ip:  # Αν υπάρχει PORT 
                user_ip = user_ip.split(":")[0]


            if user_ip == "127.0.0.1" or user_ip == "192.168.1.114":
                user_ip = "8.8.8.8"  # Google DNS , για δοκιμές στον localhost

            url = f'http://ip-api.com/json/{user_ip}'  

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                return jsonify({"error": "Failed to retrieve location data"}), 500

            if response.status_code == 200 :
                loc = (data.get("city", "Unknown"), data.get("country", "Unknown"))
                lat = data.get("lat", 0)
                lon = data.get("lon", 0)
            else:
                return jsonify({"error" : "Failed to retrieve location data"})

            # Αίτημα στο OpenWeatherAPI
            load_dotenv()
            api_key = os.getenv("OPENWEATHER_API_KEY")
            url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&appid={api_key}'

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                return jsonify({"error": "Failed to retrieve weather data"}), 500

            # Μετατροπή Unix time σε κανονική ώρα
            if data.get("alerts"):
                unix_time_start = data["alerts"][0].get("start")
                unix_time_end = data["alerts"][0].get("end")

                human_readable_start = datetime.fromtimestamp(unix_time_start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                human_readable_end = datetime.fromtimestamp(unix_time_end, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

                alerts_data = [
                    {
                        "event"      : data["alerts"][0].get("event", "Unknown"),
                        "description": data["alerts"][0].get("description", "No description"),
                        "start time" : human_readable_start,
                        "end time"   : human_readable_end
                    }
                ]
            else:
                alerts_data = []

            return jsonify({
                "location"   : loc,
                "latitude"   : lat,
                "longtitude" : lon,
                "temperature": data.get("current", {}).get("temp", "N/A"),
                "feels_like" : data.get("current", {}).get("feels_like", "N/A"),
                "humidity"   : data.get("current", {}).get("humidity", "N/A"),
                "wind speed" : data.get("current", {}).get("wind_speed", "N/A"),
                "weather"    : data.get("current", {}).get("weather", [{}])[0].get("description", "N/A"),
                "min_temp"   : data.get("daily", [{}])[0].get("temp", {}).get("min", "N/A"),
                "max_temp"   : data.get("daily", [{}])[0].get("temp", {}).get("max", "N/A"),
                "alerts"     : alerts_data
            })

        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500



@app.route("/metrics", methods = ["GET"])
def metrics():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        return generate_latest(),200,{'Content-Type':CONTENT_TYPE_LATEST}


if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=5000)


    






