from wrappers import webdriver_wrapper
import ten_bis
from utils import parse_config
from datetime import datetime
import calendar
import time


class MainFlow:
    def __init__(self):
        self.logger = parse_config.set_logger(file_name="output.txt", level="INFO")
        print("starting...")
        self.config = parse_config.get_configurations(self.logger)
        self.web_driver_obj = webdriver_wrapper.WebDriverObject(self.config.get("browser"))
        self.monthly_balance = 0
        self.is_logged_in = False
        self.phone = self.config.get("input_funds").get("phone")
        with open('user_input.txt', 'w') as f:
            f.write('')

    @staticmethod
    def is_last_day():
        currentday = datetime.now().day
        currentyear = datetime.now().year
        currentMonth = datetime.now().month
        last_day = calendar.monthrange(currentyear, currentMonth)[1]
        if currentday == last_day:
            return True

    def get_balance(self):
        ten_bis.send_massage("מייד אגיד לך, \nכמה רגעים...", self.phone)

        while True:
            monthly_balance = ten_bis.get_balance_from_ten_bis(self.web_driver_obj, self.config, self.is_logged_in)
            if not monthly_balance:
                self.is_logged_in = False
            else:
                break

        self.monthly_balance = monthly_balance
        ten_bis.send_massage("😏היתרה שלך עד סוף החודש: *{0}*".format(str(self.monthly_balance)), self.phone)

    def buy_vouchers(self):
        ten_bis.send_massage("אין בעיה, אני אדאג לך :)", self.phone)
        if not self.monthly_balance:
            self.get_balance()
        if int(self.monthly_balance) > 30:
            vouchers_number, vouchers_list = ten_bis.number_of_voucher(self.monthly_balance)
            message = ten_bis.printv(vouchers_list)
            ten_bis.send_massage(message, self.phone)
            ten_bis.send_massage("נא אשר את הקניה:\n\n@ (1) - אשר\n@ (2) - בטל\n-> ", self.phone)

            while True:
                with open('user_input.txt', 'r+') as f:
                    option = f.read()
                    if option:
                        if "1" in option:
                            ten_bis.buy_voucher(vouchers_list, self.web_driver_obj, self.phone)
                            ten_bis.send_massage("כל הווצ'רים יופיעו במייל שלך :)")
                            break

                        elif "2" in option:
                            ten_bis.send_massage("בוטל!", self.phone)
                            break

                        else:
                            ten_bis.send_massage("רשום 1 או 2", self.phone)
                            f.write('')

        else:
            ten_bis.send_massage("אין לך מספיק כסף לוואצ'רים :(\nיוצא", self.phone)

    def schedule_buy(self):
        ten_bis.send_massage('אין בעיה, ביום האחרון של החודש אזכיר לך לפני שאקנה :)\nנהיה בקשר...', self.phone)
        while True:
            if self.is_last_day():
                ten_bis.send_massage('היום זה היום! בוא ננצל את מה שנשאר!', self.phone)
                self.buy_vouchers()
                ten_bis.send_massage('נהיה בקשר בעוד חודש, שמחתי לעזור', self.phone)
                break
            else:
                time.sleep(1800)
        self.__exit__()

    def __exit__(self):
        self.web_driver_obj.close_browser()
        print("finished")


if __name__ == "__main__":
    start = MainFlow()
    print(start.get_balance())
    start.__exit__()
