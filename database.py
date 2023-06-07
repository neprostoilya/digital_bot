import sqlite3


def create_user_table():
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT
    );
    ''')
    database.commit()
    database.close()


def create_categories_table():
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) NOT NULL UNIQUE,
        category_time VARCHAR NOT NULL 
    );
    ''')

    database.commit()
    database.close()
		
def insert_categories():
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name, category_time) VALUES
    ('Ресайз баннера', 10),
    ('3D модель', 10),
    ('Моушен-ролик', 8),
    ('Сайт без логики', 15),
    ('Сайт с логикой', 30),
    ('Визитка', 3),
    ('Айдентика', 50)
    ''')
    database.commit()
    database.close()
    
def select_user(chat_id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchall()
    database.close()
    return user

def first_register_user(chat_id, full_name):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO users(telegram_id, full_name) VALUES (?,?)  
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def update_user_to_finish_register(phone, chat_id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET phone = ? WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories

def get_hours_categories(id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT  category_time FROM categories
    WHERE category_id = ?;
    ''', (id,))
    hours = cursor.fetchone()
    database.close()
    return hours

def get_name_categories(id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT category_name FROM categories
    WHERE category_id = ?;   
    ''', (id,))
    name = cursor.fetchone()
    database.close()
    return name

def create_order():
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_order(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT,
        name_category VARCHAR,
        price TEXT,
        hours TEXT,
        days TEXT,
        week TEXT
    );
    ''')
    database.commit()
    database.close()

def insert_order(name, chat_id, phone, name_category, price, hours, days, week):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO user_order(name, telegram_id, phone, name_category, price, hours, days, week) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, chat_id, phone, name_category, price, hours, days, week))
    database.commit()
    database.close()

def get_order(chat_id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''   
    SELECT * FROM user_order
    WHERE telegram_id = ?;
    ''', (chat_id,))
    order = cursor.fetchall()
    database.close()
    return order

def delete_order(id):
    database = sqlite3.connect('library/telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''   
    DELETE FROM user_order
    WHERE telegram_id = ?;
    ''', (id,))
    database.commit()   
    database.close()
