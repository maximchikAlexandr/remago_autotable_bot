from telebot import types

from src.bot.constants import (
    CANCEL_TEXT,
    SIGN_IN_TEXT,
    MY_CAR_BLOCKES_TEXT,
    MY_CAR_IS_BLOCKED_TEXT,
)


def get_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=CANCEL_TEXT))
    return keyboard


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=MY_CAR_BLOCKES_TEXT))
    keyboard.add(types.KeyboardButton(text=MY_CAR_IS_BLOCKED_TEXT))
    return keyboard


def get_registration_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=SIGN_IN_TEXT))
    return keyboard


def get_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Поделиться данными", request_contact=True)
    keyboard.add(button_phone)
    return keyboard
