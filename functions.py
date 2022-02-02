from twilio.rest import Client


# send massage to client
# return True if massage sent
# Error if not
def send_massage(msg, phone):
    account_sid = 'ACd75121056db21981c932136355c6895e'
    auth_token = '53b23266d5cf8feb347fc27d22df5107'
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
            from_='whatsapp:+14155238886',
            body=msg,
            to='whatsapp:' + phone
        )
        return True

    except Exception as e:
        print("Error: {0}".format(e))
