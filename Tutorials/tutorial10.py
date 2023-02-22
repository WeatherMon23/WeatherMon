'''
Tutorial 10 example -- Sending an SMS
'''
from m5stack import *
from ALTnotifications import *
# from ALTconnection import *
from ALTwidgets import *
from ALTelements import *
# import time

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

send_button = Button(x=125, y=180, text='Send SMS', text_color=0x4682B4,
                 color=0x4682B4, height=40, width=100, is_toggled=False, font=lv.font_montserrat_18)


def send_message(src, event):
    if event == lv.EVENT.CLICKED:
        sms = TwilioSMS('account_sid', 'auth_token', 'service_sid')
        sms.send_sms('to_number', 'hello')
        lcd.print('ok', 0, 0, 0xffffff)
    else:
        lcd.print('error', 0, 0, 0xffffff)

        
#When pressing on the button call refresh_readings function
send_button.set_event_cb(send_message)
