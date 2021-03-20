import math
import requests
from django.shortcuts import render
from django.http import HttpResponse

from .forms import CityForm
from .models import City


# Create your views here.
# Default/Global Variable


def home_index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=89d4874741c802437c20ea38addbc758"
    if request.method =='POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()  # return all cities from databases
    weather_data = []
    for city in cities:
        city_weather = requests.get(
            url.format(city)).json()  # request the API data and convert the JSON to Python data types

        weather = {
            'city': city,
            'temperature': celsiusCal(city_weather['main']['temp']),
            'temp_min': celsiusCal(city_weather['main']['temp_min']),
            'temp_feels_like': celsiusCal(city_weather['main']['feels_like']),
            'temp_max': celsiusCal(city_weather['main']['temp_max']),
            'description': city_weather['weather'][0]['description'],
            'error': False
        }

        weather_data.append(weather)  # add the data for the current city into our list

    return render(request, 'home/index.html', context={'weather_data': weather_data, "form": form})
    # return HttpResponse("Hello, world. You're at the polls index.")


def celsiusCal(temp):
    return math.floor((temp - 32) * (5 / 9))
