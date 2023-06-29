from aiogram import Router, F
from aiogram.types import CallbackQuery
from user.keyboards.user_keyboard import get_user_start_menu
from datebase.datebase_info_user import get_user_info_info
from user.utils.utils import generate_text

callbacks_users_router = Router()

@callbacks_users_router.callback_query(F.data == "menu")
async def get_menu(callback: CallbackQuery):
    await callback.message.answer("Что теперь хотите делать?", reply_markup=get_user_start_menu())

@callbacks_users_router.callback_query(F.data == "get_advice")
async def get_advice(callback: CallbackQuery):
    user_id = callback.from_user.id
    info = await get_user_info_info(user_id)
    await callback.message.answer('ИИ думает, что ответить, пожалуйста, ждите')
    advice = await generate_text(str(info))
    await callback.message.answer(advice, reply_markup=get_user_start_menu())