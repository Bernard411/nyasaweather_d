import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class WeatherAnalyzer:
    def __init__(self, api_key, country='MW'):
        self.api_key = api_key
        self.country = country

    def get_weather_data(self, city, days=7):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': f'{city},{self.country}',
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['cod'] != '200':
                logging.error(f"Error: {data['message']}")
                return None

            forecasts = data['list']

            weather_data = []
            for forecast in forecasts:
                timestamp = forecast['dt']
                date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                temperature = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                rain = forecast['rain']['3h'] if 'rain' in forecast else 0
                wind_speed = forecast['wind']['speed']
                weather_data.append({'date': date, 'temperature': temperature, 'description': description,
                                    'rain': rain, 'wind_speed': wind_speed})

            return weather_data[:days]

        except requests.exceptions.RequestException as e:
            logging.error(f"Error making API request: {e}")
            return None

    def detect_natural_disaster(self, weather_data, consecutive_days_threshold=3):
        potential_disasters = []
        consecutive_days = 0

        for i in range(len(weather_data) - consecutive_days_threshold + 1):
            # Calculate the average weather conditions for the next consecutive_days_threshold days
            average_data = self.calculate_average_weather(weather_data[i:i + consecutive_days_threshold])

            # Detect potential disasters based on average conditions
            if average_data['rain'] > 10:
                potential_disasters.append(("Flood", average_data))
                consecutive_days += 1
            else:
                consecutive_days = 0

            if average_data['temperature'] > 35:
                potential_disasters.append(("Heatwave", average_data))
                consecutive_days += 1
            else:
                consecutive_days = 0

            if average_data['temperature'] > 30 and average_data['rain'] < 2:
                potential_disasters.append(("Drought", average_data))
                consecutive_days += 1
            else:
                consecutive_days = 0

            if average_data['rain'] > 5 and average_data['wind_speed'] > 20:
                potential_disasters.append(("Cyclone", average_data))
                consecutive_days += 1
            else:
                consecutive_days = 0

            if consecutive_days >= consecutive_days_threshold:
                break

        return potential_disasters

    def calculate_average_weather(self, weather_data):
        total_temperature = sum(data['temperature'] for data in weather_data)
        total_rain = sum(data['rain'] for data in weather_data)
        total_wind_speed = sum(data['wind_speed'] for data in weather_data)

        average_data = {
            'temperature': total_temperature / len(weather_data),
            'rain': total_rain / len(weather_data),
            'wind_speed': total_wind_speed / len(weather_data)
        }

        return average_data

    def run_analysis(self):
        city = input('YOUR_CITY: ')
        weather_data = self.get_weather_data(city, days=14)

        if weather_data:
            for data in weather_data:
                self.log_weather_data(data)

            potential_disasters = self.detect_natural_disaster(weather_data)

            if potential_disasters:
                for disaster_type, disaster_data in potential_disasters:
                    self.log_disaster_warning(disaster_type, disaster_data)
            else:
                logging.info("No potential natural disasters detected.")

    def log_weather_data(self, data):
        logging.info(
            f"Date: {data['date']}, Temperature: {data['temperature']}°C, "
            f"Description: {data['description']}, Rain: {data['rain']}mm, Wind Speed: {data['wind_speed']}m/s"
        )

    def log_disaster_warning(self, disaster_type, disaster_data):
        logging.warning(f"Warning: Potential {disaster_type} detected!")
        logging.warning(f"Average Temperature: {disaster_data['temperature']}°C")
        logging.warning(f"Average Rain: {disaster_data['rain']}mm")
        logging.warning(f"Average Wind Speed: {disaster_data['wind_speed']}m/s")

def main():
    api_key = 'a3388151eeeda8d97b14fbeaf70bad25'
    weather_analyzer = WeatherAnalyzer(api_key)
    weather_analyzer.run_analysis()

if __name__ == "__main__":
    main()
