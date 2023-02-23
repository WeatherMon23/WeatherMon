'''
Tutorial 12 example -- publisher (MQTT)
'''
from m5stack import *
from m5mqtt import M5mqtt
from ALTelements import *
from ALTconnection import *
import time


## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)


## Connecting to wifi ##
connect_wifi("TH", "thomas1234")
m5mqtt = M5mqtt('kjgwdd', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_Hzae8396FuVde9G4ORx1ap1nWmdy', 300)
m5mqtt.start()

var = 0
for count in range(10):
  var = var + 1
  m5mqtt.publish(str('WeatherMon/feeds/exampleFeed'), str(var), 1)
  time.sleep(1)
