import asyncio
import logging
from user.handlers.commands import commands_user_router
from user.handlers.expenses import expense_users_router
from user.handlers.callbacks import callbacks_users_router
from user.handlers.messages import messages_user_router
from admin.handlers.callbacks import callbacks_admin_router
from aiogram import Bot, Dispatcher
from datebase.datebase_users import create_table_users
from datebase.datebase_expenses import create_table_expenses_user
from datebase.datebase_info_user import create_table_info
from dotenv import load_dotenv
import os

async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    await create_table_users()
    await create_table_expenses_user()
    await create_table_info()
    dp.include_routers(callbacks_admin_router, callbacks_users_router, expense_users_router, commands_user_router, messages_user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
