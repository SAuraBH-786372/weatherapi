from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

API_KEY = os.getenv('API_KEY')   # Replace with your actual API key
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
        # Return the weather data to be displayed on the results page
        return render_template('result.html', weather_info=weather_info)
    else:
        return jsonify({"error": "City not found or invalid API key"}), 404

# Route to display the result page with weather information
@app.route('/result', methods=['GET'])
def result():
    # Fetch city from the URL parameters
    city = request.args.get('city')
    if not city:
        return render_template('error.html', message="City is required")

    # Call the /weather API route to get weather data
    weather_info = get_weather_data(city)
    if weather_info.get("error"):
        return render_template('error.html', message=weather_info["error"])

    # Pass the weather data to the result page template
    return render_template('result.html', weather_info=weather_info)

def get_weather_data(city):
    """ Helper function to fetch weather data from OpenWeatherMap """
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return {"error": "City not found or invalid API key"}

# Run the app (This is for local testing only, when deploying you may not need this)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
