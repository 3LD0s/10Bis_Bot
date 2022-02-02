from twilio.rest import Client
import schedule
import time
from datetime import datetime

account_sid = 'ACd75121056db21981c932136355c6895e'
auth_token = '53b23266d5cf8feb347fc27d22df5107'
client = Client(account_sid, auth_token)


# for check
def check_if_end_of_month():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    pass


# for whatsapp
def send_whatsapp(message):
    message = client.messages.create(
        from_='whatsapp:<assigned twilio number>',
        body=message,
        to='whatsapp:+972504083675'
    )
    print(message.sid)


