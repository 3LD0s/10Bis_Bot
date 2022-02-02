import re
from time import sleep
from twilio.rest import Client

welcome_text = ''


def printv(dct):
    msg = "כדי לנצל את כל הכסף שנותר זה מה שאקנה:\n"
    for typeof, amount in dct.items():
        msg += "{0} וואצ'רים של {1}\n".format(amount, typeof)
    return msg


def get_balance_from_ten_bis(web_driver_obj, configurations, is_logged):
    """
    extract the monthly balance from 10Bis
    :param web_driver_obj:
    :param configurations:
    :param is_logged:
    :return:
    """
    global welcome_text
    while not is_logged:
        web_driver_obj.navigate_to_url("https://www.10bis.co.il/next/user-report?dateBias=0")
        sleep(3)

        web_driver_obj.wait_for("//*[@id=\"email\"]")
        web_driver_obj.click_on("//*[@id=\"email\"]", "xpath")
        sleep(2)

        # login
        web_driver_obj.type("email", "id", configurations.get("input_funds").get("email"))
        web_driver_obj.click_on("//button[@type='submit']", "xpath")

        success = False
        while not success:
            # enters OTP
            send_massage("שלח לי את הקוד שנשלח אליך בסמס",
                         configurations.get("input_funds").get("phone"))
            OTP = get_otp()

            try:
                web_driver_obj.wait_for('//*[@id="authenticationCode"]')
                web_driver_obj.click_on('//*[@id="authenticationCode"]', "xpath")
                web_driver_obj.type('//*[@id="authenticationCode"]', "xpath", OTP)
                web_driver_obj.click_on("//button[@type='submit']", "xpath")

                web_driver_obj.wait_for('/html/body/div[2]/div[2]/header/div/div/div[2]/button/div/div', delay=6)

                success = True
                send_massage("מתחבר...",
                             configurations.get("input_funds").get("phone"))
                try:
                    welcome_text = web_driver_obj.get_element_attribute(
                        "/html/body/div[2]/div[2]/header/div/div/div[2]/button/div/div",
                        "xpath", "innerHTML")
                    is_logged = True

                    with open('user_input.txt', 'w') as f:
                        f.write('')

                except Exception:
                    is_logged = False
                    return False

                break

            except Exception:
                with open('user_input.txt', 'w') as f:
                    f.write('')
                send_massage(f"הקוד שגוי, נסה שוב", configurations.get("input_funds").get("phone"))

    print(f"# logged in to 10bis as - {welcome_text.split()[1]}\n")
    send_massage(f" מחובר לחשבון של - {welcome_text.split()[1]}\n", configurations.get("input_funds").get("phone"))

    # get daily usage
    web_driver_obj.wait_for('/html/body/div[2]/div[2]/div[1]/div/div[2]/div[3]/div/div[1]/div/div')
    monthly_balance = web_driver_obj.get_element_attribute(
        '/html/body/div[2]/div[2]/div[1]/div/div[2]/div[3]/div/div[1]/div/div', "xpath", "innerHTML")
    monthly_balance = int(re.findall(r'\d+', monthly_balance)[0])

    return monthly_balance


def get_otp():
    lis = []
    while True:
        with open('user_input.txt', 'r') as f:
            otp = f.read()
        if otp and otp not in lis:
            lis.append(otp)
            break
        else:
            f.close()
    return otp


def buy_voucher(vouchers, web_driver_obj, phone):
    """
    The function who buy the vouchers
    :param phone:
    :param vouchers: dictionary of vouchers amount and type
    :param web_driver_obj:
    :return:
    """
    web_driver_obj.navigate_to_url("https://www.10bis.co.il/next/restaurants/menu/delivery/26698/%D7%A9%D7%95%D7%A4%D7%A8%D7%A1%D7%9C---%D7%9B%D7%9C%D7%9C-%D7%90%D7%A8%D7%A6%D7%99")
    sleep(4)

    for typeof, amount in vouchers.items():

        if typeof == "100":
            while amount > 0:
                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[4]/button/div[1]')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[4]/button/div[1]')
                sleep(1.5)
                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                sleep(3)

                if "order-success" in web_driver_obj.drive.current_url:
                    vouchers[typeof] -= 1
                    amount -= 1
                    send_massage('*קניה בוצעה, הווצ\'ר ישלח למייל*', phone)
                else:
                    send_massage("משהו לא עבד :(", phone)
                    break

            vouchers.pop(typeof)

        if typeof == "50":
            while amount > 0:
                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[3]/button/div[1]')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[3]/button/div[1]')
                sleep(1.5)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                sleep(3)

                if "order-success" in web_driver_obj.drive.current_url:
                    vouchers[typeof] -= 1
                    amount -= 1
                    send_massage('*קניה בוצעה, הווצ\'ר ישלח למייל*', phone)
                else:
                    send_massage("משהו לא עבד :(", phone)
                    break

            vouchers.pop(typeof)

        if typeof == "40":
            while amount > 0:
                web_driver_obj.wait_for(
                    '//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[2]/button/div[1]')
                web_driver_obj.click_on(
                    '//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[2]/button/div[1]')
                sleep(1.5)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                sleep(3)

                if "order-success" in web_driver_obj.drive.current_url:
                    vouchers[typeof] -= 1
                    amount -= 1
                    send_massage('*קניה בוצעה, הווצ\'ר ישלח למייל*', phone)
                else:
                    send_massage("משהו לא עבד :(", phone)
                    break

            vouchers.pop(typeof)

        if typeof == "30":
            while amount > 0:
                web_driver_obj.wait_for(
                    '//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[1]/button/div[1]')
                web_driver_obj.click_on(
                    '//*[@id="main-setion"]/div[1]/div[1]/section/div/div[2]/div[1]/button/div[1]')
                sleep(1.5)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div[3]/div/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                web_driver_obj.click_on('//*[@id="main-setion"]/div[1]/div[2]/div/div/div[1]/button')
                sleep(3)

                web_driver_obj.wait_for('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                web_driver_obj.click_on('//*[@id="modals"]/div/div/div/div/div/div/div[2]/div/div[4]/div/button')
                sleep(3)

                if "order-success" in web_driver_obj.drive.current_url:
                    vouchers[typeof] -= 1
                    amount -= 1
                    send_massage('*קניה בוצעה, הווצ\'ר ישלח למייל*', phone)
                else:
                    send_massage("משהו לא עבד :(", phone)
                    break

            vouchers.pop(typeof)


def number_of_voucher(monthly_balance):
    """
    make the calculation of how many vouchers and which to buy
    :param monthly_balance: the monthly balance of the user.
    :return: number of vouchers, and how much from each.
    """
    voucher_number = 0
    vouchers = {"100": 0, "50": 0, "40": 0, "30": 0}
    while monthly_balance > 30:

        if monthly_balance >= 130:
            monthly_balance -= 100
            voucher_number += 1
            vouchers["100"] += 1

        else:
            match (int(monthly_balance/10))*10:

                case 120:
                    vouchers["40"] += 1
                    vouchers["50"] += 1
                    vouchers["30"] += 1
                    voucher_number += 3
                    monthly_balance -= 120

                case 110:
                    vouchers["40"] += 2
                    vouchers["30"] += 1
                    voucher_number += 3
                    monthly_balance -= 110

                case 100:
                    vouchers["100"] += 1
                    voucher_number += 1
                    monthly_balance -= 100

                case 90:
                    vouchers["50"] += 1
                    vouchers["40"] += 1
                    voucher_number += 2
                    monthly_balance -= 90

                case 80:
                    vouchers["40"] += 2
                    voucher_number += 2
                    monthly_balance -= 80

                case 70:
                    vouchers["40"] += 1
                    vouchers["30"] += 1
                    voucher_number += 2
                    monthly_balance -= 70

                case 60:
                    vouchers["30"] += 2
                    voucher_number += 2
                    monthly_balance -= 60

                case 50:
                    vouchers["50"] += 1
                    voucher_number += 1
                    monthly_balance -= 50

                case 40:
                    vouchers["40"] += 1
                    voucher_number += 1
                    monthly_balance -= 40

                case 30:
                    vouchers["40"] += 1
                    voucher_number += 1
                    monthly_balance -= 30

    vouchers_list = {}
    for typeof, amount in vouchers.items():
        if amount > 0:
            vouchers_list[typeof] = amount

    print("# You will left with {2} shekels #\n\n".format(voucher_number, vouchers_list, monthly_balance))
    return voucher_number, vouchers_list


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
        print("-" + msg)

    except Exception as e:
        print("Error: {0}".format(e))


if __name__ == "__main__":
    pass
