import random
import ubinascii
import urequests as requests


class SendGridEmail:
    def __init__(self, sender_address, sender_auth):
        self.sender_address = sender_address
        self.SendGrid_sender_auth = sender_auth

    def send_email(self, subject, body, receiver_address):
        headers = {'Authorization': self.SendGrid_sender_auth, }
        json_data = {'personalizations': [{'to': [{'email': receiver_address, }, ], }, ],
                     'from': {'email': self.sender_address, }, 'subject': subject,
                     'content': [{'type': 'text/plain', 'value': body, }, ], }
        try:
            response = requests.post('https://api.sendgrid.com/v3/mail/send', headers=headers, json=json_data)
        except Exception as e:
            print('Failed Sending Email: ' + str(e))
        print('Email Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)
        
    def verf_code(self, receiver_address, code_len=8):
      max_number = 10**code_len - 1
      code = str(random.randint(0, max_number))
      code = '0'*(code_len-len(code)) + code
      self.send_email('Verification Code', 'Use verification code ' + code + ' for authentication.', receiver_address)
      return code


class TwilioSMS:
    def __init__(self, account_sid, auth_token, service_sid):
        self.twilio_account_sid = account_sid
        self.twilio_auth_token = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()
        self.twilio_service_sid = service_sid

    def send_sms(self, body, to_number):
        data = 'Body={body}&To={to_number}&MessagingServiceSid={mssid}'.format(body=body,
                                                                               to_number=to_number.replace('+', '%2B'),
                                                                               mssid=self.twilio_service_sid)
        try:
            response = requests.post(
                'https://api.twilio.com/2010-04-01/Accounts/' + self.twilio_account_sid + '/Messages.json', data=data,
                headers={'Authorization': b'Basic ' + self.twilio_auth_token,
                         'Content-Type': 'application/x-www-form-urlencoded'})
        except Exception as e:
            print('Failed Sending SMS: ' + str(e))
        print('SMS Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)
        
    def verf_code(self, to_number, code_len=8):
      max_number = 10**code_len - 1
      code = str(random.randint(0, max_number))
      code = '0'*(code_len-len(code)) + code
      self.send_sms('Use verification code ' + code + ' for authentication.', to_number)
      return code


class TwilioWhatsApp:
    def __init__(self, account_sid, auth_token, from_number):
        self.twilio_account_sid = account_sid
        self.twilio_auth_token = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()
        self.twilio_from_number = from_number

    def send_whatsapp_message(self, body, to_number):
        data = 'Body={body}&To=whatsapp:{to_number}&From=whatsapp:{from_number}'.format(body=body,
                                                                      to_number=to_number.replace('+', '%2B'),
                                                                      from_number=self.twilio_from_number.replace('+',
                                                                                                                  '%2B'))
        try:
            response = requests.post(
                'https://api.twilio.com/2010-04-01/Accounts/' + self.twilio_account_sid + '/Messages.json', data=data,
                headers={'Authorization': b'Basic ' + self.twilio_auth_token,
                         'Content-Type': 'application/x-www-form-urlencoded'})
        except Exception as e:
            print('Failed Sending WhatsApp Message: ' + str(e))
        print('WhatsApp Message Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)
        
    def verf_code(self, to_number, code_len=8):
      max_number = 10**code_len - 1
      code = str(random.randint(0, max_number))
      code = '0'*(code_len-len(code)) + code
      self.send_sms('Use verification code ' + code + ' for authentication.', to_number)
      return code
