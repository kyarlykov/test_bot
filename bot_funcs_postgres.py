from psycopg2 import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def c():
    conn = connect(
        dbname = "postgres",
        user = "postgres",
        password = "14Kirill122006",
        host = "db",
        port = 5432
    )
    return conn

def private_res(user_id):
    con = c()
    cur = con.cursor()
    cur.execute("SELECT * FROM results WHERE user_id = (%s)", (user_id,))
    s = cur.fetchall()
    cur.close()
    con.commit()
    con.close()
    return s

def test_res(cr_id):
    conn = c()
    l = []
    cur = conn.cursor()
    cur.execute("SELECT id FROM test_name WHERE creator_id = (%s)", (cr_id,))
    sp = cur.fetchall()
    for i in sp:
        for id in i:
            cur.execute("SELECT * FROM results WHERE test_id = (%s)", (id,))
            k = cur.fetchall()
            l.append(k)
    cur.close()
    conn.commit()
    conn.close()
    return l

def ques(testid, text, num):
    conn = c()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions VALUES(%s,%s,%s)", (testid, text, num))
    cur.close()
    conn.commit()
    conn.close()

def adding_questions(message):
    conn = c()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM test_name")
    next_id = cur.fetchone()
    cur.execute("INSERT INTO test_name VALUES (%s,%s,%s)", (next_id[0] + 1, f'{message.text}', message.from_user.id))
    cur.close()
    conn.commit()
    conn.close()
    return next_id

def checking_id():
    conn = c()
    cur = conn.cursor()
    cur.execute("SELECT id FROM test_name")
    b = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return b

def find_name(testid):
    conn = c()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_name WHERE id = (%s)", (testid,))
    names = cur.fetchall()
    name = names[0][1]
    cur.close()
    conn.commit()
    conn.close()
    return name

def getting_question(testid, num):
    connection = c()
    cur = connection.cursor()
    cur.execute('SELECT question FROM questions WHERE id = (%s) and qnum = (%s)', (testid, num))
    q = cur.fetchall()[0][0]
    cur.close()
    connection.commit()
    connection.close()
    return q

def insert_result(testid, user_id, cnt):
    conn = c()
    curs = conn.cursor()
    curs.execute("INSERT INTO results VALUES (%s,%s,%s)", (testid, user_id, cnt))
    curs.close()
    conn.commit()
    conn.close()

def buts(creator_id):
    conn = c()
    markup = InlineKeyboardMarkup()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_name WHERE creator_id = (%s)", (creator_id, ))
    tests = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    for i in tests:
        markup.add(InlineKeyboardButton(f"Имя теста: {i[1]}, id теста: {i[0]}", callback_data=f"{i[0]}"))
    return markup







