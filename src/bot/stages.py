from telebot.asyncio_handler_backends import State, StatesGroup


class RegistrationStates(StatesGroup):
    contact = State()
    register_sign = State()
    car_year = State()
    message = State()


class CarIsBlockedStates(StatesGroup):
    register_sign = State()
    message = State()


class CarBlockesStates(StatesGroup):
    register_sign = State()
    message = State()
