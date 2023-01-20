from m5stack import *
from m5stack_ui import *
from uiflow import *

from Backend import *
from Connection import *
from Widgets import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

connect_wifi("ICST", "arduino123")

# print(fetch_local_weather_from_web('F'))
# api_dict = fetch_local_weather_from_api('f5ea650f7e2d0b0459b76f5816318ecc', 'C')
# print(api_dict)
# image0 = M5Img(api_dict['icon-url'], x=93, y=64, parent=None)


# mbox.set_text('Helloooo')

# time_s = fetch_time()
# button2 = M5Fadingbtn(time_s, 100, 0, 100, 30, 0xF222222, 0xF655333)


# tab = M5Tabview(0,2)
# tab.add_tab("tab1")
# mbox = M5Msgbox(None, 0, 10)
# tab.add_tab("tab2")
# tab.add_tab("tab3")

# tab.set_tab_name(0, 't1')
res = fetch_date_time()
title = M5Title(res, 0xFFFFFF, 0x605959)
title.show_red_wifi()
title.show_red_cloud()
title.show_battery()
