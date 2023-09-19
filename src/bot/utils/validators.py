import re

from src.bot.utils.formatters import to_format_sign


def _is_matches_the_pattern(pattern: str, input_str: str) -> bool:
    match = re.match(pattern, input_str)
    return True if match else False


def is_valid_register_sign(sign: str) -> bool:
    pattern = r"^([0-9]|E|I)[0-9]{3}[ABEIKMHOPCTX]{2}[0-7]$"
    return _is_matches_the_pattern(pattern, sign)


def check_invalid_register_sign(sign: str) -> str:
    sign = to_format_sign(sign)
    if len(sign) != 7:
        return "⛔️ Регистрационный знак автомобиля введен некорректно." \
               "Регистрационный знак должен содержать:\n" \
               "- номер в формате '0000' или 'Е000' ('I000') - для электроавтомобилей, где 0 - это " \
               "цифры от 0 до 9\n" \
               "- серии в формате 'АА', где А - это буквы ABEIKMHOPCTX\n" \
               "- код региона - цифра от 0 до 7"

    number, series, code = sign[:4], sign[4:6], sign[6:]
    number_pattern = r"([0-9]|E|I)[0-9]{3}"
    series_pattern = r"[ABEIKMHOPCTX]{2}"
    code_pattern = r"[0-7]"

    messages = []

    if not _is_matches_the_pattern(number_pattern, number):
        message = f"⛔️ Номер регистрационного знака '{number}' некорректен. Номер должен " \
                  f"начинаться " \
                  f"с цифры или буквы E (I) - для электроавтомобилей. Далее должны следовать 3 " \
                  f"цифры "
        messages.append(message)

    if not _is_matches_the_pattern(series_pattern, series):
        message = f"⛔️ Серия регистрационного знака '{series}' некорректна. " \
                  f"Серия состоять из 2 букв. Разрешенные буквы: ABEIKMHOPCTX"
        messages.append(message)

    if not _is_matches_the_pattern(code_pattern, code):
        message = f"⛔️ Код регистрационного знака '{code}' некорректен. " \
                  f"Разрешенные коды - это цифры от 0 до 7 включительно"
        messages.append(message)

    return "\n\n".join(messages)
