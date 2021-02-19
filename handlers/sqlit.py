import sqlite3
def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_list (
            name,
            number
            ) """)
    db.commit()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_ref
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()


def info_members():
    a = 0
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    for i in sql.execute(f'SELECT * from user_time'):
        a+=1
    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    name = name[1:]
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (name, 1))
        db.commit()
    db.commit()

def reg_channels(text): #Регистрация списка каналов
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    text = text.split()
    for i in text:
        i = i[1:]
        sql.execute(f"SELECT name FROM channel_list WHERE name ='{i}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (i, 1))
            db.commit()
        db.commit()

def proverka_channel(channel_name):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT name FROM channel_list WHERE name ='{channel_name}'").fetchone()
    if a is None:
        return 0
    else:
        return 1