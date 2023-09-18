import os

from dotenv import load_dotenv
from telebot import TeleBot, custom_filters, types
from telebot.storage import StateMemoryStorage

from src.bot.constants import (
    CANCEL_TEXT,
    MY_CAR_BLOCKES_TEXT,
    MY_CAR_IS_BLOCKED_TEXT,
    SIGN_IN_TEXT,
)
from src.bot.filters import (
    ExistingRegisterSignFilter,
    ExistingUsersFilter,
    ValidCarYearFilter,
    ValidRegisterSignFilter,
)
from src.bot.keyboards import (
    get_cancel_keyboard,
    get_contact_keyboard,
    get_main_keyboard,
    get_registration_keyboard,
)
from src.bot.stages import CarBlockesStates, CarIsBlockedStates, RegistrationStates
from src.db.settings import EngineDB
from src.facades import UserFacade

user_facade = UserFacade(engine_db=EngineDB())


load_dotenv(".env")

state_storage = StateMemoryStorage()
TOKEN: str = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TOKEN, parse_mode=None, state_storage=state_storage)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Для продолжения работы нажмите кнопку 'Зарегистрироваться':",
        reply_markup=get_registration_keyboard(),
    )


# Register a new user
@bot.message_handler(func=lambda message: message.text == SIGN_IN_TEXT)
@bot.message_handler(commands=["sign_in"])
def start_registration(message):
    if user_facade.is_existing_user(message.chat.id):
        bot.send_message(message.chat.id, "Вы уже зарегистрированы")
    else:
        bot.set_state(message.from_user.id, RegistrationStates.contact, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Для регистрации нам нужна информация о Вас. Для этого нажмите 'Поделиться данными'.",
            reply_markup=get_contact_keyboard(),
        )


@bot.message_handler(content_types=["contact"], state=RegistrationStates.contact)
def get_contact_for_registration(message):
    if message.contact is not None:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            for field in ("phone_number", "first_name", "last_name", "user_id"):
                data[field] = getattr(message.contact, field)
        bot.set_state(
            message.from_user.id, RegistrationStates.register_sign, message.chat.id
        )
        bot.send_message(
            message.chat.id,
            "Введите номер своего автомобиля ",
            reply_markup=types.ReplyKeyboardRemove(),
        )


@bot.message_handler(
    state=RegistrationStates.register_sign,
    is_valid_register_sign=True,
    is_existing_register_sign=False,
    is_existing_user=False,
)
def get_register_sign_for_registration(message):
    bot.set_state(message.from_user.id, RegistrationStates.car_year, message.chat.id)
    bot.send_message(message.chat.id, "Введите год своего автомобиля:")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["register_sign"] = message.text


@bot.message_handler(state=RegistrationStates.car_year, is_valid_car_year=True)
def save_new_user(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        user_facade.create(
            user_id=data["user_id"],
            phone_number=data["phone_number"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            register_sign=data["register_sign"],
            car_year=message.text,
        )

    bot.delete_state(message.from_user.id, message.chat.id)
    if user_facade.is_existing_user(message.chat.id):
        bot.send_message(
            message.chat.id,
            "Вы успешно зарегистрированы",
            reply_markup=get_main_keyboard(),
        )
    else:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при регистрации",
            reply_markup=get_registration_keyboard(),
        )


# sent message to other users
@bot.message_handler(
    state="*", content_types=["text"], func=lambda message: message.text == CANCEL_TEXT
)
def cancel(message):
    bot.send_message(
        message.chat.id, "Действие отменено", reply_markup=get_main_keyboard()
    )
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(
    func=lambda message: message.text == MY_CAR_IS_BLOCKED_TEXT, is_existing_user=True
)
@bot.message_handler(commands=["my_car_is_blocked"], is_existing_user=True)
def my_car_is_blocked(message):
    bot.send_message(
        message.chat.id,
        "Мы постараемся помочь Вам с этой проблемой. "
        "Для начала введите номер автомобиля, который Вас подпёр:",
        reply_markup=get_cancel_keyboard(),
    )
    bot.set_state(
        message.from_user.id, CarIsBlockedStates.register_sign, message.chat.id
    )


@bot.message_handler(
    func=lambda message: message.text == MY_CAR_BLOCKES_TEXT, is_existing_user=True
)
@bot.message_handler(commands=["my_car_blockes"], is_existing_user=True)
def my_car_blockes(message):
    bot.send_message(
        message.chat.id,
        "Мы постараемся помочь Вам с этой проблемой. "
        "Для начала введите номер автомобиля, который Вы подпёрли:",
        reply_markup=get_cancel_keyboard(),
    )
    bot.set_state(message.from_user.id, CarBlockesStates.register_sign, message.chat.id)


@bot.message_handler(
    state=[CarIsBlockedStates.register_sign, CarBlockesStates.register_sign],
    is_valid_register_sign=True,
    is_existing_user=True,
)
def find_other_user(message):
    state = bot.get_state(message.from_user.id, message.chat.id)
    if state == "CarIsBlockedStates:register_sign":
        bot.set_state(message.from_user.id, CarIsBlockedStates.message, message.chat.id)
    elif state == "CarBlockesStates:register_sign":
        bot.set_state(message.from_user.id, CarBlockesStates.message, message.chat.id)

    bot.send_message(message.chat.id, "Ищем пользователей")
    try:
        other_user_data = user_facade.get_user_data_by_register_sign(message.text)
    except AttributeError:
        bot.send_message(
            message.chat.id,
            "Пользователь с таким номером автомобиля не зарегистрирован",
        )
        bot.delete_state(message.from_user.id, message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        f"Введите сообщение для пользователя {other_user_data['last_name']} {other_user_data['first_name']} "
        f"{other_user_data['phone_number']}. Пожалуйста, уважайте других пользователей:",
    )
    user_data = user_facade.get_user_data_by_user_id(message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["other_user_id"] = other_user_data["user_id"]
        data["phone_number"] = user_data["phone_number"]
        data["first_name"] = user_data["first_name"]
        data["last_name"] = user_data["last_name"]


@bot.message_handler(
    state=[CarIsBlockedStates.message, CarBlockesStates.message], is_existing_user=True
)
def message_to_other_user(message):
    state = bot.get_state(message.from_user.id, message.chat.id)
    first_row = ""
    if state == "CarIsBlockedStates:message":
        first_row = "Внимание, Вы подпёрли автомобиль!"
    elif state == "CarBlockesStates:message":
        first_row = "Ваш автомобиль подпёрли! "

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.send_message(
            data["other_user_id"],
            f"{first_row} \n"
            f"Сообщение от пользователя {data['last_name']} {data['first_name']} "
            f"{data['phone_number']}: '{message.text}'.",
        )

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Ваше сообщение успешно отправлено пользователю",
        reply_markup=get_main_keyboard(),
    )


# Check incorrect dates
@bot.message_handler(
    commands=["my_car_is_blocked", "my_car_blockes"], is_existing_user=False
)
def not_existing_user(message):
    bot.send_message(message.chat.id, "Для данного действия нужно зарегистрироваться.")


@bot.message_handler(state=RegistrationStates.car_year, is_valid_car_year=False)
def car_year_incorrect(message):
    bot.send_message(message.chat.id, "Год автомобиля введен некорректно")


@bot.message_handler(
    state=RegistrationStates.register_sign, is_existing_register_sign=True
)
def existing_register_sign(message):
    bot.send_message(message.chat.id, "Данный номер автомобиля уже зарегистрирован")


@bot.message_handler(
    state=[
        CarIsBlockedStates.register_sign,
        CarBlockesStates.register_sign,
        RegistrationStates.register_sign,
    ],
    is_valid_register_sign=False,
)
def register_sign_incorrect(message):
    bot.send_message(message.chat.id, "Номер автомобиля введен некорректно")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(ValidRegisterSignFilter())
bot.add_custom_filter(ValidCarYearFilter())
bot.add_custom_filter(ExistingUsersFilter(user_facade))
bot.add_custom_filter(ExistingRegisterSignFilter(user_facade))

bot.set_my_commands(
    [
        types.BotCommand(command="my_car_blockes", description=MY_CAR_BLOCKES_TEXT),
        types.BotCommand(
            command="my_car_is_blocked", description=MY_CAR_IS_BLOCKED_TEXT
        ),
    ]
)
