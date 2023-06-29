import aiosqlite

async def create_table_users():
    async with aiosqlite.connect('users.sql') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS users '
                         '(id INTEGER PRIMARY KEY, '
                         'user_id INTEGER, '
                         'role TEXT)')
        await db.commit()


async def insert_user(user_id, role):
    async with aiosqlite.connect('users.sql') as db:
        await db.execute('INSERT INTO users (user_id, role) VALUES (?,?)', (user_id, role))
        await db.commit()

async def select_all_users():
    async with aiosqlite.connect('users.sql') as db:
        cursor = await db.execute('SELECT * FROM users')
        users = await cursor.fetchall()
    return users

async def check_user_id(user_id):
    async with aiosqlite.connect('users.sql') as db:
        cursor = await db.execute('SELECT * FROM users WHERE (user_id) = (?)', (user_id,))
        user = await cursor.fetchone()
    return user

async def check_user_role(user_id):
    async with aiosqlite.connect('users.sql') as db:
        cursor = await db.execute('SELECT role FROM users WHERE (user_id) = (?)', (user_id,))
        role = await cursor.fetchone()
    return role

async def delete_user(id):
    async with aiosqlite.connect('users.sql') as db:
        await db.execute("DELETE FROM users WHERE id = ?", (id))
        await db.commit()