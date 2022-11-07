from m5stack import *
from m5stack_ui import *
from uiflow import *
import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

try:
    bps_0 = unit.get(unit.BPS, unit.PORTA)
except Exception as e:
    bps_0 = None
    warning_label = M5Label('WARNING: BPS unit maybe not connect.', x=15, y=150, color=0xFF0000, font=FONT_MONT_14,
                            parent=None)


def refresh_readings():
    if not bps_0:
        return
    temperature, pressure = bps_0.temperature(), bps_0.pressure()
    if temperature >= 20:
        temperature_label.set_text_color(0xFF3333)
    else:
        temperature_label.set_text_color(0x6699FF)
    temperature_label.set_text('Temperature: ' + str(temperature) + ' °C')
    pressure_label.set_text('Pressure: ' + str((pressure * 100)) + ' Pa')


temperature_label = M5Label('Temperature: ' + 'N/A' + ' °C', x=50, y=30, color=0x000, font=FONT_MONT_14, parent=None)
pressure_label = M5Label('Pressure: ' + 'N/A' + ' Pa', x=50, y=60, color=0x000, font=FONT_MONT_14, parent=None)
refresh_button = M5Btn(text='Refresh', x=125, y=180, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14,
                       parent=None)
refresh_readings()


def refresh_button_wasPressed():
    refresh_readings()


refresh_button.pressed(refresh_button_wasPressed)
