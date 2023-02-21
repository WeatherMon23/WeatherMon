import lvgl as lv
import ujson
import unit
from m5mqtt import M5mqtt
from m5stack import *
from m5stack_ui import *
from uiflow import *

from ALTelements import *
from ALTweb_server import *
from ALTwidgets import *

# ------------------------------------------------- #
# -------------------- GLOBALS -------------------- #
LV_HOR_RES = 320
LV_VER_RES = 240

'''
    index 0: Green Theme
    index 1: Light Theme
    index 2: Dark Theme
'''
theme_index = 0
global_themes = [{'dark': 0x115400, 'light': 0x1C8900, 'font': 0xFFFFFF},
                 {'dark': 0xD8D8D8, 'light': 0xFFFFFF, 'font': 0x000000},
                 {'dark': 0x000000, 'light': 0x2A2A2A, 'font': 0xFFFFFF}]

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(global_themes[theme_index]['light'])

bps = None
bps_temp = 0
bps_pres = 0
bps_humid = 0
units = 'C'
time_date = '01 Jan 00:00'
weather_dict = None
refresh_rate = -1
chart_points = 10
sum_points = 20
# Local buffer size:
unpublished_points = 10

isconn = wifiCfg.is_connected()

temp_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pres_list = [900, 900, 900, 900, 900, 900, 900, 900, 900, 900]
sum_list = []
unpublished_list = []

temp_reads = [(0xff0000, temp_list)]
pres_reads = [(0x00ff00, pres_list)]

# ------------------------------------------------- #
# -------------------- MQTT -------------------- #
connect_wifi('TH', 'thomas1234')
mqtt_con = M5mqtt('publisher', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_RqUD02IMuP8XxkBI3Bv6lE7DJ2Vs', 300)
mqtt_con.start()

# ------------------------------------------------- #
# -------------------- TITLE -------------------- #
t = Title(color=global_themes[theme_index]['dark'])
t.show_battery()
if isconn:
    t.show_green_wifi()
else:
    t.show_red_wifi()

t.set_text(time_date)


# ------------------------------------------------- #
# -------------------- MAIN PAGE -------------------- #

def reset_charts(new_temp, new_pres, new_humid, is_click):
    global temp_list, pres_list, sum_list, temp_reads, pres_reads, temp_chart, pres_chart
    date_time = fetch_date_time()
    sum_list.insert(0, (new_temp, new_pres, new_humid, is_click, date_time))
    sum_list = sum_list[:sum_points]

    temp_list.insert(0, new_temp)
    temp_list = temp_list[:chart_points]
    pres_list.insert(0, new_pres)
    pres_list = pres_list[:chart_points]
    temp_reads = [(temp_reads[0][0], temp_list)]
    pres_reads = [(pres_reads[0][0], pres_list)]
    print(unpublished_list)
    print(temp_reads)
    print(pres_reads)
    print(sum_list)
    temp_chart_hid = temp_chart.get_hidden()
    pres_chart_hid = pres_chart.get_hidden()
    temp_chart.delete()
    pres_chart.delete()
    temp_chart = Chart(parent=m_cont, x=60, y=94, height=110, width=200, min_val=0, max_val=50, input_vector=temp_reads,
                       chart_type=lv.chart.TYPE.LINE)
    pres_chart = Chart(parent=m_cont, x=60, y=94, height=110, width=200, min_val=900, max_val=1100,
                       input_vector=pres_reads, chart_type=lv.chart.TYPE.LINE)

    pres_chart.set_hidden(pres_chart_hid)
    temp_chart.set_hidden(temp_chart_hid)


def refresh_handler(source, evt):
    global temp_l, pres_l, bps_temp, bps_pres
    if evt == lv.EVENT.CLICKED:
        refresh_reads(True)


m_cont = Page(x=0, y=t.get_height(), height=LV_VER_RES - t.get_height(), width=LV_HOR_RES,
              color=global_themes[theme_index]['light'], radius=0)
temp_l = Label(parent=m_cont, x=4, y=4, text=str('BPS Temperature: N/A ' + units), font=lv.font_montserrat_18,
               text_color=global_themes[theme_index]['font'])
pres_l = Label(parent=m_cont, x=4, y=29, text=str('BPS Pressure: N/A hPa'), font=lv.font_montserrat_18,
               text_color=global_themes[theme_index]['font'])
refresh_btn = Button(parent=m_cont, x=260, y=4, text=lv.SYMBOL.LOOP, height=45, width=45,
                     color=global_themes[theme_index]['dark'], font=lv.font_montserrat_30)

refresh_btn.set_event_cb(refresh_handler)

s_chart_drop_option = 'Temperature'


def s_chart_drop_event(obj, event):
    global s_theme_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 15  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        s_chart_drop_option = str(option.strip())
        s_chart_drop_option = s_chart_drop_option[:len(s_chart_drop_option) - 1]
        print(s_chart_drop_option)
        if s_chart_drop_option == 'Temperature':
            temp_chart.set_hidden(False)
            pres_chart.set_hidden(True)
        if s_chart_drop_option == 'Pressure':
            temp_chart.set_hidden(True)
            pres_chart.set_hidden(False)


drop_options = ['Temperature', 'Pressure']
dropdown = Dropdown(parent=m_cont, x=85, y=59, width=150, options=drop_options,
                    color=global_themes[theme_index]['dark'])
temp_chart = Chart(parent=m_cont, x=60, y=94, height=110, width=200, min_val=0, max_val=50, input_vector=temp_reads,
                   chart_type=lv.chart.TYPE.LINE)
pres_chart = Chart(parent=m_cont, x=60, y=94, height=110, width=200, min_val=900, max_val=1100, input_vector=pres_reads,
                   chart_type=lv.chart.TYPE.LINE)

dropdown.set_event_cb(s_chart_drop_event)
pres_chart.set_hidden(True)

# --------------------------------------------------------------- #
# ---------------------- Settings Page ---------------------------#

s_theme_drop_option = 'Green'


def s_theme_drop_event(obj, event):
    global s_theme_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 15  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        s_theme_drop_option = str(option.strip())
        s_theme_drop_option = s_theme_drop_option[:len(s_theme_drop_option) - 1]
        print(s_theme_drop_option)


s_refresh_drop_option = 'Never'


def s_refresh_drop_event(obj, event):
    global s_refresh_drop_option
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 15  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        s_refresh_drop_option = str(option.strip())
        s_refresh_drop_option = s_refresh_drop_option[:len(s_refresh_drop_option) - 1]
        print(s_refresh_drop_option)


theme_dict = {'Green': 0, 'Light': 1, 'Dark': 2}
rate_dict = {'Never': -1, '30 sec': 30, '1 min': 60, '2 min': 120}


def manage_settings():
    global refresh_rate, s_refresh_drop_option, s_theme_drop_option, units, theme_dict, rate_dict, theme_index
    theme_index = theme_dict[s_theme_drop_option]
    refresh_rate = rate_dict[s_refresh_drop_option]
    refresh_colors(theme_index)


def save_event_handler(source, evt):
    if evt == lv.EVENT.CLICKED:
        manage_settings()
        btnA_pressed()
        print('Settings have been saved!')


summarized_data = "REMOTE DATA SUMMARY\n"


def send_summary_email():
    global summarized_data
    user_email = get_user_input(80, 'Provide your email address at:')
    email_client = altn.GridEmail('Bearer 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',
                                  'weathermon23@gmail.com')
    email_client.send_email('user_email', 'WeatherMon Data Summary', summarized_data)
    print(summarized_data)
    pass


def export_event_handler(source, evt):
    global sum_list, summarized_data
    if evt == lv.EVENT.CLICKED:
        if not sum_list:
            empty_list_alert = Alert('There is no data to export!', text_color=global_themes[theme_index]['font'],
                                     color=global_themes[theme_index]['light'])
            return

        if refresh_rate != -1:
            summarized_data += str('Data is automatically refreshed every ' + str(refresh_rate) + ' seconds.\n\n')
        else:
            summarized_data += str('Data is refreshed only manualy.\n\n')

        i = 1
        for entry in sum_list:
            entry_type = 'Manual' if entry[3] else 'Automatic'
            summarized_data += str(i) + ') ' + str(entry[4]) + ' [' + entry_type + '] - Temperature: ' + str(
                entry[0]) + ' ' + units + ', Pressure: ' + str(entry[1]) + ' hPa' + ', Humidity: ' + str(
                entry[2]) + ' RH\n'
            i += 1
        send_summary_email()


s_cont = Page(x=0, y=t.get_height(), height=LV_VER_RES - t.get_height(), width=LV_HOR_RES,
              color=global_themes[theme_index]['light'], radius=0)
s_cont.set_hidden(True)
s_title = Label(parent=s_cont, x=5, y=5, text=lv.SYMBOL.SETTINGS + ' Settings', font=lv.font_montserrat_30,
                text_color=global_themes[theme_index]['font'])
s_theme_label = Label(parent=s_cont, x=5, y=50, text='Theme: ', font=lv.font_montserrat_22,
                      text_color=global_themes[theme_index]['font'])
s_theme_drop = Dropdown(parent=s_cont, x=100, y=45, options=['Green', 'Light', 'Dark'],
                        color=global_themes[theme_index]['dark'])
s_refresh_label = Label(parent=s_cont, x=5, y=85, text='Automatic refresh: ', font=lv.font_montserrat_22,
                        text_color=global_themes[theme_index]['font'])
s_refresh_drop = Dropdown(parent=s_cont, x=220, y=80, width=75, options=['Never', '30 sec', '1 min', '2 min'],
                          color=global_themes[theme_index]['dark'])
s_bright_label = alte.Label(parent=s_cont, x=5, y=125, text='Brightness: ', font=lv.font_montserrat_22,
                            text_color=global_themes[theme_index]['font'])
s_bright = BrightnessSlider(parent=s_cont, x=60, y=175, color=global_themes[theme_index]['font'], show_label=False)
s_export = Button(parent=s_cont, x=85, y=205, text='Export Data', color=global_themes[theme_index]['dark'], height=35,
                  width=150, font=lv.font_montserrat_22)
s_save = Button(parent=s_cont, x=110, y=250, text='Save', color=global_themes[theme_index]['dark'], height=35,
                width=100, font=lv.font_montserrat_22)

s_theme_drop.set_event_cb(s_theme_drop_event)
s_refresh_drop.set_event_cb(s_refresh_drop_event)
s_export.set_event_cb(export_event_handler)
s_save.set_event_cb(save_event_handler)

# --------------------------------------------------------------- #
# ---------------------- Gauges Page ---------------------------#
g_drop_option = 'BPS Temperature'


def g_gauge_drop_event(obj, event):
    global g_drop_option, bps_temp, bps_pres
    if event == lv.EVENT.VALUE_CHANGED:
        option = " " * 20  # Should be large enough to store the option
        obj.get_selected_str(option, len(option))
        g_drop_option = option.strip()
        g_drop_option = g_drop_option[:g_drop_option.find('(') - 1]
        if g_drop_option == 'BPS Temperature':
            g_pres.set_hidden(True)
            g_temp.set_hidden(False)
            g_temp.set_value(bps_temp)
            print(str(g_drop_option + str(' ') + str(bps_temp)))
        if g_drop_option == 'BPS Pressure':
            g_pres.set_hidden(False)
            g_temp.set_hidden(True)
            g_pres.set_value(bps_pres)
            print(str(g_drop_option + str(' ') + str(bps_pres)))


g_cont = Page(x=0, y=t.get_height(), height=LV_VER_RES - t.get_height(), width=LV_HOR_RES,
              color=global_themes[theme_index]['light'], radius=0)
g_drop = Dropdown(parent=g_cont, x=35, y=5, width=250, options=['BPS Temperature (C)', 'BPS Pressure (kPa)'],
                  color=global_themes[theme_index]['dark'])
g_temp = Gauge(parent=g_cont, x=80, y=44, gauge_color=0xFF0000, length=160, initial_value=0, max_value=50)
g_pres = Gauge(parent=g_cont, x=80, y=44, gauge_color=0xFF0000, length=160, initial_value=900, min_value=900,
               max_value=1100)
g_pres.set_hidden(True)
g_cont.set_hidden(True)
g_drop.set_event_cb(g_gauge_drop_event)


# --------------------------------------------------------------- #
# ---------------------- Main Page Funcs ---------------------------#
def main_page_change_state(hidden):
    global m_cont
    m_cont.set_hidden(hidden)


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

# ------------------------------------------------- #
# -------------------- GENERAL -------------------- #
widgets_with_text = [temp_l, pres_l, s_title, s_theme_label, s_refresh_label,
                     s_bright_label]  # s_units_label, s_units_F]
widgets_with_border = [s_theme_drop, s_refresh_drop, s_save, g_drop, g_temp, g_pres, refresh_btn]  # ,s_units_switch
widgets_with_light_color = [s_cont, g_cont, m_cont]


def refresh_colors(index):
    light_bg_color = global_themes[index]['light']
    dark_bg_color = global_themes[index]['dark']
    font_color = global_themes[index]['font']

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


def publish_the_unpublished():
    global unpublished_list, mqtt_con
    print('Trying to republish the unpublished')
    if unpublished_list:
        mqtt_con.reconnect()
    for entry in unpublished_list:
        print('Republishing: ' + str(entry))
        json_data = {}
        json_data['temperature'] = entry[0]
        json_data['pressure'] = entry[1]
        json_data['humidity'] = entry[2]
        json_data = ujson.dumps(json_data)
        mqtt_con.publish(str('WeatherMon/feeds/weathermonfeed'), json_data, 1)
    unpublished_list = []


def refresh_minor():
    global time_date
    print('Refresh Minor Underway')
    time_date = fetch_date_time()
    t.set_text(time_date)
    t.show_battery()
    isconn = wifiCfg.is_connected()
    if isconn:
        t.show_green_wifi()
        publish_the_unpublished()
    else:
        t.show_red_wifi()


def refresh_reads(is_click=False):
    global bps_temp, bps_pres, bps_humid, unpublished_list
    print('Refresh Reads Underway')
    try:
        bps = unit.get(unit.ENV3, unit.PORTA)
    except Exception as e:
        bps = None
        bps_alert = Alert('ENV3 unit might not be connected!', text_color=global_themes[theme_index]['font'],
                          title=lv.SYMBOL.WARNING + " Warning!", title_color=0xFF0000,
                          color=global_themes[theme_index]['light'])
        return
    rounded_temp = round(bps.temperature)
    bps_temp = rounded_temp
    g_temp.set_value(rounded_temp)
    rounded_pres = round(Pa_to_hPa(bps.pressure))
    bps_pres = rounded_pres
    g_pres.set_value(rounded_pres)
    rounded_humid = round(bps.humidity)
    print(str('Readings: Temp = ' + str(rounded_temp) + units + ', Pressure = ' + str(
        rounded_pres) + 'hPa' + ', Humidity = ' + str(rounded_humid) + 'RH'))
    temp_l.set_text(str('BPS Temperature: ' + str(rounded_temp) + ' ' + units))
    pres_l.set_text(str('BPS Pressure: ' + str(rounded_pres) + ' ' + 'hPa'))
    json_data = {}
    json_data['temperature'] = rounded_temp
    json_data['pressure'] = rounded_pres
    json_data['humidity'] = rounded_humid
    json_data = ujson.dumps(json_data)
    isconn = wifiCfg.is_connected()
    if isconn:
        mqtt_con.publish(str('WeatherMon/feeds/weathermonfeed'), json_data, 1)
    else:
        unpublished_list.append((rounded_temp, rounded_pres, rounded_humid))
        unpublished_list = unpublished_list[-unpublished_points:]

    reset_charts(rounded_temp, rounded_pres, rounded_humid, is_click)


stopper = 0
while True:
    if stopper % 60 == 0:
        refresh_minor()
    if refresh_rate != -1 and stopper % refresh_rate == 0:
        refresh_reads()
    stopper = (stopper + 30) % 120
    print(str('Refresh Reads Rate: ' + str(refresh_rate) + '\nStopper: ' + str(stopper)))
    wait(30)
# ------------------------------------------------- #
