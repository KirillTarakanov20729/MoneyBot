import aiosqlite

async def create_table_expenses_user():
    async with aiosqlite.connect('expenses.sql') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS expenses '
                         '(id INTEGER PRIMARY KEY,'
                         'user_id INTEGER, '
                         'category TEXT,'
                         'name TEXT, '
                         'date DATE, '
                         'total INTEGER)')
        await db.commit()

async def insert_expense_user(user_id, category, name, date, total):
    async with aiosqlite.connect('expenses.sql') as db:
        await db.execute('INSERT INTO expenses (user_id, category, name, date, total) VALUES (?,?,?,?,?)',
                         (user_id, category, name, date, total))
        await db.commit()

async def get_all_expense_admin():
    async with aiosqlite.connect('expenses.sql') as db:
        cursor = await db.execute('SELECT * FROM expenses')
        expenses = await cursor.fetchall()
    return expenses

async def get_last_10_expenses_user(user_id):
    async with aiosqlite.connect('expenses.sql') as db:
        cursor = await db.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 10', (user_id,))
        expenses = await cursor.fetchall()
    return expenses

async def get_expense_for_month_user(year, month, user_id):
    async with aiosqlite.connect('expenses.sql') as db:
        cursor = await db.execute("SELECT * FROM expenses WHERE user_id = (?) AND date LIKE '{}-{}%'".format(year, month), (user_id,))
        results = await cursor.fetchall()
    return results

async def delete_expense_user(user_id, expense_id):
    async with aiosqlite.connect('expenses.sql') as db:
        await db.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
        await db.commit()

async def edit_expense_user(user_id, expense_id, category, name, date, total):
    async with aiosqlite.connect('expenses.sql') as db:
        await db.execute("UPDATE expenses SET category = ?, name = ?, date = ?, total = ? WHERE id = ? AND user_id = ?", (category, name, date, total, expense_id, user_id))
        await db.commit()

async def get_total_of_category_user(category, year, month, user_id):
    async with aiosqlite.connect('expenses.sql') as db:
        cursor = await db.execute("SELECT SUM(total) FROM expenses WHERE category = (?) AND user_id = (?) AND date LIKE '{}-{}%'".format(year, month), (category, user_id))
        total = await cursor.fetchone()
    return total

async def get_total_of_month_user(user_id, year, month):
    async with aiosqlite.connect('expenses.sql') as db:
        query = "SELECT SUM(total) FROM expenses WHERE user_id = ? AND date LIKE ?"
        params = (user_id, f"{year}-{month}%")
        cursor = await db.execute(query, params)
        total = await cursor.fetchone()
    return total