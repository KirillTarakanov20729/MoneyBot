from aiogram import types


def get_user_start_menu():
    keyboard = [
        [types.InlineKeyboardButton(text="Добавить расход", callback_data="add_expense")],
        [types.InlineKeyboardButton(text="Посмотреть расходы", callback_data="get_expense")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu

def get_user_filter_menu():
    keyboard = [
        [types.InlineKeyboardButton(text="Вывести последние 10 расходов", callback_data="all_expenses")],
        [types.InlineKeyboardButton(text="Вывести расходы за последний месяц", callback_data="expenses_by_month")],
        [types.InlineKeyboardButton(text="Вывести статистику за год", callback_data="expenses_by_year")],
        [types.InlineKeyboardButton(text="Меню", callback_data="menu")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu

def get_user_edit_expense_menu():
    keyboard = [
        [types.InlineKeyboardButton(text="Удалить расход", callback_data="delete_expense")],
        [types.InlineKeyboardButton(text="Изменить расход", callback_data="edit_expense")],
        [types.InlineKeyboardButton(text="Вернуться в меню", callback_data="menu")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu

def get_user_reply_category_menu():
    keyboard = [
        [types.KeyboardButton(text="Еда 🍔"),
         types.KeyboardButton(text="Жилье 🏠"),
         types.KeyboardButton(text="Транспорт 🚘")],

        [types.KeyboardButton(text="Развлечение 🎪"),
         types.KeyboardButton(text="Одежда и обувь 👠"),
         types.KeyboardButton(text="Здоровье и красота 💅")],

        [types.KeyboardButton(text="Образование 📕"),
         types.KeyboardButton(text="Электроника 📱"),
         types.KeyboardButton(text="Подарки 🎁")]
    ]
    reply_markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return reply_markup

def get_exit_user():
    keyboard = [
        [types.InlineKeyboardButton(text="Выйти", callback_data="menu")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu

def get_user_chatGPT_menu():
    keyboard = [
        [types.InlineKeyboardButton(text="Добавить расход", callback_data="add_expense")],
        [types.InlineKeyboardButton(text="Посмотреть расходы", callback_data="get_expense")],
        [types.InlineKeyboardButton(text="Получить совет", callback_data="get_advice")]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu