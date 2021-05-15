import requests
from django.conf import settings
from django.http import JsonResponse
from .models import HourlyData

API_KEY = settings.API_KEY

# Collect Weather data based on the circuler lat long (12,32,15,37,10)
def collect_data(request):
    url = f'http://api.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&appid={API_KEY}'
    req = requests.get(url)
    data = req.json()
    data_list = data['list'][:10]
    for doc in data_list:
        lat = doc['coord']['Lat']
        long = doc['coord']['Lon']
        name = doc['name']
        hourly_data_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude=minutely,' \
                          f'daily&appid={API_KEY}'
        req = requests.get(hourly_data_url)
        hourly_data = req.json()
        hourly_data['name'] = name
        existing_data = HourlyData.objects.filter(lat=lat, lon=long)
        if existing_data:
            existing_data.update(**hourly_data)
        else:
            HourlyData.objects.create(**hourly_data)
    message = 'New data added and existing data updated successfully'
    res = {
        'message': message
    }
    return JsonResponse(res)


# Find the similarity of weather of two cities. (the approach I picked might not be the right one)
def get_similar_cities(request):
    data = HourlyData.objects.all().values('name', 'current')
    weather_percentage = []
    weather_list = []
    for element in list(data):
        city_name = element['name']
        current = element['current']
        addition = sum((current['temp'], current['feels_like'], current['pressure'], current['humidity']),
                       current['wind_deg'])
        weather_list.append((city_name, addition))
    weather_list.sort(key=lambda x: x[1], reverse=True)
    for index in range(len(weather_list) - 1):
        city1 = weather_list[index][1]
        city2 = weather_list[index + 1][1]
        print(city1, city2)
        percentage = (100 - abs(city1 - city2))
        weather_percentage.append((weather_list[index][0], weather_list[index + 1][0], round(percentage, 2)))
    weather_percentage.sort(key=lambda x: x[2], reverse=True)
    res = {
        'city1': weather_percentage[0][0],
        'city2': weather_percentage[0][1],
        'similarity_percentage': weather_percentage[0][2],
    }
    return JsonResponse(res)
