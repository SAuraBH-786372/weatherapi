from flask import Flask, request, jsonify
import requests  # or your method to fetch weather data

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')  # Get the city from query parameters
    
    if not city:
        return jsonify({"error": "City is required"}), 400  # Return error if no city is provided
    
    # Here you should call your weather API (like OpenWeather or whatever service you use)
    # Example of a mock API response for now (you should replace this with actual API call):
    weather_data = {
        "city": city,
        "temperature": "20°C",  # Placeholder for actual data
        "description": "Clear Sky",  # Placeholder for actual data
        "humidity": "60%",  # Placeholder for actual data
        "wind_speed": "10 km/h"  # Placeholder for actual data
    }

    # If the weather data is fetched successfully, return it as JSON
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
