import psycopg2
import telebot
from telebot import types
from datetime import datetime, timedelta
from babel.dates import format_date

connection = psycopg2.connect(database="new_v1",
                             user="postgres",
                             password="12345",
                             host="localhost")

token = '6285828476:AAFpS0Rio5dXM47ZaNHD0IY8EQk70jBhd1Q'

bot = telebot.TeleBot(token)

def get_week_type():
    today = datetime.today()
    first_of_september = datetime(today.year, 9, 1)
    delta = today - first_of_september
    return "Четная неделя" if (delta.days // 7) % 2 == 0 else "Нечетная неделя"

def get_schedule(day_of_week, week_type):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT s.item_id, i.name, i.type, t.name, s.start_time, s.end_time, r.number, s.week_type
        FROM schedule as s
        JOIN subject as i ON s.item_id = i.id
        JOIN teacher as t ON s.teacher_id = t.id
        JOIN room as r ON s.room_id = r.id
        WHERE s.day_of_week = %s AND (s.week_type = %s OR s.week_type = 'both')
        ORDER BY s.start_time
    """, (day_of_week, week_type))

    schedule = cursor.fetchall()
    print("Результат запроса:", schedule)

    full_schedule = [None] * 5
    for item in schedule:
        index = item[4].hour // 2 - 4
        if index < 5:
            full_schedule[index] = item

    return full_schedule

def russian_month_name(month_number):
    month_names = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }
    return month_names.get(month_number, "")

def format_schedule(schedule, day_of_week, week_number, week_type, date):
    result = []

    day_of_week_cases = {
        "Понедельник": "Понедельник",
        "Вторник": "Вторник",
        "Среда": "Среду",
        "Четверг": "Четверг",
        "Пятница": "Пятницу",
        "Суббота": "Субботу",
    }
    day_of_week_case = day_of_week_cases.get(day_of_week, day_of_week)

    result.append(f"Расписание на {day_of_week_case}")
    result.append(f"{day_of_week.capitalize()}, {date.day} {russian_month_name(date.month)}")
    result.append(f"№{week_number} неделя, {week_type.lower()}\n")
    for i, item in enumerate(schedule, 1):
        if item:
            result.append(f"{i}. {item[4].strftime('%H:%M')} - {item[5].strftime('%H:%M')}")
            result.append(f"{item[1]}")
            result.append(f"{item[2]}")
            result.append(f"{item[3]} в {item[6]}\n")
        else:
            if i == 1:
                result.append(f"{i}. 09:30 - 11:05")
            elif i == 2:
                result.append(f"{i}. 11:20 - 12:55")
            elif i == 3:
                result.append(f"{i}. 13:10 - 14:45")
            elif i == 4:
                result.append(f"{i}. 15:25 - 17:00")
            elif i == 5:
                result.append(f"{i}. 17:15 - 18:50")
            result.append("<Нет пары>\n")
    return "\n".join(result)

def schedule_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
               "Расписание на следующую неделю"]
    for button in buttons:
        markup.add(button)
    return markup

def get_day_of_week(day):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    return days[day]

def get_next_week_type(week_type):
    return "Четная неделя" if week_type == "Нечетная неделя" else "Нечетная неделя"

def get_target_date(day_of_week):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    target_day_index = days.index(day_of_week)
    today = datetime.today()
    today_index = today.weekday()
    days_difference = (target_day_index - today_index + 7) % 7

    return today + timedelta(days=days_difference)

def get_help_message():
    help_message = """
Привет,я телеграм-бот, который помогает с расписанием занятий.

Мой список команд:

/week - узнать текущий тип недели (четная/нечетная)
/mtuci - получить ссылку на официальный сайт МТУСИ
/help - получить краткую информацию о мне и список команд

Если хотетите узнать расписание на определенный день недели нажмите на кнопку с днем недели.

Нажмите на кнопку "Расписание на текущую неделю" или "Расписание на следующую неделю", чтобы узнать расписание на всю неделю.
    """
    return help_message

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать! Я бот, который поможет Вам с расписанием занятий. Воспользуйтесь кнопками ниже.",
                     reply_markup=schedule_markup())

@bot.message_handler(commands=['week'])
def handle_week(message):
    bot.send_message(message.chat.id, f"Текущая неделя: {get_week_type()}")

@bot.message_handler(commands=['mtuci'])
def handle_mtuci(message):
    bot.send_message(message.chat.id, "Официальный сайт МТУСИ: https://mtuci.ru/")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, get_help_message())

def get_week_schedule(week_type, current_date):
    week_schedule = ""
    for i in range(6):
        day = get_day_of_week(i)
        target_date = current_date + timedelta(days=i)
        day_schedule = get_schedule(day, week_type)
        week_schedule += format_schedule(day_schedule, day, target_date.isocalendar()[1], week_type,
                                         target_date)
        week_schedule += "\n\n"
    return week_schedule

@bot.message_handler(content_types=['text'])
def handle_text(message):
    today = datetime.today()
    current_week_type = get_week_type()
    next_week_type = get_next_week_type(current_week_type)

    if message.text.lower() in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]:
        target_date = get_target_date(message.text)
        day_schedule_current_week = get_schedule(message.text, current_week_type)
        day_schedule_next_week = get_schedule(message.text, next_week_type)

        if day_schedule_current_week:
            bot.send_message(message.chat.id, format_schedule(day_schedule_current_week, message.text, target_date.isocalendar()[1],
                                                              current_week_type, target_date))
        elif day_schedule_next_week:
            bot.send_message(message.chat.id, format_schedule(day_schedule_next_week, message.text, target_date.isocalendar()[1] + 1,
                                                              next_week_type, target_date + timedelta(days=7)))
        else:
            bot.send_message(message.chat.id, "Занятий на этот день нет.")
    elif message.text.lower() == "расписание на текущую неделю":
        current_week_start_date = today - timedelta(days=today.weekday())
        bot.send_message(message.chat.id, get_week_schedule(current_week_type, current_week_start_date))
    elif message.text.lower() == "расписание на следующую неделю":
        next_week_start_date = today + timedelta(days=(7 - today.weekday()))
        bot.send_message(message.chat.id, get_week_schedule(next_week_type, next_week_start_date))
    else:
        days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
        if message.text.lower() in days_of_week:
            day_index = days_of_week.index(message.text.lower())
            days_difference = (day_index - today.weekday() + 7) % 7
            days_difference = days_difference if days_difference != 0 else 7
            target_date = today + timedelta(days=days_difference)
            day_schedule_current_week = get_schedule(message.text, current_week_type)
            day_schedule_next_week = get_schedule(message.text, next_week_type)

            if day_schedule_current_week:
                bot.send_message(message.chat.id,
                                 format_schedule(day_schedule_current_week, message.text,
                                                 target_date.isocalendar()[1],
                                                 current_week_type, target_date))
            elif day_schedule_next_week:
                bot.send_message(message.chat.id,
                                 format_schedule(day_schedule_next_week, message.text,
                                                 target_date.isocalendar()[1] + 1,
                                                 next_week_type, target_date + timedelta(days=7)))
            else:
                bot.send_message(message.chat.id, "Занятий на этот день нет.")

        else:
            bot.send_message(message.chat.id, "Извините, я вас не понял.")

bot.polling()