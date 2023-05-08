import requests
import datetime

api_key = "8125ac9dc7fd2dcf2a828c333bbb931e"
city_name = "Москва"
url_current_weather = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ru"
url_weekly_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric&lang=ru"

def get_weather_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка запроса")
        return None

def print_current_weather(data):
    if data:
        wind_speed = data["wind"]["speed"]
        visibility = data["visibility"] / 1000
        print(f"Текущая погода в {city_name}:")
        print(f"Скорость ветра: {wind_speed} м/с")
        print(f"Видимость: {visibility} км")

def print_weekly_forecast(data):
    if data:
        print(f"Недельный прогноз погоды в {city_name}:")
        for item in data["list"]:
            date = datetime.datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M:%S")
            wind_speed = item["wind"]["speed"]
            visibility = item["visibility"] / 1000
            print(f"{date}:")
            print(f"  Скорость ветра: {wind_speed} м/с")
            print(f"  Видимость: {visibility} км")

current_weather_data = get_weather_data(url_current_weather)
print_current_weather(current_weather_data)

weekly_forecast_data = get_weather_data(url_weekly_forecast)
print_weekly_forecast(weekly_forecast_data)
