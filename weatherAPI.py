from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Store your OpenWeather API key here or use an environment variable
API_KEY = os.getenv('API_KEY', 'your_openweather_api_key')  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Route to serve the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the About page (about.html)
@app.route('/about')
def about():
    return render_template('about.html')

# Weather API route (this will be used by the frontend to fetch weather data)
@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')  # Get the city from query parameters
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Construct the API URL for OpenWeatherMap
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"  # 'units=metric' gives temperature in Celsius

    # Make the API request to OpenWeatherMap
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response from OpenWeatherMap
        # Extract relevant information
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        # Render the result page with the weather info
        return render_template('result.html', weather_info=weather_info)
    else:
        return jsonify({"error": "City not found or invalid API key"}), 404

# Run the app (This is for local testing only, when deploying you may not need this)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
