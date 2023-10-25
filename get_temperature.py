from geopy.geocoders import Nominatim
import requests
import json

YANDEX_TOKEN = '27557f08-f65e-457b-a1f8-428dadff9c63'

def get_coordinates(city):
    loc = Nominatim(user_agent = 'GetLoc')
    getLoc =  loc.geocode(city)
    return getLoc.latitude, getLoc.longitude

def get_json(city):
    latitude, longitude = get_coordinates(city)
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast/'
    params = {'lat':latitude, 
          'lon':longitude, 
          'lang': 'ru_RU', 
          'limit': 1, 
          'hours':'false'}
    req = requests.get(url_yandex, headers={'X-Yandex-API-Key': YANDEX_TOKEN}, params=params)
    yandex_json = json.loads(req.text)
    return yandex_json

def get_temperature(city):
    yandex_json = get_json(city)
    return yandex_json['fact']['feels_like']


def get_condition(city):
    yandex_json = get_json(city)
    return str(yandex_json['fact']['condition'])


def is_precipitation(city):
    if get_condition(city) not in ['clear', 'partly-cloudy', 
                                                'heavy-rain','cloudy', 'overcast']:
        return True
    return False