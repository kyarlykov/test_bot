import telebot as tb
from telebot.handler_backends import State, StatesGroup
import os
from dotenv import load_dotenv
from bot_funcs_postgres import *

load_dotenv()
bot = tb.TeleBot(os.getenv("TOKEN"))

class MS(StatesGroup):
    my_res = State()
    test_res = State()
    questions = State()
    check_num = State()


@bot.message_handler(state = MS.my_res)
def my_res(message):
    user_id = message.from_user.id
    s = private_res(user_id)
    for r in s:
        bot.send_message(message.chat.id, f"Номер теста: {r[0]}, результат: {r[2]} / 5")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MS.test_res)
def res(message):
    bot.send_message(message.chat.id, "Выберите тест:", reply_markup=buts(message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    conn = c()
    cur = conn.cursor()
    cur.execute("SELECT id FROM test_name WHERE creator_id = (%s)", (call.from_user.id, ))
    tests = cur.fetchall()
    for i in tests:
        if call.data == f"{i[0]}":
            cur.execute("SELECT * FROM results WHERE test_id = (%s)", (i[0], ))
            res = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    if len(res) == 0:
        bot.send_message(call.message.chat.id, "Ваш тест никто не проходил!")
    else:
        for i in res:
             bot.send_message(call.message.chat.id, f"ID тестируемого: {i[1]}, результат: {i[2]}")

def q1(message, testid):
    ques(testid, message.text, 1)
    m = bot.send_message(message.chat.id, 'Успешно! Теперь второй вопрос!')
    bot.register_next_step_handler(m, q2, testid)


def q2(message, testid):
    ques(testid, message.text, 2)
    m = bot.send_message(message.chat.id, 'Успешно! Теперь третий вопрос!')
    bot.register_next_step_handler(m, q3, testid)


def q3(message, testid):
    ques(testid, message.text, 3)
    m = bot.send_message(message.chat.id, 'Успешно! Теперь четвёртый вопрос!')
    bot.register_next_step_handler(m, q4, testid)

def q4(message, testid):
    ques(testid, message.text, 4)
    m = bot.send_message(message.chat.id, 'Успешно! Теперь пятый вопрос!')
    bot.register_next_step_handler(m, q5, testid)



def q5(message, testid):
    ques(testid, message.text, 5)
    bot.send_message(message.chat.id, 'Успешно! Все вопросы добавлены!')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state = MS.questions)
def questions(message):
    c = adding_questions(message)
    testid = c[0]+1
    bot.send_message(message.chat.id, f'Код вашего теста - {testid}')
    bot.send_message(message.chat.id, 'Далее отправляйте свои вопросы по одному в следующем формате:')
    bot.send_message(message.chat.id, 'Номер вопроса)вопрос варианты: 1)вариант№1. 2)вариант№2. 3)вариант№3+. 4)вариант№4')
    bot.send_message(message.chat.id, 'Пример:\n3)Какая фамилия у нынешнего президента РФ? варианты: 1)Путин+. 2)Медведев. 3)Даванков. 4)Ельцин')
    m = bot.send_message(message.chat.id, 'Следите за пробелами и точками! Ставьте плюс после правильного ответа. Максимальное количество вопросов равно 5!')
    bot.register_next_step_handler(m, q1, testid)


@bot.message_handler(state = MS.check_num)
def check(message):
    b = checking_id()
    for bd in b:
        try:
            if int(message.text) in bd:
                testid = int(message.text)
                name = find_name(testid)
                m = bot.send_message(message.chat.id,
                                     f'Название теста - "{name}", отправьте "+" чтобы пройти или "?" чтобы выйти. ')
                bot.register_next_step_handler(m, prom, testid)
                break
        except ValueError:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, 'Попробуйте ещё раз!')
            break
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Попробуйте ещё раз!')


def prom(message, testid):
    if message.text == '+':
        q = getting_question(testid, 1)
        q = q.replace('\n', ' ')
        ques = q[:q.find('варианты:')]
        vars = q[q.find('варианты:') + 10:].split('.')
        vars = list(map(lambda x: x.lstrip(), vars))
        for i in vars:
            if i[-1] == '+':
                corr = str(i[0])
                vars[vars.index(i)] = i[:-1]
    var = " ".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    cnt = 0
    bot.register_next_step_handler(mes, a1, testid, cnt, corr)

def a1(message, testid, cnt, corr):
    if message.text == corr:
        cnt+=1

    q = getting_question(testid, 2)
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    vars = list(map(lambda x: x.lstrip(), vars))
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = " ".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a2, testid, cnt, corr)


def a2(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1

    q = getting_question(testid, 3)
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    vars = list(map(lambda x: x.lstrip(), vars))
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var =  " ".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a3, testid, cnt, corr)

def a3(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1
    q = getting_question(testid, 4)
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    vars = list(map(lambda x: x.lstrip(), vars))
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = " ".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a4, testid, cnt, corr)

def a4(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1
    q = getting_question(testid, 5)
    q = q.replace('\n', ' ')
    ques = q[:q.find('варианты:')]
    vars = q[q.find('варианты:') + 10:].split('.')
    vars = list(map(lambda x: x.lstrip(), vars))
    for i in vars:
        if i[-1] == '+':
            corr = str(i[0])
            vars[vars.index(i)] = i[:-1]
    var = " ".join(vars)
    bot.send_message(message.chat.id, f"{ques}")
    mes = bot.send_message(message.chat.id, f"{var}")
    bot.register_next_step_handler(mes, a5, testid, cnt, corr)


def a5(message, testid, cnt, corr):
    if message.text == corr:
        cnt += 1
    bot.send_message(message.chat.id, f"Ваш результат: {cnt} из 5!")
    insert_result(testid, message.from_user.id, cnt)
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