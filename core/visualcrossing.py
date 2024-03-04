# visualcrossing.py
import requests
from datetime import datetime, timedelta
import json
import os

class VisualCrossingWeatherAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    def get_timeline_data(self, location, start_date, end_date=None):
        url = f"{self.base_url}/{location}/{start_date}"
        if end_date:
            url += f"/{end_date}"
        url += f"?key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

def save_timeline_data_to_file(location, start_date, end_date):
    api_key = "922MWNKWR3G4MW2M7USGTL5JB" 
    visual_crossing_api = VisualCrossingWeatherAPI(api_key)

    timeline_data = visual_crossing_api.get_timeline_data(location, start_date, end_date)

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f"{location}_weather_output.json")
    with open(output_file_path, "w") as output_file:
        json.dump(timeline_data, output_file, indent=2)

    return output_file_path
