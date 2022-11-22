from m5stack import *
from m5stack_ui import *
from uiflow import *

################# TIME #######################

# Fetches the exact time from host: cn.pool.ntp.org
def fetch_time(timezone = 3):
    rtc.settime('ntp', host='cn.pool.ntp.org', tzone=3)
    time_info = rtc.datetime()
    return str(time_info[4]) + str(":") + str(time_info[5])

import urequests
import ujson

################# WEATHER #######################

# returns current public IP
def _get_curr_ip():
    ip = urequests.get('https://api.ipify.org').content.decode('utf8')
    return ip

# returns a list that contains : ['lat', 'long']
def _get_lat_long_from_curr_ip():
    ip = _get_curr_ip()
    latlong = urequests.get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
    return latlong

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
def _get_weather_json_online(apikey, units):
    units_string = _parse_units(units)
    if units_string is None:
        raise Exception('Units must either be : K, F, C')
    latlong = _get_lat_long_from_curr_ip()
    req = urequests.get('https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&cnt=1'
                        .format(latlong[0], latlong[1], apikey)).text
    json_data = ujson.loads((req))
    return json_data

# Returns a dictionary that contains:
# [city, date, pressure (hPa units), temperature, humidity (%), wind speed (if imperial: miles/hour else meter/second), discription, icon-id] 
def fetch_local_weather_online(apikey, units):
    json_data = _get_weather_json_online(apikey, units)
    return {'city' : json_data["city"]["name"], 'date' : json_data["list"][0]["dt_txt"],
            'pressure' : json_data["list"][0]["main"]["pressure"], 'temperature' : json_data["list"][0]["main"]["temp"],
            'humidity' : json_data["list"][0]["main"]["humidity"], 'wind' : json_data["list"][0]["wind"]["speed"],
            'description' : json_data["list"][0]["weather"][0]["description"], 'icon-id' : json_data["list"][0]["weather"][0]["icon"]}

# returns : https://openweathermap.org/img/wn/{id}@2x.png
def fetch_icon_url_from_id(icon_id):
    return 'https://openweathermap.org/img/wn/{}@2x.png'.format(icon_id)
    
    