import sqlite3

def sql_start():
    global conn, cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if conn:
        print("Data base connected OK!")
    # Создание таблицы для хранения информации о пользователях
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referral_id INTEGER,
            skins_count INTEGER,
            skins_received INTEGER,
            friends_invited INTEGER,
            flag1 INTEGER,
            flag2 INTEGER
        )
    ''')
    conn.commit()

# Функция для добавления нового пользователя
async def add_user(user_id=0, referral_id = 0, skins_count=0, skins_received=0, friends_invited=0, flag1=0,flag2=0):
    cursor.execute('''
        INSERT INTO users (user_id, referral_id, skins_count, skins_received, friends_invited, flag1,flag2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, referral_id, skins_count, skins_received, friends_invited,flag1,flag2))
    conn.commit()

# Функция для получения информации о пользователе по его ID
async def get_user_by_id(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()


# Функция для обновления количества полученных скинов и их остаток
async def update_skins_received(user_id, count, received):
    cursor.execute('UPDATE users SET skins_count = ?, skins_received = ? WHERE user_id = ?', (count, received, user_id))
    conn.commit()

# Функция для обновления количества друзей и колво доступных скинов, приведенных в бота
async def update_friends_invited(user_id, countSckin, countFriend ):
    cursor.execute('UPDATE users SET friends_invited = ?, skins_count = ? WHERE user_id = ?', (countFriend, countSckin, user_id))
    conn.commit()

async def update_flag1(user_id, count):
    cursor.execute('UPDATE users SET flag1 = ? WHERE user_id = ?', (count, user_id))
    conn.commit()

async def update_flag2(user_id, count):
    cursor.execute('UPDATE users SET flag2 = ? WHERE user_id = ?', (count, user_id))
    conn.commit()