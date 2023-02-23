'''
Tutorial 9 example -- Confirmation with function 
'''
from ALTconnection import *
from ALTwidgets import *
from m5stack import *
from ALTelements import *
import time

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)
                
button = Button(x=40, y=100, text='Click Here', text_color=0x4682B4,
                 color=0x4682B4, height=60, width=250, is_toggled=False, font=lv.font_montserrat_18)
flag = 0
def func():
    global flag
    if flag == 0:
        screen.set_screen_bg_color(0x0F52BA)
        flag = 1
    else :
        screen.set_screen_bg_color(0xB6D0E2)
        flag = 0
            
    
def alert_message(src, event):
    global picker 
    if event == lv.EVENT.CLICKED:
        Confirmation("Do you want to change Background Color?", text_color=0x000000, title='', title_color=0x000000, color=0xFFFFFF,
                 confirm_func=func)
    
        
#When pressing on the button call refresh_readings function
button.set_event_cb(alert_message)

