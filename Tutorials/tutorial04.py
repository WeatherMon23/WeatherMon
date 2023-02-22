'''
Tutorial 4 example -- reading sensor and displaying values 
'''
import unit
from m5stack import *
from ALTelements import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

# Connect to sensor
bps_0 = unit.get(unit.BPS, unit.PORTA)

# a function to read the measured data on button pressing
def refresh_readings(src, event):
    if event == lv.EVENT.CLICKED:
        if not bps_0:
            return
        temperature, pressure = bps_0.temperature(), bps_0.pressure()
        temperature_label.set_text('Temperature: ' + str(temperature) + ' °C')
        pressure_label.set_text('Pressure: ' + str((pressure * 100)) + ' Pa')

# Creating the values displayed on te Screen
temperature_label = Label(x=50, y=30, text='Temperature: ' + 'N/A' + ' °C', font=lv.font_montserrat_18,
                          text_color=0xFF3333)
pressure_label = Label(x=50, y=60, text='Pressure: ' + 'N/A' + ' Pa', font=lv.font_montserrat_18, text_color=0x000)
refresh_button = Button(x=125, y=180, text='Refresh', text_color=0x4682B4,
                 color=0x4682B4, height=40, width=100, is_toggled=False, font=lv.font_montserrat_18)

#When pressing on the button call refresh_readings function
refresh_button.set_event_cb(refresh_readings)

