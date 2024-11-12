from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
 
app = Flask(__name__)
 
# Enable CORS for all routes
CORS(app)
 
API_KEY = os.getenv('API_KEY')   # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
 
# Serve the index.html page from the 'templates' directory
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')  # Get the city from query parameters
    if not city:
        return jsonify({"error": "City is required"}), 400
 
    # Construct the API URL for OpenWeatherMap
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"  # 'units=metric' gives temperature in Celsius
 
    # Make the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract relevant information
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "City not found or invalid API key"}), 404
if __name__ == '__main__':
    app.run(debug=True)
 
    