from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5mqtt import M5mqtt
from connection import *
import time


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

# This is a working example for subscribing to an mqtt server

connect_wifi("ICST","arduino123")
label0 = M5Label('label0', x=115, y=97, color=0x000, font=FONT_MONT_22, parent=None)

def func(topic_data):
  # global params
  label0.set_text(topic_data)
  #print(topic_data)
  pass


m5mqtt = M5mqtt('subscriber', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_EFNz48mbZBaSwjDdXfBGusa9xIoO', 300)
m5mqtt.subscribe(str('WeatherMon/feeds/weathermonfeed'), func)
m5mqtt.start()

wait(20)
print('Bye')
m5mqtt.deinit()
