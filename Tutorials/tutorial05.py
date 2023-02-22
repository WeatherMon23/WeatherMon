'''
Tutorial 5 example -- connecting to the wifi 
'''
from ALTconnection import *
from ALTwidgets import *
from m5stack import *
import time

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

## Creating an element which is displayed on the screen ##
title = Title(color=0x191970)
title.show_red_wifi()

wifi_SSD = "Cellcom-WiFi_01"
wifi_pass = "0503322407"

## Connecting to wifi ##
connect_wifi(wifi_SSD, wifi_pass)

def checking_wifi():
    isconn = wifiCfg.is_connected()
    if isconn:
        title.show_green_wifi()
    else:
        title.show_red_wifi()

stopper = 0
while True:
    checking_wifi()
    print(stopper)
    stopper = stopper + 1
    if stopper == 5:
        break
    time.sleep(10)