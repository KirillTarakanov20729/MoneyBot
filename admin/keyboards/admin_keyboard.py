from aiogram import types

def get_admin_start_menu():
    keyboard = [
        [types.InlineKeyboardButton(text="Добавить расход", callback_data="add_expense")],
        [types.InlineKeyboardButton(text="Посмотреть расходы", callback_data="get_expense")],
        [types.InlineKeyboardButton(text="Вывести пользователей", callback_data="users")],
        [types.InlineKeyboardButton(text="Вывести все расходы", callback_data="all_users_expenses")],
        [types.InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu