from m5stack_ui import *
from ALTwidgets import *
from ALTelements import *
from ALTconnection import *
from ALTweather import *
import uiflow
## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

## Creating an element which is displayed on the screen ##
title = Title(color=0x191970)
title.show_battery()
title.show_red_wifi()
title.set_text("My Title")
title.show_red_cloud()

## Creating a Board and Widgets on it ##
board = Board(51, 58, 5, 3, 5, True)
image_widget = board.draw_widget(2, 2, 0, 0, 0x0818A8)
weather_widget = board.draw_widget(2, 1, 0, 2, 0x4682B4)
checkBox_widget = board.draw_widget(1, 3, 2, 0, 0x191970)
picker_widget = board.draw_widget(2, 2, 0, 3, 0x0F52BA)
weather_widget2 = board.draw_widget(1, 2, 2, 3, 0x088F8F)

## Display elements on the widgets ##
image = Image(parent=image_widget, x=35, y=35, src='/flash/Assets/Icons/globe.png')
label = Label(parent=image_widget, x=3, y=3, text='My Globe', font=lv.font_montserrat_18, text_color=0xFFFFFF)
checkbox1 = Checkbox(parent=checkBox_widget, x=0, y=0, text='My CheckBox 1', text_color=0xFFFFFF, color=0x000000)
line = Line(parent=checkBox_widget, x=0, y=25, length=200, is_vertical=True, width=2, color=0x000000)
checkbox2 = Checkbox(parent=checkBox_widget, x=0, y=30, text='My CheckBox 2', text_color=0xFFFFFF, color=0x000000)
picker = Cpicker(parent=picker_widget, x=10, y=10, length=100)
temp_val = Label(parent=weather_widget2, x=4, y=5, text='00 C', font=lv.font_montserrat_14, text_color=0xFFFFFF)
temp_disc = Label(parent=weather_widget2, x=7, y=20, text='Cloudy', font=lv.font_montserrat_14, text_color=0xFFFFFF,
                  width=116, long_mode=lv.label.LONG.BREAK, alignment=lv.label.ALIGN.LEFT)
temp_pres = Label(parent=weather_widget2, x=7, y=35, text='1007.3 hPa', font=lv.font_montserrat_14, text_color=0xFFFFFF)
uv_text = Label(parent=weather_widget, x=5, y=5, text='UV', font=lv.font_montserrat_30)
uv_icon = Image(parent=weather_widget, x=15, y=50, src='/flash/Assets/Icons/uv.png')
uv_val = Label(parent=weather_widget, x=20, y=85, text='3', font=lv.font_montserrat_30)

wifi_SSD = "Lareine's iPhone"
wifi_pass = "2rffx73lukv8"

## Connecting to wifi ##
connect_wifi(wifi_SSD, wifi_pass)


def connect_wifi():
    isconn = wifiCfg.is_connected()
    if isconn:
        title.show_green_wifi()
    else:
        title.show_red_wifi()


'''
stopper = 0
while True:
    connect_wifi()
    if stopper == 0:
        print('Hello World')
    stopper = (stopper + 60) % 1800
    wait(60)
 '''


def refresh_minor():
    global time_date
    time_date = fetch_date_time()
    title.set_text(time_date)
    title.show_battery()
    connect_wifi()


def refresh_major():
    global weather_dict
    weather_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', 'C')
    print(weather_dict)
    temp_val.set_text(str(weather_dict['temperature']) + 'C')
    temp_disc.set_text(str(weather_dict['description']))
    temp_pres.set_text(str(weather_dict['pressure']) + ' hPa')
    #uv_val.set_text(str(weather_dict['uv-index']))
    uv_icon.set_src(str(weather_dict['icon-url']))
    uv_icon.set_pos(-22, -22)


stopper = 0  # Should add modulo 1800 (Refresh every half hour)
while True:
    print('Refresh Minor Underway')
    refresh_minor()
    if stopper == 0:
        print('Refresh Major Underway')
        refresh_major()
    stopper = (stopper + 60) % 1800
    wait(60)
