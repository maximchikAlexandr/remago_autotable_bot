import datetime

from telebot.asyncio_filters import SimpleCustomFilter

from src.bot.utils.formatters import to_format_sign
from src.bot.utils.validators import is_valid_register_sign


class ValidRegisterSignFilter(SimpleCustomFilter):
    key = "is_valid_register_sign"

    async def check(self, message):
        register_sign = to_format_sign(message.text)
        return is_valid_register_sign(register_sign)


class ValidCarYearFilter(SimpleCustomFilter):
    key = "is_valid_car_year"

    async def check(self, message):
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

    async def check(self, message):
        result = await self.facade.is_existing_user(message.chat.id)
        return result


class ExistingRegisterSignFilter(SimpleCustomFilter):
    key = "is_existing_register_sign"

    def __init__(self, facade=None) -> None:
        self.facade = facade

    async def check(self, message):
        result = await self.facade.is_existing_register_sign(message.text)
        return result
