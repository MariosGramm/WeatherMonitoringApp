from flask import Flask,request,jsonify
from flask_cors import CORS
import requests
from datetime import datetime,timezone
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)

REQUEST_COUNT = Counter('weather_api_requests_total', 'Συνολικός αριθμός αιτημάτων στο /weather')
REQUEST_DURATION = Histogram('weather_api_response_duration_seconds', 'Χρονική διάρκεια απόκρισης αιτημάτων στο /weather')

CORS(app)   #access σε όλους τους clients

@app.route("/", methods=["GET"])
def home():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        return "Welcome to the Weather Monitoring API "


@app.route("/weather", methods = ["GET"])
def weather():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        #Ανίχνευση latitude και longtitude χρήστη
        user_ip = request.headers.get("X-Forwarded-For",request.remote_addr)
        if user_ip == "127.0.0.1" or user_ip == "192.168.1.114":
            user_ip = "8.8.8.8"  # Google DNS , για δοκιμές στον localhost

        url = f'http://ip-api.com/json/{user_ip}'

        response = requests.get(url)

        data = response.json()

        if response.status_code == 200 :
            loc = data["city"],data["country"]
            lat = data["lat"]
            lon = data["lon"]
        else:
            return{"error : Failed to retrieve location data"}

        #Αίτημα στο OpenWeatherAPI
        api_key = "d3867d125924f8f826fa707057778f18"
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&appid={api_key}'
    

        response = requests.get(url)

        data = response.json()

        #Μετατροπή Unix time σε κανονική ώρα
        unix_time_start = data["alerts"][0]["start"]
        unix_time_end = data["alerts"][0]["end"]

        human_readable_start = datetime.fromtimestamp(unix_time_start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        human_readable_end = datetime.fromtimestamp(unix_time_end, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    

        return jsonify({
            "location"   :loc,
            "latitude"   :lat,
            "longtitude" :lon,
            "temperature":data["current"]["temp"],
            "feels_like" :data["current"]["feels_like"],
            "humidity"   :data["current"]["humidity"],
            "wind speed" :data["current"]["wind_speed"],
            "weather"    :data["current"]["weather"][0]["description"],
            "min_temp"   :data["daily"][0]["temp"]["min"],
            "max_temp"   :data["daily"][0]["temp"]["max"],
            "alerts"     :[
                {
                "event"      :data["alerts"][0]["event"],
                "description":data["alerts"][0]["description"],
                "start time" :human_readable_start,
                "end time"   :human_readable_end
                }
            ]

        })


@app.route("/metrics", methods = ["GET"])
def metrics():
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        return generate_latest(),200,{'Content-Type':CONTENT_TYPE_LATEST}


if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=5000)


    






