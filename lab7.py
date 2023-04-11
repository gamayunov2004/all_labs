import telebot
from telebot import types
from datetime import datetime as dt, timedelta, timezone
import psycopg2


conn = psycopg2.connect(database='schedule',
                        user='postgres',
                        password='0000',
                        host='localhost',
                        port='5432')
cursor = conn.cursor()


token = '5442051393:AAHNVf9NFuTDRyb_TOFjT95uJqG6Gkge9-8'
bot = telebot.TeleBot(token)

def timeconvert(clock):
    sgtTimeDelta = timedelta(hours=6)
    sgtTZObject = timezone(sgtTimeDelta)
    return (dt.utcfromtimestamp(int(clock)).astimezone(sgtTZObject))
    #delt = timedelta(weeks=1)
    #return (dt.utcfromtimestamp(int(x)).astimezone(sgtTZObject)+delt)
    #.strftime('%d.%m.%Y %A, %V %H:%M'))

def output(id):
    mas = []
    for lesson in range(id, id+5):
        cursor.execute(f"SELECT * FROM timetable WHERE id ={lesson}")
        records_lesson = cursor.fetchall()
        mas.append(records_lesson)
        cursor.execute(f"SELECT teacher_name FROM subject WHERE name = '{records_lesson[0][2]}'")
        records_teacher = cursor.fetchall()
        mas.append(records_teacher)
    day = str(f"{mas[0][0][1]}")
    first = str(f'1) <i>{mas[0][0][4]}</i>\n   <b>{mas[0][0][2]}</b>\n   <ins>{mas[0][0][3]}</ins>\n   {mas[1][0][0]}')
    second = str(f"2) <i>{mas[2][0][4]}</i>\n   <b>{mas[2][0][2]}</b>\n   <ins>{mas[2][0][3]}</ins>\n   {mas[3][0][0]}")
    third = str(f"3) <i>{mas[4][0][4]}</i>\n   <b>{mas[4][0][2]}</b>\n   <ins>{mas[4][0][3]}</ins>\n   {mas[5][0][0]}")
    fourth = str(f"4) <i>{mas[6][0][4]}</i>\n   <b>{mas[6][0][2]}</b>\n   <ins>{mas[6][0][3]}</ins>\n   {mas[7][0][0]}")
    fifth = str(f"5) <i>{mas[8][0][4]}</i>\n   <b>{mas[8][0][2]}</b>\n   <ins>{mas[8][0][3]}</ins>\n   {mas[9][0][0]}")
    return (f'————————————\n{day}\n{first}\n   \n{second}\n   \n{third}\n   \n{fourth}\n   \n{fifth}\n\n————————————')

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Хочу узнать о МТУСИ", "/help")
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница", "Суббота")
    keyboard.row("Текущая неделя", "/week" ,"Следующая неделя")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите ли Вы узнать свежую информацию о МТУСИ?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я полезный бот для студентов МТУСИ! Вот мои команды:\n/help - инструкция\n/mtuci '
                                      '- информация о мтуси\n/week - четность недели\n/monday - понедельник\n/tuesday '
                                      '- вторник\n/wednesday - среда\n/thirsday - четверг\n/friday - пятница\n/saturday'
                                      ' - суббота\n/thisweek - текущая неделя\n/nextweek - следующая неделя')

@bot.message_handler(commands=['week'])
def week_message(message):
    if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
        mes = 'Сейчас идёт <b>верхняя</b> <i>(нечётная)</i> неделя'
        bot.send_message(message.chat.id, mes, parse_mode='HTML')
    if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
        mes = 'Сейчас идёт <b>нижняя</b> <i>(чётная)</i> неделя'
        bot.send_message(message.chat.id, mes, parse_mode='HTML')

@bot.message_handler(commands=['mtuci'])
def mtuci_message(message):
    bot.send_message(message.chat.id, "https://mtuci.ru/")

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу узнать о мтуси":
        bot.send_message(message.chat.id, 'Тогда Вам сюда - https://mtuci.ru/')

    elif message.text.lower() == "понедельник" or message.text.lower() == "/monday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(1)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(31)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "вторник" or message.text.lower() == "/tuesday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(6)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(36)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "среда" or message.text.lower() == "/wednesday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(11)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(41)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "четверг" or message.text.lower() == "/thirsday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(16)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(46)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "пятница" or message.text.lower() == "/friday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(21)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(51)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "суббота" or message.text.lower() == "/saturday":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(26)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(56)
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "текущая неделя" or message.text.lower() == "/thisweek":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(1)+"\n\n"+output(6)+"\n\n"+output(11)+"\n\n"+output(16)+"\n\n"+output(21)+"\n\n"+output(26)+"\n\n"
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(31)+"\n\n"+output(36)+"\n\n"+output(41)+"\n\n"+output(46)+"\n\n"+output(51)+"\n\n"+output(56)+"\n\n"
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    elif message.text.lower() == "следующая неделя" or message.text.lower() == "/nextweek":
        if int(timeconvert(message.date).strftime('%V')) % 2 != 0:
            mes = output(31)+"\n\n"+output(36)+"\n\n"+output(41)+"\n\n"+output(46)+"\n\n"+output(51)+"\n\n"+output(56)+"\n\n"
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
        if int(timeconvert(message.date).strftime('%V')) % 2 == 0:
            mes = output(1)+"\n\n"+output(6)+"\n\n"+output(11)+"\n\n"+output(16)+"\n\n"+output(21)+"\n\n"+output(26)+"\n\n"
            bot.send_message(message.chat.id, mes, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')


bot.polling()
