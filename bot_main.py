import telebot

from main_function import absent_full_day, absent_half_day, get_names

from datetime import datetime
import os

bot = telebot.TeleBot('5729204958:AAEFzABmZlOcRbE-hs2EfKMV-3NwmDm-SNA')

# constants
name = 'Имя и Фамилия С большой буквы и без Ё'
day1 = 1
day2 = 1
lessons_count = 0

month = datetime.now().month
months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа",
          9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
names = get_names()


@bot.message_handler(commands=['start'])
def student_hello_get_name(message):
    mesg = bot.send_message(message.chat.id, 'Привет! Я бот для мониторинга посещаемости. ' +
                            'Как тебя зовут? (формат: Иванов Иван)')
    bot.register_next_step_handler(mesg, student_count)


def student_count(message):
    global name, names
    try:
        name = message.text.title()
        if name and name not in names:
            mesg = bot.send_message(message.chat.id, 'Такого имени нет. напишите "ок"')
            raise ZeroDivisionError
        else:
            bot.send_message(message.chat.id, f'Отлично, {name.split()[1]}')
            mesg = bot.send_message(message.chat.id, 'Вы пропустили полный день (несколько полных дней),' +
                                    'или часть одного дня? (полный/часть)')
            bot.register_next_step_handler(mesg, check)

    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def check(message):
    global month, months
    try:
        ans = message.text.lower()
        if ans == "полный":
            bot.send_message(message.chat.id, f'Отлично, полный день или несколько полных дней.')
            mesg = bot.send_message(message.chat.id,
                                    f'С какого числа {months[month]} вы хотите отметить? (напишите цифру. например, 5)')
            bot.register_next_step_handler(mesg, student_full_day_second)
        elif ans == "часть":
            bot.send_message(message.chat.id, f'Отлично, единичный пропуск')
            mesg = bot.send_message(message.chat.id,
                                    f'Какого числа {months[month]} это было? (напишите цифру. например, 5)')
            bot.register_next_step_handler(mesg, student_half_day_second)
        else:
            bot.send_message(message.chat.id, f'Полный или часть')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


# branch 1 "полный"


def student_full_day_second(message):
    global day1
    try:
        day1 = message.text
        if 1 <= int(day1) <= 31:
            mesg = bot.send_message(message.chat.id, f'С {day1} по? (напишите цифру. например, 5)')
            bot.register_next_step_handler(mesg, student_full_day_third)
        else:
            bot.send_message(message.chat.id, f'От 1 до 31.')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def student_full_day_third(message):
    global name, day1, day2, month, months
    try:
        day2 = message.text
        if 1 <= int(day2) <= 31:
            mesg = bot.send_message(message.chat.id,
                                    f'Отметить пропуск с {day1} {months[month]} по {day2} {months[month]} для {name}? '
                                    f'(да/нет)')
            bot.register_next_step_handler(mesg, student_full_check)
        else:
            bot.send_message(message.chat.id, f'От 1 до 31.')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def student_full_check(message):
    global name, day1, day2, month, months
    try:
        ans = message.text
        if ans == "да":
            absent_full_day(name, day1, day2)
            bot.send_message(message.chat.id, f'Отлично, отметил. '
                                              f'Ведомость посещаемости по ссылке: '
                                              f'https://docs.google.com/spreadsheets/d/'
                                              f'1oXkwc5ft6YE7e27iM_3a-UdMcMvkmus-9ogOhgRdIZI')
            mesg = bot.send_message(message.chat.id, f'В ответ вы можете скинуть сообщение о причине или справку.')
            bot.register_next_step_handler(mesg, send_message_to_admin)
        elif ans == "нет":
            mesg = bot.send_message(message.chat.id, f'Ошибка. Я не идеальный бот. Давай сначала (напиши "ок")')
            bot.register_next_step_handler(mesg, student_hello_get_name)
        else:
            bot.send_message(message.chat.id, f'да или нет.')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


# branch 2 "часть"


def student_half_day_second(message):
    global month, months, day1
    try:
        day1 = message.text
        if 1 <= int(day1) <= 31:
            mesg = bot.send_message(message.chat.id, f'{day1} {months[month]}. Сколько пар вы пропустили?')
            bot.register_next_step_handler(mesg, student_half_day_third)
        else:
            bot.send_message(message.chat.id, f'От 1 до 31.')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def student_half_day_third(message):
    global name, day1, day2, month, months, lessons_count
    try:
        lessons_count = message.text
        if 1 <= int(lessons_count) <= 4:
            mesg = bot.send_message(message.chat.id,
                                    f'Отметить пропуск {day1} {months[month]} {lessons_count} пар для {name}? (да/нет)')
            bot.register_next_step_handler(mesg, student_half_check)
        else:
            bot.send_message(message.chat.id, f'Максимум 4 пары')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def student_half_check(message):
    global name, day1, lessons_count
    try:
        ans = message.text
        if ans == "да":
            absent_half_day(name, day1, int(lessons_count) * 2)
            bot.send_message(message.chat.id, f'Отлично, отметил. '
                                              f'Ведомость посещаемости по ссылке: '
                                              f'https://docs.google.com/spreadsheets/d/'
                                              f'1oXkwc5ft6YE7e27iM_3a-UdMcMvkmus-9ogOhgRdIZI')
            mesg = bot.send_message(message.chat.id, f'В ответ вы можете скинуть сообщение о причине или справку.')
            bot.register_next_step_handler(mesg, send_message_to_admin)
        elif ans == "нет":
            mesg = bot.send_message(message.chat.id, f'Ошибка. Я не идеальный бот. Давай сначала (напиши "ок" и /start)')
            bot.register_next_step_handler(mesg, student_hello_get_name)
        else:
            bot.send_message(message.chat.id, f'да или нет.')
            raise ZeroDivisionError
    except Exception as e:
        mesg = bot.send_message(message.chat.id, f'Ошибка ({e}). Напишите "ок"')
        bot.register_next_step_handler(mesg, student_hello_get_name)


def send_message_to_admin(message):
    try:
        if message.photo:
            raw = message.photo[-1].file_id
            n = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(n, 'wb') as new_file:
                new_file.write(downloaded_file)
            img = open(n, 'rb')
            bot.send_photo(1533305274, img)
            bot.send_message(1533305274, f'{message.text}; {name}')

        else:
            bot.send_message(1533305274, f'{message.text}; {name}')
    except:
        bot.send_message(message.chat.id, f'Ошибка. Сообщил старосте.')
        bot.send_message(1533305274, f'Ошибка; {name}')


bot.polling(none_stop=True)
