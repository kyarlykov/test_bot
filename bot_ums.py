import telebot as tb
from telebot.handler_backends import State, StatesGroup
import sqlite3
from token_bot import token

bot = tb.TeleBot(token)

class MS(StatesGroup):
    my_res = State()
    test_res = State()
    questions = State()
    check_num = State()


with sqlite3.connect('project.db') as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test_name(id INTEGER NOT NULL, name TEXT NOT NULL, creator_id INTEGER NOT NULL, PRIMARY KEY(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER NOT NULL, question TEXT NOT NULL, qnum INTEGER NOT NULL,FOREIGN KEY(id) REFERENCES test_name(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS results(test_id INTEGER NOT NULL, user_id INTEGER NOT NULL, result INTEGER NOT NULL)")
    conn.commit()


@bot.message_handler(state = MS.my_res)
def my_res(message):
    user_id = message.from_user.id
    with sqlite3.connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM results WHERE user_id = (?)", (user_id, ))
        s = cur.fetchall()
        conn.commit()
    for r in s:
        bot.send_message(message.chat.id, f"Номер теста: {r[0]}, результат: {r[2]} / 5")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state = MS.test_res)
def test_res(message):
    l = []
    cr_id = message.from_user.id
    with sqlite3.connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM test_name WHERE creator_id = (?)", (cr_id, ))
        sp = cur.fetchall()
        for i in sp:
            for id in i:
                cur.execute("SELECT * FROM results WHERE test_id = (?)", (id, ))
                k = cur.fetchall()
                l.append(k)
        conn.commit()
    for i in l:
        bot.send_message(message.chat.id, f"Номер теста: {i[0]}, ID тестируемого: {i[1]}, результат: {i[2]}")
    bot.delete_state(message.from_user.id, message.chat.id)




def q1(message, testid):
    num = 1
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, message.text, num))
        connection.commit()
    m = bot.send_message(message.chat.id, 'Успешно! Теперь второй вопрос!')
    bot.register_next_step_handler(m, q2, testid)


def q2(message, testid):
    num = 2
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, message.text, num))
        connection.commit()
    m = bot.send_message(message.chat.id, 'Успешно! Теперь третий вопрос!')
    bot.register_next_step_handler(m, q3, testid)


def q3(message, testid):
    num = 3
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, message.text, num))
        connection.commit()

    m = bot.send_message(message.chat.id, 'Успешно! Теперь четвёртый вопрос!')
    bot.register_next_step_handler(m, q4, testid)



def q4(message, testid):
    num = 4
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, message.text, num))
        connection.commit()
    m = bot.send_message(message.chat.id, 'Успешно! Теперь пятый вопрос!')
    bot.register_next_step_handler(m, q5, testid)



def q5(message, testid):
    num = 5
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO questions VALUES(?,?,?)", (testid, message.text, num))
        connection.commit()
    bot.send_message(message.chat.id, 'Успешно! Все вопросы добавлены!')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state = MS.questions)
def questions(message):
    with sqlite3.connect('project.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM test_name")
        c = cur.fetchone()
        cur.execute("INSERT INTO test_name VALUES (?,?,?)", (c[0]+1, f'{message.text}', message.from_user.id))
        conn.commit()
    testid = c[0]+1
    bot.send_message(message.chat.id, f'Код вашего теста - {testid}')
    bot.send_message(message.chat.id, 'Далее отправляйте свои вопросы по одному в следующем формате:')
    bot.send_message(message.chat.id, 'Номер вопроса)вопрос варианты: 1)вариант№1. 2)вариант№2. 3)вариант№3+. 4)вариант№4')
    bot.send_message(message.chat.id, 'Пример:\n3)Какая фамилия у нынешнего президента РФ? варианты: 1)Путин+. 2)Медведев. 3)Даванков. 4)Ельцин')
    m = bot.send_message(message.chat.id, 'Следите за пробелами и точками! Ставьте плюс после правильного ответа. Максимальное количество вопросов равно 5!')
    bot.register_next_step_handler(m, q1, testid)


@bot.message_handler(state = MS.check_num)
def check(message):
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT id FROM test_name")
        b = cur.fetchall()
        connection.commit()
    for bd in b:
        if int(message.text) in bd:
            testid = int(message.text)
            with sqlite3.connect('project.db') as connection:
                cur = connection.cursor()
                cur.execute("SELECT * FROM test_name WHERE id == (?)", (testid,))
                c = cur.fetchall()
                name = c[0][1]
                connection.commit()
            m = bot.send_message(message.chat.id,
                                 f'Название теста - "{name}", отправьте "+" чтобы пройти или "?" чтобы выйти. ')
            bot.register_next_step_handler(m, prom, testid)
            break
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Попробуйте ещё раз!')


def checki(message, testid):
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM test_name WHERE id == (?)", (testid,))
        c = cur.fetchall()
        name = c[0][1]
        connection.commit()
    m = bot.send_message(message.chat.id, f'Название теста - "{name}", отправьте "+" чтобы пройти или "-" чтобы выйти. ')
    bot.register_next_step_handler(m, prom, testid)


def prom(message, testid):
    if message.text == '+':
        with sqlite3.connect('project.db') as connection:
            cur = connection.cursor()
            cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = 1', (testid,))
            connection.commit()
            q = cur.fetchall()[0][0]
        q = q.replace('\n', ' ')
        ques = q[:q.find('варианты:')]
        vars = q[q.find('варианты:') + 10:].split('.')
        for i in vars:
            if i[-1] == '+':
                corr = str(i[0])
                vars[vars.index(i)] = i[:-1]
    var = "".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    cnt = 0
    bot.register_next_step_handler(mes, a1, testid, cnt, corr)

def a1(message, testid, cnt, corr):
    if message.text == corr:
        cnt+=1

    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = 2', (testid,))
        connection.commit()
        q = cur.fetchall()[0][0]
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = "".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a2, testid, cnt, corr)


def a2(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1

    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = 3', (testid,))
        connection.commit()
        q = cur.fetchall()[0][0]
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = "".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a3, testid, cnt, corr)

def a3(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1

    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = 4', (testid,))
        connection.commit()
        q = cur.fetchall()[0][0]
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = "".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a4, testid, cnt, corr)

def a4(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1
    with sqlite3.connect('project.db') as connection:
        cur = connection.cursor()
        cur.execute('SELECT question FROM questions WHERE id = (?) and qnum = 5', (testid,))
        connection.commit()
        q = cur.fetchall()[0][0]
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = "".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a5, testid, cnt, corr)


def a5(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1
    bot.send_message(message.chat.id, f"Ваш результат: {cnt} из 5!")
    with sqlite3.connect('project.db', check_same_thread=False) as conn:
        curs = conn.cursor()
        curs.execute("INSERT INTO results VALUES (?,?,?)", (testid, message.from_user.id, cnt))
        conn.commit()
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['start'])
def start(message):
    markup = tb.types.ReplyKeyboardMarkup()
    markup.add(tb.types.KeyboardButton("/create"))
    markup.add(tb.types.KeyboardButton("/run"))
    markup.add(tb.types.KeyboardButton("/results"))
    bot.send_message(message.chat.id,
                     'Здравствуйте! Это бот для создания/прохождения тестов.\nВыберите действие:\n/create - создание теста\n/run - выполнить тест\n/results - посмотреть результаты',
                     reply_markup=markup)


@bot.message_handler(commands=['create'])
def create(message):
    bot.send_message(message.chat.id, 'Напишите название своего теста')
    bot.set_state(message.from_user.id, MS.questions)


@bot.message_handler(commands=['run'])
def run(message):
    bot.send_message(message.chat.id, "Введите код теста:")
    bot.set_state(message.from_user.id, MS.check_num)

@bot.message_handler(commands=['results'])
def res(message):
    b = bot.send_message(message.chat.id, f'Введите "1" чтобы посмотреть результаты пройденных тестов\nВведите "2" чтобы посмотреть результаты своих тестов!')
    bot.register_next_step_handler(b, ress)
def ress(message):
    if message.text == '1':
        bot.send_message(message.chat.id, f"Подтвердите своё действие отправив +")
        bot.set_state(message.from_user.id, MS.my_res)
    elif message.text == '2':
        bot.send_message(message.chat.id, f"Подтвердите своё действие отправив +")
        bot.set_state(message.from_user.id, MS.test_res)


bot.add_custom_filter(tb.custom_filters.StateFilter(bot))
bot.infinity_polling()