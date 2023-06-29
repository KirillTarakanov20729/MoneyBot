from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from datebase import datebase_expenses, datebase_users
from aiogram.fsm.context import FSMContext
from states.states import Delete_user

callbacks_admin_router = Router()

@callbacks_admin_router.callback_query(F.data == 'users')
async def get_users(callback: CallbackQuery):
    users = await datebase_users.select_all_users()
    users_list = '\n'.join([f'{user[0]} - {user[1]} - {user[2]}' for user in users])
    await callback.message.answer(f'Список пользователей:\n{users_list}')


@callbacks_admin_router.callback_query(F.data == 'all_users_expenses')
async def get_users_expenses(callback: CallbackQuery):
    expenses = await datebase_expenses.get_all_expense_admin()
    expenses_list = '\n'.join([f'{expense[0]} - {expense[1]} - {expense[2]} - {expense[3]} - {expense[4]}' for expense in expenses])
    await callback.message.answer(f'Список расходов: \n{expenses_list}')

@callbacks_admin_router.callback_query(F.data == 'delete_user')
async def get_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите id")
    await state.set_state(Delete_user.id)

@callbacks_admin_router.message(Delete_user.id)
async def delete_user(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    id = await state.get_data()
    await datebase_users.delete_user(id['id'])
    await message.answer(f"Пользователь с id {id['id']} удален")