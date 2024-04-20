from sqlite3 import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def creating():
    with connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS test_name(id INTEGER NOT NULL, name TEXT NOT NULL, creator_id INTEGER NOT NULL, PRIMARY KEY(id))")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS questions(id INTEGER NOT NULL, question TEXT NOT NULL, qnum INTEGER NOT NULL,FOREIGN KEY(id) REFERENCES test_name(id))")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS results(test_id INTEGER NOT NULL, user_id INTEGER NOT NULL, result INTEGER NOT NULL)")
        conn.commit()

def private_res(user_id):
    with connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM results WHERE user_id = (?)", (user_id, ))
        s = cur.fetchall()
        conn.commit()
        return s

def test_res(cr_id):
    with connect('project.db') as conn:
        l = []
        cur = conn.cursor()
        cur.execute("SELECT id FROM test_name WHERE creator_id = (?)", (cr_id, ))
        sp = cur.fetchall()
        for i in sp:
            for id in i:
                cur.execute("SELECT * FROM results WHERE test_id = (?)", (id, ))
                k = cur.fetchall()
                l.append(k)
        conn.commit()
    return l

def ques(testid, text, num):
    with connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, text, num))
        connection.commit()

def adding_questions(message):
    with connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM test_name")
        c = cur.fetchone()
        cur.execute("INSERT INTO test_name VALUES (?,?,?)", (c[0]+1, f'{message.text}', message.from_user.id))
        conn.commit()
    return c

def checking_id():
    with connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT id FROM test_name")
        b = cur.fetchall()
        connection.commit()
    return b

def find_name(testid):
    with connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM test_name WHERE id == (?)", (testid,))
        c = cur.fetchall()
        name = c[0][1]
        connection.commit()
    return name

def getting_question(testid, num):
    with connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = (?)', (testid, num))
        connection.commit()
        q = cur.fetchall()[0][0]
    return q

def insert_result(testid, user_id, cnt):
    with connect('project.db', check_same_thread=False) as conn:
        curs = conn.cursor()
        curs.execute("INSERT INTO results VALUES (?,?,?)", (testid, user_id, cnt))
        conn.commit()

def buts(creator_id):
    markup = InlineKeyboardMarkup()
    with connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM test_name WHERE creator_id = (?)", (creator_id, ))
        tests = cur.fetchall()
        for i in tests:
            markup.add(InlineKeyboardButton(f"Имя теста: {i[1]}, id теста: {i[0]}", callback_data=f"{i[0]}"))
    return markup