'''
Tutorial 11 example -- subscriber (MQTT)
'''
from m5stack import *
from m5mqtt import M5mqtt
from ALTelements import *
from ALTconnection import *


## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)


label = Label(x=150, y=100, text='', font=lv.font_montserrat_22, text_color=0x000000)

def fun_WeatherMon_feeds_examplefeed_(topic_data):
  label.set_text(topic_data)
  pass

wifi_SSD = "Cellcom-WiFi_01"
wifi_pass = "0503322407"

## Connecting to wifi ##
connect_wifi(wifi_SSD, wifi_pass)
m5mqtt = M5mqtt('kjgwdd', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_Hzae8396FuVde9G4ORx1ap1nWmdy', 300)
m5mqtt.subscribe(str('WeatherMon/feeds/exampleFeed'), fun_WeatherMon_feeds_examplefeed_)
m5mqtt.start()