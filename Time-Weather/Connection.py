from m5stack import *
from m5stack_ui import *
from uiflow import *

import wifiCfg
import urequests
import os

def connect_wifi(ssid, password):
    try:
        wifiCfg.doConnect(ssid, password)
        print('Connection Established')
        return True
    except Exception as e:
        print("Can't Connect to WIFI : " + str(e), 0, 0, 0x000)
        return False
    

