from m5stack import *
from m5stack_ui import *
from uiflow import *
from Connection import *
from Backend import *
from Widgets import *
    

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

connect_wifi("TH", "thomas1234")


print(fetch_local_weather_from_web('C'))
api_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', 'C')
print(api_dict)
image0 = M5Img(api_dict['icon-url'], x=93, y=64, parent=None)

time_s = fetch_time()
button2 = M5Fadingbtn(time_s, 100, 0, 100, 30, 0xF222222, 0xF655333)