from aiogram.fsm.state import StatesGroup, State

class Filter(StatesGroup):
    type_filter = State()

class Expense(StatesGroup):
    category = State()
    name = State()
    date = State()
    total = State()

class Expense_Delete(StatesGroup):
    id = State()

class Expense_Edit(StatesGroup):
    category = State()
    name = State()
    date = State()
    total = State()
    id = State()

class Delete_user(StatesGroup):
    id = State()