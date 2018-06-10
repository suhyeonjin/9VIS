#-*- coding: utf-8-*-
from twilio.rest import Client

class twilioSMS():
    def sendSMS(self):
        # Your Account Sid and Auth Token from twilio.com/console
        self.account_sid = 'AC73bf97d681eee2ae0beb6a8a336de0d1'
        self.auth_token = ''
        self.client = Client(self.account_sid, self.auth_token)

        message = self.client.messages.create(
            body='감시카메라에 움직임이 감지되었습니다.',
            to='+821053803897',
            from_='+18043150468'
        )
        print "[!] Send SMS!"
        print (message.sid)
