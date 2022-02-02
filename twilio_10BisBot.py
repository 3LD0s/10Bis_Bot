from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import ten_bis
import re
from main_flow import MainFlow

app = Flask(__name__)
counter = 0
flow = MainFlow()
resp = MessagingResponse()
otp = ''


@app.route('/bot', methods=['POST'])
def bot():
    global counter
    incoming_msg = request.values.get('Body', '').lower()
    counter += 1
    global resp
    msg = resp.message()

    print("+ " + incoming_msg)
    responded = False

    if incoming_msg in ['הי', 'שלום', 'התחל', 'התחלה'] or counter == 1:
        response = """
         *היי! ברוכים הבאים 10BISBOT*
        אני פה כדי לעזור לך לנצל את כרטיס התן-ביס שלך עד הסוף!
        הנה כמה מהדברים שאני יכול לעשות:
        
        > *'יתרה'*: אבדוק מה היתרה החודשית שלך
        
        > *'תזכורת'*: בכל סוף חודש אזכיר לך שסוף החודש עוד מעט נגמר ויש עוד מה לנצל
        
        > *'קניה':* אקנה עבורך תלושים בכסף שנשאר לך!
        """
        msg.body(response)
        responded = True

    elif 'קניה' in incoming_msg:
        flow.buy_vouchers()
        responded = True

    elif incoming_msg in ['תזכורת', 'מתוזמנת']:
        flow.schedule_buy()
        responded = True

    elif 'יתרה' in incoming_msg:
        # Get Monthly Balance From 10BIS
        flow.get_balance()
        responded = True

    elif get_otp(incoming_msg):
        # TODO: write otp to incoming logger
        with open('user_input.txt', 'w') as f:
            global otp
            f.write(otp)
        ten_bis.send_massage('אוקי רק שניה...', flow.phone)
        responded = True

    elif incoming_msg == "1" or incoming_msg == "2":
        with open('user_input.txt', 'w') as f:
            f.write(incoming_msg)
        responded = True

    if not responded:
        msg.body('אני מבין רק כמה פקודות בסיסיות, סליחה :(')

    return str(resp)


def get_otp(string):
    global otp
    try:
        otp = str(re.findall(r"\D(\d{5})\D", " " + string + " ")[0])
        if otp:
            return True
        else:
            return False
    except Exception:
        return False


if __name__ == '__main__':
    app.run()

