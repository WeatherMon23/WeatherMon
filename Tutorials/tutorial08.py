'''
Tutorial 8 example -- Fetching data from internet
'''
from ALTconnection import *
from ALTweather import *
from ALTwidgets import *
from ALTelements import *
from m5stack import *
import time

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

#Labels to display weather and time information
time_date = '01 Jan 00:00'
time_date = Label(x=100, y=10, text=time_date, font=lv.font_montserrat_18, text_color=0x000000)
temperature_val = Label(x=100, y=40, text='00 C', font=lv.font_montserrat_18, text_color=0x000000)
temperature_disc = Label(x=100, y=70, text='None', font=lv.font_montserrat_18, text_color=0x000000,
                  width=116, long_mode=lv.label.LONG.BREAK, alignment=lv.label.ALIGN.LEFT)
temperature_pres = Label(x=100, y=100, text='00 hPa', font=lv.font_montserrat_18, text_color=0x000000)
uv_text = Label(x=100, y=130, text='UV', font=lv.font_montserrat_18)
uv_icon = Image(x=100, y=160, src='/flash/Assets/Icons/uv.png')



def refresh_minor():
    global time_date, wifi_SSD, wifi_pass
    connect_wifi("TH", "thomas1234")
    time_date = fetch_date_time()
    

def refresh_major():
    global weather_dict
    weather_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', 'C')
    print(weather_dict)
    temperature_val.set_text(str(weather_dict['temperature']) + 'C')
    temperature_disc.set_text(str(weather_dict['description']))
    temperature_pres.set_text(str(weather_dict['pressure']) + ' hPa')
    uv_icon.set_src(str(weather_dict['icon-url']))
    uv_icon.set_pos(80, 140)


stopper = 0  # Should add modulo 1800 (Refresh every half hour)
while True:
    print('Refresh Minor Underway')
    refresh_minor()
    if stopper == 0:
        print('Refresh Major Underway')
        refresh_major()
    stopper = (stopper + 60) % 1800
    time.sleep(10)