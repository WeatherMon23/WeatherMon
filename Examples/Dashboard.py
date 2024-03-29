import lvgl as lv
import wifiCfg as wcfg
from m5mqtt import M5mqtt
from m5stack_ui import *
from m5stack import *
from uiflow import *

from ALTweather import *
import ALTwidgets as altw
import ALTelements as alte
import ALTutils as altu
import ALTnotifications as altn

import ujson

# ---------------------- Globals ---------------------------#
LV_HOR_RES = 320
LV_VER_RES = 240

'''
    index 0: Original Theme
    index 1: Green Theme
    index 2: Light Theme
    index 3: Dark Theme
'''
DEFAULT_THEME = 0
global_themes = [{'dark': 0x003333, 'light': 0x006666, 'font': 0xFFFFFF},
                 {'dark': 0x115400, 'light': 0x1C8900, 'font': 0xFFFFFF},
                 {'dark': 0xD8D8D8, 'light': 0xFFFFFF, 'font': 0x000000},
                 {'dark': 0x000000, 'light': 0x2A2A2A, 'font': 0xFFFFFF}]

w_colors = {'temp': 0xB8860B, 'icon': 0xffe033, 'uv': 0xFFD700, 'humid': 0x00cccc, 'remote': 0xA52A2A, 'wind': 0x4169E1,
            'light_bg': 0x006666, 'dark_bg': 0x003333, 'font': 0xFFFFFF}

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(w_colors['light_bg'])

time_date = '01 Jan 00:00'
weather_dict = None
isconn = wcfg.is_connected()

units = 'C'
local_temp = 0
remote_temp = 0
local_pressure = 0
remote_pressure = 0
major_refresh_rate = 120

alert_flag = True

t = altw.Title(color=w_colors['dark_bg'])
t.show_battery()
if isconn:
    t.show_green_wifi()
else:
    t.show_red_wifi()
t.set_text(time_date)
# --------------------------------------------------------------- #
# ---------------------- Main Page ---------------------------#
b = altw.Board(51, 58, 5, 3, 5, False)
w_temp = b.draw_widget(2, 2, 0, 0, w_colors['temp'])
w_icon = b.draw_widget(1, 1, 0, 2, w_colors['icon'])
w_remote = b.draw_widget(2, 2, 0, 3, w_colors['remote'])
w_humid = b.draw_widget(1, 2, 2, 0, w_colors['humid'])
w_uv = b.draw_widget(2, 1, 1, 2, w_colors['uv'])
w_wind = b.draw_widget(1, 2, 2, 3, w_colors['wind'])

temp_val = alte.Label(parent=w_temp, x=4, y=5, text='N/A ' + units, font=lv.font_montserrat_38,
                      text_color=w_colors['font'])
temp_disc = alte.Label(parent=w_temp, x=7, y=55, text='N/A', font=lv.font_montserrat_18, text_color=w_colors['font'],
                       width=116, long_mode=lv.label.LONG.BREAK, alignment=lv.label.ALIGN.LEFT)
temp_pres = alte.Label(parent=w_temp, x=7, y=98, text='N/A hPa', font=lv.font_montserrat_18,
                       text_color=w_colors['font'])

icon_icon = alte.Image(parent=w_icon, x=3, y=3, src='/flash/Assets/Icons/error.png')

uv_text = alte.Label(parent=w_uv, x=7, y=5, text='UV', font=lv.font_montserrat_26)
uv_icon = alte.Image(parent=w_uv, x=7, y=40, src='/flash/Assets/Icons/uv.png')
uv_val = alte.Label(parent=w_uv, x=22, y=85, text='3', font=lv.font_montserrat_26)

humid_val = alte.Label(parent=w_humid, x=5, y=13, text='N/A%', font=lv.font_montserrat_30, text_color=w_colors['font'])
humid_icon = alte.Image(parent=w_humid, x=82, y=17, src='/flash/Assets/Icons/humidity.png')

remote_title = alte.Label(parent=w_remote, x=10, y=5, text='Remote\nM5Stack', font=lv.font_montserrat_22,
                          text_color=w_colors['font'])
remote_disc = alte.Label(parent=w_remote, x=6, y=72, text='Temp: N/A' + units, font=lv.font_montserrat_18,
                         text_color=w_colors['font'])
remote_pres = alte.Label(parent=w_remote, x=7, y=95, text='N/A hPa', font=lv.font_montserrat_18,
                         text_color=w_colors['font'])

wind_val = alte.Label(parent=w_wind, x=5, y=13, text='N/A m/s', font=lv.font_montserrat_26, text_color=w_colors['font'])
# --------------------------------------------------------------- #

# ---------------------- Settings Page ---------------------------#

s_theme_drop_option = 'Original'


def s_theme_drop_event(obj, event):
    global s_theme_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 15  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        s_theme_drop_option = str(option.strip())
        s_theme_drop_option = s_theme_drop_option[:len(s_theme_drop_option) - 1]
        print(s_theme_drop_option)


s_refresh_drop_option = '2 min'


def s_refresh_drop_event(obj, event):
    global s_refresh_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 15  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        s_refresh_drop_option = str(option.strip())
        s_refresh_drop_option = s_refresh_drop_option[:len(s_refresh_drop_option) - 1]
        print(s_refresh_drop_option)


theme_dict = {'Original': 0, 'Green': 1, 'Light': 2, 'Dark': 3}
rate_dict = {'2 min': 120, '5 min': 300, '10 min': 600, '20 min': 1200}


def manage_settings():
    global major_refresh_rate, s_refresh_drop_option, s_theme_drop_option, units, theme_dict, rate_dict
    units_old = units
    rate_old = major_refresh_rate
    major_refresh_rate = rate_dict[s_refresh_drop_option]
    refresh_colors(theme_dict[s_theme_drop_option])


def event_handler(source, evt):
    if evt == lv.EVENT.CLICKED:
        manage_settings()
        btnA_pressed()
        print('Settings have been saved!')


def switch_handler(source, evt):
    global s_bright, s_refresh_drop
    if evt == lv.EVENT.CLICKED:
        if source.get_state():
            s_bright.set_value(3)
            s_refresh_drop.set_selected(0)
        else:
            s_bright.set_value(100)
            s_refresh_drop.set_selected(0)


s_cont = alte.Page(x=0, y=t.get_height(), height=LV_VER_RES - t.get_height(), width=LV_HOR_RES,
                   color=w_colors['light_bg'], radius=0)
s_cont.set_hidden(True)
s_title = alte.Label(parent=s_cont, x=5, y=5, text=lv.SYMBOL.SETTINGS + ' Settings', font=lv.font_montserrat_30,
                     text_color=w_colors['font'])
s_theme_label = alte.Label(parent=s_cont, x=5, y=50, text='Theme: ', font=lv.font_montserrat_22,
                           text_color=w_colors['font'])
s_theme_drop = alte.Dropdown(parent=s_cont, x=95, y=45, options=['Original', 'Green', 'Light', 'Dark'],
                             color=w_colors['dark_bg'])
s_refresh_label = alte.Label(parent=s_cont, x=5, y=90, text='Major refresh rate: ', font=lv.font_montserrat_22,
                             text_color=w_colors['font'])
s_refresh_drop = alte.Dropdown(parent=s_cont, x=220, y=85, width=80, options=['2 min', '5 min', '10 min', '20 min'],
                               color=w_colors['dark_bg'])
s_bright_label = alte.Label(parent=s_cont, x=5, y=130, text='Brightness: ', font=lv.font_montserrat_22,
                            text_color=w_colors['font'])
s_bright = altw.BrightnessSlider(parent=s_cont, x=150, y=150, width=150, color=w_colors['font'], show_label=False)
s_power_save_label = alte.Label(parent=s_cont, x=5, y=170, text='Power Save Mode: ', font=lv.font_montserrat_22,
                                text_color=global_themes[0]['font'])
s_power_save_switch = alte.Switch(parent=s_cont, x=215, y=165, color=global_themes[0]['dark'])
s_power_save_switch.set_event_cb(switch_handler)
s_save = alte.Button(parent=s_cont, x=110, y=210, text='Save', color=w_colors['dark_bg'], height=35, width=100,
                     font=lv.font_montserrat_22)

s_theme_drop.set_event_cb(s_theme_drop_event)
s_refresh_drop.set_event_cb(s_refresh_drop_event)
# s_units_switch.set_event_cb(s_units_switch_event)
s_save.set_event_cb(event_handler)

# --------------------------------------------------------------- #

# ---------------------- Gauges Page ---------------------------#
g_drop_option = 'Local Temp'


def g_gauge_drop_event(obj, event):
    global g_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 20  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        g_drop_option = option.strip()
        g_drop_option = g_drop_option[:g_drop_option.find('(') - 1]
        if g_drop_option == 'Local Temp':
            g_pres.set_hidden(True)
            g_temp.set_hidden(False)
            g_temp.set_value(int(local_temp))
            print(str(g_drop_option + str(' ') + str(local_temp)))
        if g_drop_option == 'Remote Temp':
            g_pres.set_hidden(True)
            g_temp.set_hidden(False)
            g_temp.set_value(remote_temp)
            print(str(g_drop_option + str(' ') + str(remote_temp)))
        if g_drop_option == 'Local Pressure':
            g_pres.set_hidden(False)
            g_temp.set_hidden(True)
            g_pres.set_value(local_pressure)
            print(str(g_drop_option + str(' ') + str(local_pressure)))
        if g_drop_option == 'Remote Pressure':
            g_pres.set_hidden(False)
            g_temp.set_hidden(True)
            g_pres.set_value(remote_pressure)
            print(str(g_drop_option + str(' ') + str(remote_pressure)))


g_cont = alte.Page(x=0, y=t.get_height(), height=LV_VER_RES - t.get_height(), width=LV_HOR_RES,
                   color=w_colors['light_bg'], radius=0)
g_drop = alte.Dropdown(parent=g_cont, x=35, y=5, width=250,
                       options=['Local Temp (' + units + ')', 'Remote Temp (' + units + ')', 'Local Pressure (hPa)',
                                'Remote Pressure (hPa)'], color=w_colors['dark_bg'])
g_temp = alte.Gauge(parent=g_cont, x=80, y=44, gauge_color=0xFF0000, length=160, initial_value=0, max_value=50)
g_pres = alte.Gauge(parent=g_cont, x=80, y=44, gauge_color=0xFF0000, length=160, initial_value=900, min_value=900,
                    max_value=1100)
g_pres.set_hidden(True)
g_cont.set_hidden(True)
g_drop.set_event_cb(g_gauge_drop_event)


# --------------------------------------------------------------- #
# ---------------------- Main Page Funcs ---------------------------#
def main_page_change_state(hidden):
    global b
    b.set_hidden(hidden)


# --------------------------------------------------------------- #
# ---------------------- Settings Page Funcs ---------------------------#
def settings_page_change_state(hidden):
    global s_cont
    s_cont.set_hidden(hidden)


# --------------------------------------------------------------- #
# ---------------------- Gauge Page Funcs ---------------------------#
def gauge_page_change_state(hidden):
    global g_cont
    g_cont.set_hidden(hidden)
    pass


# --------------------------------------------------------------- #
# ---------------------- Buttons A,B,C ---------------------------#
def btnA_pressed():
    main_page_change_state(hidden=False)
    settings_page_change_state(hidden=True)
    gauge_page_change_state(hidden=True)
    pass


def btnB_pressed():
    main_page_change_state(hidden=True)
    settings_page_change_state(hidden=False)
    gauge_page_change_state(hidden=True)
    pass


def btnC_pressed():
    main_page_change_state(hidden=True)
    settings_page_change_state(hidden=True)
    gauge_page_change_state(hidden=False)
    pass


btnA.wasPressed(btnA_pressed)
btnB.wasPressed(btnB_pressed)
btnC.wasPressed(btnC_pressed)


# --------------------------------------------------------------- #
# ---------------------- MQTT ---------------------------#
def alert_close_func():
    global alert_flag
    alert_flag = True


def fetch_data(topic_data):
    global remote_temp, remote_pressure, units, alert_flag
    print(topic_data)
    json_data = ujson.loads(str(topic_data))
    remote_pressure = int(json_data['pressure'])
    if units == 'C':
        remote_temp = int(json_data['temperature'])
    else:
        remote_temp = C_to_F(int(json_data['temperature']))

    if alert_flag:
        alert_flag = False
        a = altw.Alert(text='BPS has detected ubnormal temperature.',
                       text_color=global_themes[theme_dict[s_theme_drop_option]]['font'],
                       title=lv.SYMBOL.WARNING + " Warning!", title_color=0xFF0000,
                       color=global_themes[theme_dict[s_theme_drop_option]]['light'], close_func=alert_close_func)
        # email_client = altn.GridEmail('', 'weathermon23@gmail.com')
        # email_client.send_email('', 'WeatherMon Station Update', 'BPS Has Detected Abnormal Temperature')

    g_pres.set_value(remote_pressure)
    g_temp.set_value(remote_temp)
    remote_disc.set_text('Temp: ' + str(remote_temp) + units)
    remote_pres.set_text(str(remote_pressure) + ' hPa')
    pass


connect_wifi('TH', 'thomas1234')
m5mqtt = M5mqtt('subscriber', 'io.adafruit.com', 1883, 'WeatherMon', '', 300)
m5mqtt.subscribe(str('WeatherMon/feeds/weathermonfeed'), fetch_data)
m5mqtt.start()

# --------------------------------------------------------------- #
# ---------------------- General ---------------------------#
widgets_with_text = [temp_val, temp_disc, temp_pres, uv_text, uv_val, humid_val, wind_val, remote_title, remote_disc,
                     remote_pres, s_title, s_theme_label, s_refresh_label, s_bright_label]  # s_units_label, s_units_F]
widgets_with_dark_color = [w_temp, w_icon, w_remote, w_uv, w_wind, w_humid]
widgets_with_border = [s_theme_drop, s_refresh_drop, s_save, g_drop, g_temp, g_pres]  # ,s_units_switch
widgets_with_light_color = [s_cont, g_cont]


def refresh_colors(index):
    light_bg_color = None
    dark_bg_color = None
    font_color = None
    if index == DEFAULT_THEME:
        light_bg_color = w_colors['light_bg']
        dark_bg_color = w_colors['dark_bg']
        font_color = w_colors['font']

        w_temp.set_style_local_bg_color(w_temp.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['temp']))
        w_icon.set_style_local_bg_color(w_icon.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['icon']))
        w_remote.set_style_local_bg_color(w_remote.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['remote']))
        w_uv.set_style_local_bg_color(w_uv.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['uv']))
        w_wind.set_style_local_bg_color(w_wind.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['wind']))
        w_humid.set_style_local_bg_color(w_humid.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(w_colors['humid']))
    else:
        light_bg_color = global_themes[index]['light']
        dark_bg_color = global_themes[index]['dark']
        font_color = global_themes[index]['font']

        for widget in widgets_with_dark_color:
            widget.set_style_local_bg_color(widget.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(dark_bg_color))

    screen.set_screen_bg_color(light_bg_color)

    for widget in widgets_with_light_color:
        widget.set_style_local_bg_color(widget.PART.BG, lv.STATE.DEFAULT, lv.color_hex(light_bg_color))

    for widget in widgets_with_border:
        widget.set_style_local_border_color(widget.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(dark_bg_color))
        widget.set_style_local_border_color(widget.PART.MAIN, lv.STATE.FOCUSED, lv.color_hex(dark_bg_color))

    for widget in widgets_with_text:
        widget.set_style_local_text_color(widget.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(font_color))

    s_bright.set_style_local_bg_color(s_bright.PART.INDIC, lv.STATE.DEFAULT, lv.color_hex(font_color))
    s_bright.set_style_local_bg_color(s_bright.PART.KNOB, lv.STATE.DEFAULT, lv.color_hex(font_color))
    t.set_color(dark_bg_color)
    t.set_text_color(font_color)


def refresh_minor():
    global time_date
    print('Refresh Minor Underway')
    time_date = fetch_date_time()
    t.set_text(time_date)
    t.show_battery()
    isconn = wcfg.is_connected()
    if isconn:
        t.show_green_wifi()
    else:
        t.show_red_wifi()


def refresh_major():
    global weather_dict, local_temp, local_pressure, major_refresh_rate, units
    print('Refresh Major Underway')
    weather_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', units)
    print(weather_dict)
    local_temp = int(weather_dict['temperature'])
    local_pressure = int(float(weather_dict['pressure']))
    g_temp.set_value(int(local_temp))
    g_pres.set_value(local_pressure)
    temp_val.set_text(str(local_temp) + units)
    temp_disc.set_text(str(weather_dict['description']))
    temp_pres.set_text(str(local_pressure) + ' hPa')
    humid_val.set_text(str(weather_dict['humidity']) + '%')
    wind_val.set_text(str(weather_dict['wind']) + 'm/s')
    icon_icon.set_src(str(weather_dict['icon-url']))
    if 'error' not in str(weather_dict['icon-url']):
        icon_icon.set_pos(-22, -22)

    if g_drop_option == 'Local Temp':
        g_temp.set_value(local_temp)
    if g_drop_option == 'Remote Temp':
        g_temp.set_value(remote_temp)


stopper = 0  # Should add modulo (refresh rate)
while True:
    refresh_minor()
    if stopper == 0:
        refresh_major()
    stopper = (stopper + 60) % major_refresh_rate
    print(str('Major Refresh Rate: ' + str(major_refresh_rate) + '\nStopper: ' + str(stopper)))
    wait(60)

# --------------------------------------------------------------- #
