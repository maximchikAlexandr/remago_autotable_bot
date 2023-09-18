import datetime

from telebot import SimpleCustomFilter


class ValidRegisterSignFilter(SimpleCustomFilter):
    key = "is_valid_register_sign"

    def check(self, message):
        return "1" in str(message.text)


class ValidCarYearFilter(SimpleCustomFilter):
    key = "is_valid_car_year"

    def check(self, message):
        current_year = datetime.datetime.now().year
        return (
            message.text.isdigit()
            and int(message.text) >= 1886
            and int(message.text) <= current_year
        )


class ExistingUsersFilter(SimpleCustomFilter):
    key = "is_existing_user"

    def __init__(self, facade=None) -> None:
        self.facade = facade

    def check(self, message):
        return self.facade.is_existing_user(message.chat.id)


class ExistingRegisterSignFilter(SimpleCustomFilter):
    key = "is_existing_register_sign"

    def __init__(self, facade=None) -> None:
        self.facade = facade

    def check(self, message):
        return self.facade.is_existing_register_sign(message.text)
