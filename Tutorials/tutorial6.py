'''
Tutorial 6 example -- Alert message 
'''
from ALTconnection import *
from ALTwidgets import *
from m5stack import *
from ALTelements import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)
                
button = Button(x=40, y=100, text='Change Background Color', text_color=0x4682B4,
                 color=0x4682B4, height=60, width=250, is_toggled=False, font=lv.font_montserrat_18)
# label = Label(x=100, y=20, text='Choose a color', font=lv.font_montserrat_18, text_color=0xFFFFFF)

picker = 0

def alert_message(src, event):
    global picker 
    if event == lv.EVENT.CLICKED:
        Alert("Background color is changed", text_color=0x000, title='', title_color=0x000, color=0xFFFFFF,
                 sound_alert=False, close_func=None)
        picker = picker + 1
        if picker == 1:
            color = 0x000
        elif picker == 2:
            color = 0xB6D0E2
        else :
            color = 0x4682B4
            picker = 0
        screen.set_screen_bg_color(color)
        
#When pressing on the button call refresh_readings function
button.set_event_cb(alert_message)
