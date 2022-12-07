from m5stack import *
from m5stack_ui import *
from uiflow import *
from Connection import *

################# TIME #######################

def _get_month(month):
    dictionary = {1 : 'Jan', 2 : 'Feb', 3 : 'Mar', 4:'Apr', 5:'May', 6:'Jun',
                  7 : 'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12: 'Dec'}
    return dictionary.get(month, None)

def _add_left_zero(str):
    if len(str) == 1:
        return '0' + str
    else:
        return str

# Fetches the exact time from host: cn.pool.ntp.org
def fetch_time(timezone = 3, host = 'cn.pool.ntp.org'):
    check_connection()
    rtc.settime('ntp', host=host, tzone=3)
    time_info = rtc.datetime()
    return str(time_info[4]) + str(":") + str(time_info[5])

def fetch_date_time(timezone = 3, host = 'cn.pool.ntp.org'):
    rtc.settime('ntp', host=host, tzone=3)
    time_info = rtc.datetime()
    res = _add_left_zero(str(time_info[2])) + str(' ') + _get_month(time_info[1]) + str(' ') + _add_left_zero(str(time_info[4])) + str(":") + _add_left_zero(str(time_info[5]))
    return res

import urequests
import ujson

################# WEATHER FROM API #######################
# Fetches weather from: https://openweathermap.org

# returns current public IP
def _get_curr_ip():
    ip = urequests.get('https://api.ipify.org').content.decode('utf8')
    return ip

# returns a list that contains : ['lat', 'long']
def _get_lat_long_from_curr_ip():
    ip = _get_curr_ip()
    latlong = urequests.get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
    return latlong

def _get_city_from_curr_ip():
    ip = _get_curr_ip()
    city = urequests.get('https://ipapi.co/{}/city/'.format(ip)).text
    return city

# In the site we fetch the weather from, the dictionary is:
# 'standard' = 'Kelvin'
# 'imperial' = 'Fahrenheit'
# 'metric' = 'Celsius'
# Params: units is either {K, C, F}
# Return: the appropriate string to be used in the site 
def _parse_units(units):
    dictionary = {'K' : 'standard', 'C' : 'metric', 'F' : 'imperial'}
    return dictionary.get(units, None)
    
    

# returns all weather info as json
def _get_weather_json_from_api(apikey, units_string):
    check_connection()
    latlong = _get_lat_long_from_curr_ip()
    req = urequests.get('https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&cnt=1'
                        .format(latlong[0], latlong[1], apikey)).text
    json_data = ujson.loads((req))
    return json_data

# returns : https://openweathermap.org/img/wn/{id}@2x.png
def _fetch_icon_url_from_id(icon_id):
    return 'https://openweathermap.org/img/wn/{}@2x.png'.format(icon_id)

# Returns a dictionary that contains:
# [city, date, pressure (hPa units), temperature, humidity (%), wind speed (if imperial: miles/hour else meter/second), discription, icon-id] 
def fetch_local_weather_from_api(apikey, units):
    units_string = _parse_units(units)
    if units_string is None:
        raise Exception(__name__ + ': Units must either be : K, F, C')
    try:
        json_data = _get_weather_json_from_api(apikey, units)
    except Exception as e:
        return {'city' : 'N/A', 'date' : 'N/A', 'pressure' : 'N/A', 'temperature' : 'N/A',
            'humidity' : 'N/A', 'wind' : 'N/A', 'description' : 'N/A', 'icon-url' : 'res/error.png',
            'uv-index' : 'N/A', 'error-msg' : str(e)}
    return {'city' : json_data["city"]["name"], 'date' : json_data["list"][0]["dt_txt"],
            'pressure' : json_data["list"][0]["main"]["pressure"], 'temperature' : json_data["list"][0]["main"]["temp"],
            'humidity' : json_data["list"][0]["main"]["humidity"], 'wind' : json_data["list"][0]["wind"]["speed"],
            'description' : json_data["list"][0]["weather"][0]["description"], 'icon-url' : _fetch_icon_url_from_id(json_data["list"][0]["weather"][0]["icon"]),
            'uv-index' : 'N/A', 'error-msg' : ''}



################# WEATHER FROM wttr.in #######################
# Fetches the weather from : https://wttr.in/{city}

# If the city contains spaces e.g. Ramat Gan, then the parameter should contain + instead of space,
# e.g. Ramat+Gan
def _get_weather_json_from_web(city):
    check_connection()
    req_text = urequests.get("https://wttr.in/{}?format=j2".format(city)).text
    try:
        json_data = ujson.loads((req_text))
    except Exception as e:
        raise Exception(__name__ + ": https://wttr.in is currently down, can't fetch weather data.")
    return json_data

def _get_temp_id(units):
    dictionary = {'C' : 'temp_C', 'F' : 'temp_F'}
    return dictionary.get(units, None)

# TODO: Implement this function, need to check all possible descriptions and maybe create a dictionary!
def _fetch_icon_url_from_desc(desc):
    return None

# TODO: Function is too slow, because json is too big.. try and make it faster!
# Returns a dictionary that contains:
# [city, date, pressure (hPa units), temperature, humidity (%), wind speed (meter/second), description, icon-id] 
def fetch_local_weather_from_web(units):
    temp_id = _get_temp_id(units)
    if temp_id is None:
        raise Exception(__name__ + ': Units must either be : F, C')
    city = _get_city_from_curr_ip()
    city_m = city.replace(' ', '+')
    try:
        json_data = _get_weather_json_from_web(city_m)
    except Exception as e:
        return {'city' : 'N/A', 'date' : 'N/A', 'pressure' : 'N/A', 'temperature' : 'N/A',
            'humidity' : 'N/A', 'wind' : 'N/A', 'description' : 'N/A', 'icon-url' : 'res/error.png',
            'uv-index' : 'N/A', 'error-msg' : str(e)}
    weather = json_data['weather'][0]
    json_data = json_data['current_condition'][0]
    return {'city' : city, 'date' : json_data["localObsDateTime"],
            'pressure' : json_data["pressure"], 'temperature' : str(json_data[temp_id]),
            'humidity' : str(json_data["humidity"]), 'wind' : str(round(float(json_data["windspeedKmph"])*0.277778, 2)),
            'description' : json_data["weatherDesc"][0]["value"], 'icon-url' : _fetch_icon_url_from_desc(json_data["weatherIconUrl"][0]["value"]),
            'uv-index' : weather["uvIndex"], 'error-msg' : ''}
    
