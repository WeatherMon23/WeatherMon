import lvgl as lv
import wifiCfg
from m5mqtt import M5mqtt
from m5stack_ui import *

from ALTweather import *
from ALTwidgets import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x000D54)

time_date = '01 Jan 00:00'
weather_dict = None
isconn = wifiCfg.is_connected()

t = ALTTitle(color=0x00093D)
t.show_battery()
if isconn:
    t.show_green_wifi()
else:
    t.show_red_wifi()

t.set_text(time_date)

b = Board(51, 58, 5, 3, 5, True)
w_temp = b.draw_widget(2, 2, 0, 0, 0x1DAD00)
w_icon = b.draw_widget(1, 1, 0, 2, 0x1DAD00)
w_remote = b.draw_widget(2, 2, 0, 3, 0x7400B7)
w_humid = b.draw_widget(1, 2, 2, 0, 0x6A0038)
w_uv = b.draw_widget(2, 1, 1, 2, 0xD0DE00)
w_wind = b.draw_widget(1, 2, 2, 3, 0x009FA6)

temp_val = ALTLabel(parent=w_temp, x=4, y=5, text='00 C', font=lv.font_montserrat_48, text_color=0xFFFFFF)
temp_disc = ALTLabel(parent=w_temp, x=7, y=55, text='Cloudy', font=lv.font_montserrat_18, text_color=0xFFFFFF,
                     width=116, long_mode=lv.label.LONG.BREAK, alignment=lv.label.ALIGN.LEFT)
temp_pres = ALTLabel(parent=w_temp, x=7, y=98, text='1007.3 hPa', font=lv.font_montserrat_18, text_color=0xFFFFFF)

icon_icon = ALTImage(parent=w_icon, x=3, y=3, src='/flash/icons/uv.png')

uv_text = ALTLabel(parent=w_uv, x=5, y=5, text='UV', font=lv.font_montserrat_30)
uv_icon = ALTImage(parent=w_uv, x=3, y=33, src='/flash/icons/uv.png')
uv_val = ALTLabel(parent=w_uv, x=20, y=85, text='3', font=lv.font_montserrat_30)

humid_val = ALTLabel(parent=w_humid, x=5, y=13, text='00%', font=lv.font_montserrat_30, text_color=0xFFFFFF)
humid_icon = ALTImage(parent=w_humid, x=82, y=17, src='/flash/icons/humidity.png')

remote_title = ALTLabel(parent=w_remote, x=10, y=5, text='Remote\nM5stack', font=lv.font_montserrat_22,
                        text_color=0xFFFFFF)
remote_disc = ALTLabel(parent=w_remote, x=6, y=72, text='Temp: 21C', font=lv.font_montserrat_18, text_color=0xFFFFFF)
remote_pres = ALTLabel(parent=w_remote, x=7, y=95, text='1007.3 hPa', font=lv.font_montserrat_18, text_color=0xFFFFFF)

wind_val = ALTLabel(parent=w_wind, x=5, y=13, text='00 m/s', font=lv.font_montserrat_26, text_color=0xFFFFFF)


def fetch_data(topic_data):
    data_list = topic_data.split(',')
    temp = str(round(float(data_list[0])))
    pressure = str(round(float(data_list[1]), 1))
    remote_disc.set_text('Temp: ' + temp + 'C')
    remote_pres.set_text(pressure + ' hPa')
    pass


connect_wifi("ICST", "arduino123")
m5mqtt = M5mqtt('subscriber', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_dpeD84qP5LNgUJh1ihzHwEE70UsG', 300)
m5mqtt.subscribe(str('WeatherMon/feeds/weathermonfeed'), fetch_data)
m5mqtt.start()


def refresh_minor():
    global time_date
    time_date = fetch_date_time()
    t.set_text(time_date)
    t.show_battery()
    isconn = wifiCfg.is_connected()
    if isconn:
        t.show_green_wifi()
    else:
        t.show_red_wifi()


def refresh_major():
    global weather_dict
    weather_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', 'C')
    print(weather_dict)
    temp_val.set_text(str(weather_dict['temperature']) + 'C')
    temp_disc.set_text(str(weather_dict['description']))
    temp_pres.set_text(str(weather_dict['pressure']) + ' hPa')
    humid_val.set_text(str(weather_dict['humidity']) + '%')
    # uv_val.set_text(str(weather_dict['uv-index']))
    wind_val.set_text(str(weather_dict['wind']) + 'm/s')
    icon_icon.set_src(str(weather_dict['icon-url']))
    icon_icon.set_pos(-22, -22)


stopper = 0  # Should add modulo 1800 (Refresh every half hour)
while True:
    print('Refresh Minor Underway')
    refresh_minor()
    if stopper == 0:
        print('Refresh Major Underway')
        refresh_major()
    stopper = (stopper + 60) % 1800
    wait(60)
