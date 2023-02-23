'''
Tutorial 3 example -- creating elements
'''
from ALTelements import *
from m5stack import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x4682B4)

## Display elements on the widgets ##
image = Image(x=135, y=50, src='/flash/Assets/Icons/globe.png')
label = Label(x=85, y=20, text='Earth is beautiful', font=lv.font_montserrat_18, text_color=0xFFFFFF)
line = Line( x=60, y=110, length=200, is_vertical=True, width=2, color=0x000000)
checkbox1 = Checkbox(x=90, y=130, text='Agree', text_color=0xFFFFFF, color=0x000000)
checkbox2 = Checkbox(x=90, y=160, text='Do not agree', text_color=0xFFFFFF, color=0x000000)
checkbox3 = Checkbox(x=90, y=190, text='I do not care', text_color=0xFFFFFF, color=0x000000)
