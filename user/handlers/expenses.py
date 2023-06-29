from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from datebase import datebase_expenses, datebase_info_user
from user.keyboards.user_keyboard import get_user_filter_menu, get_user_start_menu, get_user_edit_expense_menu, get_user_reply_category_menu, get_exit_user, get_user_chatGPT_menu
from states.states import Filter, Expense, Expense_Delete, Expense_Edit
from user.utils.utils import check, get_list_categories, get_name_of_month

import datetime
from aiogram.types import ReplyKeyboardRemove

expense_users_router = Router()

@expense_users_router.callback_query(F.data == 'add_expense')
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите категорию", reply_markup=get_user_reply_category_menu())
    await state.set_state(Expense.category)

@expense_users_router.message(Expense.category)
async def get_name(message: Message, state: FSMContext):
    if await check(message):
        await state.update_data(category=message.text)
        await message.answer("Введите название", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Expense.name)
    else:
        await message.answer('Такой категории нет, выберите категорию с клавиатуры', reply_markup=get_user_reply_category_menu())
        await state.set_state(Expense.category)

@expense_users_router.message(Expense.name)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите дату покупки', reply_markup=get_exit_user())
    await state.set_state(Expense.date)

@expense_users_router.message(Expense.date)
async def get_total(message: Message, state: FSMContext):
    try:
        date = datetime.datetime.strptime(message.text, '%d/%m/%Y').date()
    except ValueError:
        await message.answer('Неправильный формат даты. Введите дату в формате ДД/ММ/ГГГГ')
        return
    await state.update_data(date=date)
    await message.answer('Введите сумму', reply_markup=get_exit_user())
    await state.set_state(Expense.total)

@expense_users_router.message(Expense.total)
async def add_expense(message: Message, state: FSMContext):
    await state.update_data(total=message.text)
    data = await state.get_data()
    category = data.get('category')
    name = data.get('name')
    date = data.get('date')
    total = data.get('total')
    user_id = message.from_user.id
    await datebase_expenses.insert_expense_user(user_id, category, name, date, total)
    await message.answer(f"Добавлена трата:\nКатегория: {category}\nНазвание: {name}\nДата: {date}\nСумма: {total}")
    await message.answer('Что теперь хотите сделать?', reply_markup=get_user_start_menu())
    await state.clear()

@expense_users_router.callback_query(F.data == "get_expense")
async def get_filter_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Что именно вас интересует?", reply_markup=get_user_filter_menu())
    await state.set_state(Filter.type_filter)

@expense_users_router.callback_query(Filter.type_filter)
async def filter_expenses(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(filter_type=callback.data)
    filter_type = await state.get_data()
    if filter_type['filter_type'] == 'all_expenses':
        user_id = callback.from_user.id
        all_expense = await datebase_expenses.get_last_10_expenses_user(user_id)
        if all_expense:
            expenses_str = '\n'.join([f"{expense[4]} вы потратили {expense[5]} руб на {expense[3]}, номер расхода - {expense[0]}" for expense in all_expense])
            await callback.message.answer(f'Ваши последние 10 расходов:\n{expenses_str}')
            await callback.message.answer('Что теперь хотите сделать?', reply_markup=get_user_edit_expense_menu())
            await state.clear()
        else:
            await callback.message.answer("Пока что у тебя нет расходов.", reply_markup=get_user_start_menu())
            await state.clear()
    elif filter_type['filter_type'] == 'expenses_by_month':
        user_id = callback.from_user.id
        current_month = datetime.datetime.now().month
        current_month_str = '{:02d}'.format(current_month)
        current_year = datetime.datetime.now().year
        categories = await get_list_categories()
        info = ""

        sum = 0
        info += f"Вот ваши траты за месяц: \n"
        for category in categories:
            total = await datebase_expenses.get_total_of_category_user(category, current_year, current_month_str,user_id)
            if total[0] is not None:
                info += f"•{category}: {total[0]} руб\n"
                sum += total[0]
            else:
                info += f"•{category} : 0 руб\n"
        info += f"\nВсего в этом месяце вы потратили {sum} руб"

        total = 0
        if current_month == 1:
            num_months = 1
        else:
            num_months = current_month - 1
        for month in range(1, current_month):
            month = '{:02d}'.format(month)
            total_month = await datebase_expenses.get_total_of_month_user(user_id, current_year, month)
            if total_month[0] is not None:
                total += total_month[0]
        if num_months == 0:
            average = total
        else:
            average = total / num_months

        if int(average) < sum:
            info += (f"\nВ этом месяце вы потратили на {sum - average} руб больше, чем обычно")
        if int(average) > sum:
            info += (f"\nВ этом месяце вы потратили на {average - sum} руб меньше, чем обычно")
        if int(average) == sum:
            info += (f"\nВ этом месяце вы потратили столько же, сколько обычно")

        await callback.message.answer(info, reply_markup=get_user_start_menu())
    elif filter_type['filter_type'] == 'expenses_by_year':
        user_id = callback.from_user.id
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        categories = await get_list_categories()
        info = ""
        total_year = 0
        info += f"Вот ваши траты за год: \n"
        for month in range(1, current_month + 1):
            month = '{:02d}'.format(month)
            total_month = await datebase_expenses.get_total_of_month_user(user_id, current_year, month)
            month_name = await get_name_of_month(int(month))
            if total_month[0] is not None:
                info += f"\n{month_name} - {total_month[0]}"
                total_year += total_month[0]
            else:
                info += f"\n{month_name} - 0"
                total_year += 0
        info += f"\nВсего за год вы потратили - {total_year}\n"
        total_category_year = 0
        for category in categories:
            for month in range(1, current_month + 1):
                month = '{:02d}'.format(month)
                total_category_month = await datebase_expenses.get_total_of_category_user(category, current_year, month, user_id)
                if total_category_month[0] is not None:
                    total_category_year += total_category_month[0]
                else:
                    total_category_year += 0
            info += f"\nНа {category} вы потратили {total_category_year}"
            total_category_year = 0
        await callback.message.answer(info)
        await datebase_info_user.update_user_info_info(user_id, info)
        await callback.message.answer("Что теперь хотите сделать?", reply_markup=get_user_chatGPT_menu())

@expense_users_router.callback_query(F.data == "delete_expense")
async def get_id_expense_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите номер расхода, который хотите удалить", reply_markup=get_exit_user())
    await state.set_state(Expense_Delete.id)

@expense_users_router.message(Expense_Delete.id)
async def delete_expense(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    expense_id = await state.get_data()
    user_id = message.from_user.id
    await datebase_expenses.delete_expense_user(user_id,expense_id['id'])
    await state.update_data()
    await message.answer(f"Расход с номером {expense_id['id']} удален", reply_markup=get_user_start_menu())

@expense_users_router.callback_query(F.data == "edit_expense")
async def get_id_expense_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите номер расхода, который хотите изменить", reply_markup=get_exit_user())
    await state.set_state(Expense_Edit.id)

@expense_users_router.message(Expense_Edit.id)
async def get_category_expense_edit(message: Message, state: FSMContext):
    await state.update_data(expense_id=message.text)
    await message.answer("Выберите категорию", reply_markup=get_user_reply_category_menu())
    await state.set_state(Expense_Edit.category)

@expense_users_router.message(Expense_Edit.category)
async def get_name_category_edit(message: Message, state: FSMContext):
    if await check(message):
        await state.update_data(category=message.text)
        await message.answer("Введите название", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Expense_Edit.name)
    else:
        await message.answer('Такой категории нет, выберите категорию с клавиатуры', reply_markup=get_user_reply_category_menu())
        await state.set_state(Expense_Edit.category)

@expense_users_router.message(Expense_Edit.name)
async def get_date_expense_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите дату покупки', reply_markup=get_exit_user())
    await state.set_state(Expense_Edit.date)

@expense_users_router.message(Expense_Edit.date)
async def get_total_expense_edit(message: Message, state: FSMContext):
    try:
        date = datetime.datetime.strptime(message.text, '%d/%m/%Y').date()
    except ValueError:
        await message.answer('Неправильный формат даты. Введите дату в формате ДД/ММ/ГГГГ')
        return
    await state.update_data(date=date)
    await message.answer('Введите сумму', reply_markup=get_exit_user())
    await state.set_state(Expense_Edit.total)

@expense_users_router.message(Expense_Edit.total)
async def add_expense(message: Message, state: FSMContext):
    await state.update_data(total=message.text)
    data = await state.get_data()
    expense_id = data.get('expense_id')
    category = data.get('category')
    name = data.get('name')
    date = data.get('date')
    total = data.get('total')
    user_id = message.from_user.id
    await datebase_expenses.edit_expense_user(user_id,expense_id, category, name, date, total)
    await message.answer(f"Обновленная трата:\n Категория: {category}\nназвание: {name}\nдата: {date}\ncумма: {total}")
    await message.answer('Что теперь хотите сделать?', reply_markup=get_user_start_menu())
    await state.clear()
