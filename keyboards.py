from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

from database import *

def generate_phone_button():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Отправить свой контакт", request_contact=True)]
        ], resize_keyboard=True
    )

def generate_main_button():
    categories = get_all_categories()
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in categories:
        bnt = InlineKeyboardButton(text=category[1], callback_data=f"category_{category[0]}")
        buttons.append(bnt)
    markup.add(*buttons)
    return markup

def confirmation_order():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❎ Отклонить")]
        ], resize_keyboard=True, row_width=2
    )
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="⬅ Назад")]
        ], resize_keyboard=True
    )
