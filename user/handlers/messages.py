from aiogram import Router
from aiogram.types import Message

messages_user_router = Router()

@messages_user_router.message()
async def get_text(message: Message):
    await message.answer("Я пока что не знаю такого, напиши /start")