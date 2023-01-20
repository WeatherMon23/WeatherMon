import ubinascii
import urequests
from m5stack import *
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


class TwilioSMS:
    base_url = 'https://api.twilio.com/2010-04-01'

    def __init__(self, account_sid, auth_token):
        self.twilio_account_sid = account_sid
        self.twilio_auth = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()

    def create(self, body, from_number, to_number):
        data = 'Body={body}&From={from_number}&To={to_number}'.format(body=body,
            from_number=from_number.replace('+', '%2B'), to_number=to_number.replace('+', '%2B'))
        r = urequests.post(
            '{base_url}/Accounts/{sid}/Messages.json'.format(base_url=self.base_url, sid=self.twilio_account_sid),
            data=data, headers={'Authorization': b'Basic ' + self.twilio_auth,
                                'Content-Type': 'application/x-www-form-urlencoded'})
        print('SMS sent with status code', r.status_code)
        print('Response: ', r.text)


send_button = M5Btn(text='Send SMS', x=110, y=180, w=100, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14,
                    parent=None)


def send_button_wasPressed():
    try:
        sms = TwilioSMS('account_sid', 'auth_token')
        sms.create('hello', 'from_number', 'to_number')
        lcd.print('ok', 0, 0, 0xffffff)
    except Exception as e:
        lcd.print(str(e), 0, 0, 0xffffff)


send_button.pressed(send_button_wasPressed)
