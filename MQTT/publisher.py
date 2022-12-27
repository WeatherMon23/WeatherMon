from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5mqtt import M5mqtt


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

# This is a working example for publishing to mqtt adafruit mqtt server.

m5mqtt = M5mqtt('publisher', 'io.adafruit.com', 1883, 'WeatherMon', 'aio_EFNz48mbZBaSwjDdXfBGusa9xIoO', 300)
m5mqtt.start()
var = 0
for count in range(10):
  var = var + 1
  m5mqtt.publish(str('WeatherMon/feeds/weathermonfeed'), str(var), 1)
  wait_ms(2000)
