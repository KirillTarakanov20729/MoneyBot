import aiosqlite

async def create_table_info():
    async with aiosqlite.connect("info.sql") as db:
        await db.execute('CREATE TABLE IF NOT EXISTS info'
                         '(id INTEGER PRIMARY KEY,'
                         'user_id INTEGER,'
                         'info TEXT)')
        await db.commit()

async def check_table(user_id):
    async with aiosqlite.connect('info.sql') as db:
        cursor = await db.execute('SELECT * FROM info where user_id = ?', (user_id,))
        result = await cursor.fetchone()
    return result

async def insert_user_info(user_id):
    async with aiosqlite.connect("info.sql") as db:
        await db.execute('INSERT INTO info (user_id) VALUES (?)', (user_id,))
        await db.commit()

async def update_user_info_info(user_id, info: str):
    async with aiosqlite.connect("info.sql") as db:
        await db.execute('UPDATE info SET info = ? WHERE user_id = ?', (info, user_id))
        await db.commit()

async def get_user_info_info(user_id):
    async with aiosqlite.connect('info.sql') as db:
        cursor = await db.execute('SELECT info FROM info WHERE user_id = ?', (user_id,))
        info = await cursor.fetchone()
    return info