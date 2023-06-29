from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from user.keyboards.user_keyboard import get_user_start_menu
from admin.keyboards.admin_keyboard import get_admin_start_menu

from datebase import datebase_users, datebase_info_user


commands_user_router = Router()

@commands_user_router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет, меня зовут Money и я помогу тебе стать финансово грамотным. Для вызова меню напиши /help')
    user_id = message.from_user.id
    user = await datebase_users.check_user_id(user_id)
    if user is None:
        if user_id == 588633023:
            await datebase_users.insert_user(user_id, 'Admin')
        else:
            await datebase_users.insert_user(user_id, 'Usual')
    info = await datebase_info_user.check_table(user_id)
    if info is None:
        await datebase_info_user.insert_user_info(user_id)




@commands_user_router.message(Command('help'))
async def help(message: Message):
    user_id = message.from_user.id
    role_tuple = await datebase_users.check_user_role(user_id)
    role = ''.join(role_tuple)
    if role == 'Usual':
        await message.answer('Выберите действие', reply_markup=get_user_start_menu())
    else:
        await message.answer('Выберите действие', reply_markup=get_admin_start_menu())