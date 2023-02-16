import random

import ubinascii
import urequests


class GridEmail:
    """
    A class used to represent a Grid-Email object

    ...

    Attributes
    ----------
    sender_address : str
        The Email address of the sender
    sendgrid_auth_token : str
        The account's authentication token from SendGrid
    
    Methods
    -------
    send_email(self, receiver_address, subject='', body='')
        Sends an email

    verf_code(self, receiver_address, code_len=8)
        Sends an email with a verification code to destination
    """

    def __init__(self, auth_token, sender_address):
        """
        Parameters
        ----------
        sender_address : str
            The Email address of the sender
        auth_token : str
            The account's authentication token from SendGrid
        """

        self.sender_address = sender_address
        self.sendgrid_auth_token = auth_token

    def send_email(self, receiver_address, subject='', body=''):
        """
        Sends an Email message

        Parameters
        ----------
        receiver_address : str
            The Email address to receive the message
        subject : str
            The subject of the Email message (default is empty string)
        body : str
            The body of the Email message (default is empty string)
        """

        headers = {'Authorization': self.sendgrid_auth_token, }
        json_data = {'personalizations': [{'to': [{'email': receiver_address, }, ], }, ],
                     'from': {'email': self.sender_address, }, 'subject': subject,
                     'content': [{'type': 'text/plain', 'value': body, }, ], }
        try:
            response = urequests.post('https://api.sendgrid.com/v3/mail/send', headers=headers, json=json_data)
        except Exception as e:
            print('Failed Sending Email: ' + str(e))
            return
        print('Email Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)

    def verf_code(self, receiver_address, code_len=8):
        """
        Sends a verification code in Email

        Parameters
        ----------
        receiver_address : str
            The Email address to receive the verification code
        code_len : integer
            Number of digits in the verification code (default is 8)

        Returns
        -------
        str
            The generated verification code
        """

        max_number = 10 ** code_len - 1
        code = str(random.randint(0, max_number))
        code = '0' * (code_len - len(code)) + code
        self.send_email(receiver_address, 'Verification Code', 'Use verification code ' + code + ' for authentication.')
        return code


class TwilioSMS:
    """
    A class used to represent a Twilio-SMS object

    ...

    Attributes
    ----------
    twilio_account_sid : str
        The account's SID from Twilio
    twilio_auth_token : str
        The account's authentication token from Twilio
    twilio_service_sid : str
        The account's service SID from Twilio

    Methods
    -------
    send_sms(self, to_number, body='')
        Sends an SMS message

    verf_code(self, receiver_address, code_len=8)
        Sends an SMS with a verification code to destination
    """

    def __init__(self, account_sid, auth_token, service_sid):
        """
        Parameters
        ----------
        account_sid : str
            The account's SID from Twilio
        auth_token : str
            The account's authentication token from Twilio
        service_sid : str
            The account's service SID from Twilio
        """

        self.twilio_account_sid = account_sid
        self.twilio_auth_token = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()
        self.twilio_service_sid = service_sid

    def send_sms(self, to_number, body=''):
        """
        Sends an SMS

        Parameters
        ----------
        to_number : str
            The number to receive the message
        body : str
            The contents of the message (default is empty string)
        """

        data = 'Body={body}&To={to_number}&MessagingServiceSid={mssid}'.format(body=body,
                                                                               to_number=to_number.replace('+', '%2B'),
                                                                               mssid=self.twilio_service_sid)
        try:
            response = urequests.post(
                'https://api.twilio.com/2010-04-01/Accounts/' + self.twilio_account_sid + '/Messages.json', data=data,
                headers={'Authorization': b'Basic ' + self.twilio_auth_token,
                         'Content-Type': 'application/x-www-form-urlencoded'})
        except Exception as e:
            print('Failed Sending SMS: ' + str(e))
            return
        print('SMS Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)

    def verf_code(self, to_number, code_len=8):
        """
        Sends a verification code in an SMS

        Parameters
        ----------
        to_number : str
            The number to receive the verification code in an SMS
        code_len : integer
            Number of digits in the verification code (default is 8)

        Returns
        -------
        str
            The generated verification code
        """

        max_number = 10 ** code_len - 1
        code = str(random.randint(0, max_number))
        code = '0' * (code_len - len(code)) + code
        self.send_sms(to_number, 'Use verification code ' + code + ' for authentication.')
        return code


class TwilioWhatsApp:
    """
    A class used to represent a Twilio-WhatsApp object

    ...

    Attributes
    ----------
    twilio_account_sid : str
        The account's SID from Twilio
    twilio_auth_token : str
        The account's authentication token from Twilio
    twilio_from_number : str
        The phone number of the sender

    Methods
    -------
    send_whatsapp_message(self, to_number, body='')
        Sends a WhatsApp message

    verf_code(self, receiver_address, code_len=8)
        Sends a WhatsApp message with a verification code to destination
    """

    def __init__(self, account_sid, auth_token, from_number):
        """
        Parameters
        ----------
        account_sid : str
            The account's SID from Twilio
        auth_token : str
            The account's authentication token from Twilio
        from_number : str
            The phone number of the sender
        """

        self.twilio_account_sid = account_sid
        self.twilio_auth_token = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()
        self.twilio_from_number = from_number

    def send_whatsapp_message(self, to_number, body=''):
        """
        Sends a WhatsApp message

        Parameters
        ----------
        to_number : str
            The number to receive the message
        body : str
            The contents of the message (default is empty string)
        """

        data = 'Body={body}&To=whatsapp:{to_number}&From=whatsapp:{from_number}'.format(body=body,
                                                                                        to_number=to_number.replace('+',
                                                                                                                    '%2B'),
                                                                                        from_number=self.twilio_from_number.replace(
                                                                                            '+', '%2B'))
        try:
            response = urequests.post(
                'https://api.twilio.com/2010-04-01/Accounts/' + self.twilio_account_sid + '/Messages.json', data=data,
                headers={'Authorization': b'Basic ' + self.twilio_auth_token,
                         'Content-Type': 'application/x-www-form-urlencoded'})
        except Exception as e:
            print('Failed Sending WhatsApp Message: ' + str(e))
            return
        print('WhatsApp Message Sent With Status Code: ' + str(response.status_code))
        print('Response: ' + response.text)

    def verf_code(self, to_number, code_len=8):
        """
        Sends a verification code in a WhatsApp message

        Parameters
        ----------
        to_number : str
            The number to receive the verification code in a WhatsApp message
        code_len : integer
            Number of digits in the verification code (default is 8)

        Returns
        -------
        str
            The generated verification code
        """

        max_number = 10 ** code_len - 1
        code = str(random.randint(0, max_number))
        code = '0' * (code_len - len(code)) + code
        self.send_whatsapp_message(to_number, 'Use verification code ' + code + ' for authentication.')
        return code
