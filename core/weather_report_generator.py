import datetime
import math

class WeatherReportGenerator:
    def __init__(self, w_dataset):
        self.w_dataset = w_dataset

    def generate_report(self):
        try:
            temperatures = [w_data["main"]["temp"] for w_data in self.w_dataset["list"][1:8]]
            overall_avg_temp = round(sum(temperatures) / len(temperatures) - 273.0)

            daily_reports = []
            for i in range(1, 8):
                avg_temp = round((self.w_dataset["list"][i]["main"]["temp_min"] + self.w_dataset["list"][i]["main"]["temp_max"]) / 2 - 273.0)
                daily_reports.append({
                    "date": self.w_dataset['list'][i]["dt_txt"],
                    "avg_temp": avg_temp,
                    "icon": self.w_dataset["list"][i]["weather"][0]["icon"],
                })

            return {
                "overall_avg_temp": overall_avg_temp,
                "daily_reports": daily_reports,
                "city_name": self.w_dataset["city"]["name"],
                "city_country": self.w_dataset["city"]["country"],
                "wind": self.w_dataset['list'][0]['wind']['speed'],
                "degree": self.w_dataset['list'][0]['wind']['deg'],
                "status": self.w_dataset['list'][0]['weather'][0]['description'],
                "cloud": self.w_dataset['list'][0]['clouds']['all'],
                'date': self.w_dataset['list'][0]["dt_txt"],
                "pressure": self.w_dataset["list"][0]["main"]["pressure"],
                "humidity": self.w_dataset["list"][0]["main"]["humidity"],
                "sea_level": self.w_dataset["list"][0]["main"]["sea_level"],
                "weather": self.w_dataset["list"][1]["weather"][0]["main"],
                "description": self.w_dataset["list"][1]["weather"][0]["description"],
                "icon": self.w_dataset["list"][0]["weather"][0]["icon"],
            }
        except Exception as e:
            print(f"Error generating weather report: {e}")
            return None

def check_weather_conditions(w_dataset):
    extreme_conditions = {
        'heatwave': {'active': False, 'date': None},
        'flood': {'active': False, 'date': None},
        'cyclone': {'active': False, 'date': None},
        'drought': {'active': False, 'date': None},
    }

    for day in w_dataset["list"][:7]:
        temperature = day["main"]["temp"]
        description = day["weather"][0]["description"]
        rainfall = day.get("rain", {}).get("3h", 0)

        # Check for specific weather conditions
        if temperature > 35:
            extreme_conditions['heatwave']['active'] = True
            extreme_conditions['heatwave']['date'] = day["dt"]

        if rainfall > 50:
            extreme_conditions['flood']['active'] = True
            extreme_conditions['flood']['date'] = day["dt"]

        if "wind" in description.lower() and day["wind"]["speed"] > 1:  # Adjust the wind speed threshold
            extreme_conditions['cyclone']['active'] = True
            extreme_conditions['cyclone']['date'] = day["dt"]

        if rainfall < 2:
            extreme_conditions['drought']['active'] = True
            extreme_conditions['drought']['date'] = day["dt"]

    return extreme_conditions
