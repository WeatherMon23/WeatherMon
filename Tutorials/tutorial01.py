'''
Tutorial 1 example -- creating a title 
'''

from ALTwidgets import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

## Creating an element which is displayed on the screen ##
title = Title(color=0x191970)
title.show_battery()
title.show_red_wifi()
title.set_text("My Title")
title.show_red_cloud()