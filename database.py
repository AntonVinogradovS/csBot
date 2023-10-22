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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sponsor (
            url TEXT
        )
    ''')
async def update_flag2_and_skins_count(user_id):
    # Проверяем текущее значение flag2
    cursor.execute('SELECT flag2 FROM users WHERE user_id = ?', (user_id,))
    current_flag2 = cursor.fetchone()

    if current_flag2 is not None and current_flag2[0] == 0:
        # Если flag2 равен 0, то обновляем его на 1 и увеличиваем skins_count на 1
        cursor.execute('UPDATE users SET flag2 = 1, skins_count = skins_count + 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        return "Количество доступных скинов увеличилось!"
    else:
        return "Вы уже воспользовались этой возможностью"

async def reset_flag2_for_all():
    # Обнуляем столбец flag2 для всех записей
    cursor.execute('UPDATE users SET flag2 = 0')
    conn.commit()

async def count_flag2_equals_1():
    cursor.execute('SELECT COUNT(*) FROM users WHERE flag2 = 1')
    count = cursor.fetchone()[0]
    return count

# Функция для установки ссылки на спонсора
async def set_sponsor_link(url):
    cursor.execute('UPDATE sponsor SET url = ? WHERE rowid = 1', (url,))
    if cursor.rowcount == 0:
        cursor.execute('INSERT INTO sponsor (url) VALUES (?)', (url,))
    conn.commit()

# Функция для получения ссылки на спонсора
async def get_sponsor_link():
    cursor.execute('SELECT url FROM sponsor')
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
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