import random, math, telebot
from telebot import types, apihelper

apihelper.proxy = {"https": "socks5://127.0.0.1:9050",
                   "https": "платный прокси"}

bot = telebot.TeleBot('правильный токен')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     '/random - выведет вам целое или вещественное случайное число в заданном вами диапазоне\n'
                     '/calculator - примитивный калькулятор\n/help - помощь')
    

@bot.message_handler(commands=['random'])
def send_text(message):
    keyboardrandom = types.InlineKeyboardMarkup()
    key_float = types.InlineKeyboardButton(text='Вещественное', callback_data='float')
    key_int = types.InlineKeyboardButton(text='Целое', callback_data='int')
    keyboardrandom.add(key_float)
    keyboardrandom.add(key_int)
    bot.send_message(message.from_user.id, 'Какое вам нужно число?', reply_markup=keyboardrandom)

@bot.message_handler(commands=['calculator'])
def calc(message):
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, get_num)

def get_num(message):
    global a
    a = float(message.text)
    question = 'Что будем с ним делать?'
    keyboard = types.InlineKeyboardMarkup()
    key_plus = types.InlineKeyboardButton(text='+', callback_data="plus")
    key_minus = types.InlineKeyboardButton(text='-', callback_data='minus')
    key_divide = types.InlineKeyboardButton(text='/', callback_data='divide')
    key_multiply = types.InlineKeyboardButton(text='*', callback_data='multiply')
    key_sqrt = types.InlineKeyboardButton(text='sqrt', callback_data='sqrt')
    key_log = types.InlineKeyboardButton(text='log', callback_data='log')
    key_sin = types.InlineKeyboardButton(text='sin', callback_data='sin')
    key_cos = types.InlineKeyboardButton(text='cos', callback_data='cos')
    keyboard.row(key_plus, key_minus, key_multiply, key_divide)
    keyboard.row(key_sqrt, key_log, key_sin, key_cos)
    reply_markup = keyboard
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    mes = call.data
    bot.edit_message_reply_markup(call.message.from_user.id, reply_markup=call)
    global a
    global b
    if mes == 'plus':
        bot.send_message(call.message.chat.id, 'С чем будем складывать?')

        @bot.message_handler(content_types=['text'])
        def plus(message):
            b = float(message.text)
            b = a + b
            str(b)
            bot.send_message(call.message.chat.id, b)
    elif mes == "minus":
        bot.send_message(call.message.chat.id, 'Что будем вычитать?')

        @bot.message_handler(content_types=['text'])
        def minus(message):
            b = float(message.text)
            b = a - b
            str(b)
            bot.send_message(message.chat.id, b)
    elif mes == 'divide':
        bot.send_message(call.message.chat.id, 'На что будем делить?')

        @bot.message_handler(content_types=['text'])
        def divide(message):
            b = float(message.text)
            b = a / b
            str(b)
            bot.send_message(message.chat.id, b)
    elif mes == 'multiply':
        bot.send_message(call.message.chat.id, 'На что будем умножать?')

        @bot.message_handler(content_types=['text'])
        def multiply(message):
            b = float(message.text)
            b = a * b
            str(b)
            bot.send_message(message.chat.id, b)
    elif mes == 'sqrt':
        bot.send_message(call.message.chat.id, 'Корень какой степени вы хотите извлечь?')

        @bot.message_handler(content_types=['text'])
        def sqrt(message):
            b = float(message.text)
            b = math.pow(a, 1 / b)
            str(b)
            bot.send_message(message.chat.id, b)
    elif mes == 'log':
        bot.send_message(call.message.chat.id, 'Какое основание будет у логарифма?')

        @bot.message_handler(content_types=['text'])
        def log(message):
            b = float(message.text)
            b = math.log(a, b)
            str(b)
            bot.send_message(message.chat.id, b)
    elif mes == 'sin':
        a = math.radians(a)
        b = math.sin(a)
        b = str(b)
        bot.send_message(call.message.chat.id, b)
    elif mes == 'cos':
        a = math.radians(a)
        b = math.cos(a)
        b = str(b)
        bot.send_message(call.message.chat.id, b)
    elif mes == 'float':
        bot.send_message(call.message.chat.id,
                         'Введите нижний и верхний предел предел '
                         '(два вещественных числа (пример - 5.43), '
                         'через пробел)')

        @bot.message_handler(content_types=['text'])
        def get_lower(message):
            b = message.text
            c = b.split()
            b = float(c[1])
            a = float(c[0])
            b = random.uniform(a, b)
            bot.send_message(call.message.chat.id, str(b))
    elif mes == 'int':
        bot.send_message(call.message.chat.id, 'Введите нижний и верхний '
                                               'предел предел (два целых числа, через пробел)')

        @bot.message_handler(content_types=['text'])
        def get_lower(message):
            b = message.text
            c = b.split()
            b = int(c[1])
            a = int(c[0])
            b = random.randint(a, b)
            bot.send_message(call.message.chat.id, str(b))
    else:
        help()
    bot.answer_callback_query(call.id, text="")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'Помните, вещественные числа надо вводить через точку (пример - 6.04)\n '
                     'В /calculator угол вводится в градусах\n'
                     '/random - выведет вам целое или вещественное '
                     'случайное число в заданном '
                     'вами диапазоне\n/calculator - примитивный калькулятор')


bot.polling(none_stop=True)
