#
import re # модуль для работы с поиском вхождения символов
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
from telebot import types
from secrets import TOKEN
TOKEN
bot=telebot.TeleBot(TOKEN) # токен в отдельном файле
import os.path

#создадим и расположим кнопки
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    bot1 = types.InlineKeyboardButton("1", callback_data='bt1')
    bot2 = types.InlineKeyboardButton("2", callback_data='bt2')
    bot3 = types.InlineKeyboardButton("3", callback_data='bt3')
    bot4 = types.InlineKeyboardButton("4", callback_data='bt4')
    bot5 = types.InlineKeyboardButton("5", callback_data='bt5')
    markup.row(bot1, bot2, bot3, bot4, bot5)
    markup.add(types.InlineKeyboardButton('help', callback_data='hlp'))
    bot.send_message(message.chat.id,f'<i>Приветствую Вас, <b>{message.from_user.first_name}</b>, в нашем Телеграмм боте! \nПеред Вами'
                                   f' меню выбора действий (нажмите нужную баттон): \n1 - для создания текстового'
                                   f' файла с определенным названием и текстом заметки.\n2 - для вывода на экран содержимого'
                                   f' заданной пользователем заметки.\n3 - для вывода на экран содержимого запрашиваемой'
                                   f' пользователем заметки и ввода пользователем новой заметки.\n4 - для удаления указанной'
                                   f' пользователем заметки.\n5 - для упорядочивания заметок по количеству символов в самих'
                                   f' заметках.</i>', \
                                    parse_mode='html', reply_markup=markup)

#обработка действия кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'bt1':
        create_note_handler(call)
    if call.data == 'bt2':
        read_note_handler(call)
    if call.data == 'bt3':
        edit_note_handler(call)
    if call.data == 'bt4':
        delete_note_handler(call)
    if call.data == 'bt5':
        display_sorted_notes_handler(call)
    if call.data == 'hlp':
        bot.answer_callback_query(callback_query_id=call.id, text='Нажата кнопка помощи.😉', show_alert=True)
        bot.send_message(call.message.chat.id, 'Вам представлен бот для работы с заметками. Если что-то пошло не так, '
                                          'попробуйте стартануть "/start"еще раз')

def build_note(note_text, note_name):
    # проверим существует ли файл с заданным названием, если нет то создаем новый,
    # если да - то заменим его на новую заметку
        # try: ранее был блок  try:   except: но я не знаю как после except вывести сообщение об непредвиденной ошибке
    try:
        file = open(f"{note_name}.txt", "w", encoding = "utf-8")
        file.write(note_text)
        file.close()
    except IOError:
            file = open(f"{note_name}.txt", "w+", encoding = "utf-8")
            file.write(note_text)
            file.close()
    #except:

def create_note_handler(call):
    # введем имя заметки и запишем ее в переменную
    sent_name_zam = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
    bot.register_next_step_handler(sent_name_zam, write_name_zam)
def write_name_zam(message):
    global note_name # объявим переменную "note_name" в глобальную
    note_name = message.text
    forbidden_symbols = "\\|/*<>?:"
    pattern = '[{0}]'.format(forbidden_symbols)
    if (re.search(pattern, note_name)):  # набор запрещенных символов символов для Windows
        bot.send_message(message.chat.id, 'вы ввели недопустимые символы в названии файла. Стартаните заново "/start".')
    else:
        bot.send_message(message.chat.id, 'в названии файла допустимые символы, отлично')
        # введем текст заметки и запишем его в переменную
        sent_text_zam = bot.send_message(message.chat.id, 'введите текст заметки: ')
        bot.register_next_step_handler(sent_text_zam, write_text_zam)
    return note_name
def write_text_zam(message):
    global note_text # объявим переменную "note_text" в глобальную
    note_text = message.text
    build_note(note_text, note_name)
    return note_text

def read_note_handler(call):
    # поиск заданного пользователем файла с заметками и вывод текста заметки
    note_name_read = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
    bot.register_next_step_handler(note_name_read, read_note_message)
def read_note_message(message):
    note_name_for_read = message.text
    try:
        path = f"{note_name_for_read}.txt"
        if os.path.isfile(path):
            with open(f"{note_name_for_read}.txt", 'r') as file:
                lines = file.read()
                note_name_for_read.close()
            bot.send_message(message.chat.id, f'это сам текст данной заметки: {lines}')
        else:
            bot.send_message(message.chat.id, 'сорян, такая заметка не найдена. Стартаните заново "/start".')
    except:
        bot.send_message(message.chat.id, "Преобразование 'чтение заметки' прошло неудачно")

def edit_note_handler(call):
    # поиск заданного пользователем файла с заметками и ввод новой заметки в данный файл
    note_name_edit = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
    bot.register_next_step_handler(note_name_edit, edit_note_message)
def edit_note_message(message):
    global note_name_for_edit
    note_name_for_edit = message.text
    path = f"{note_name_for_edit}.txt"
    if not os.path.isfile(path):
        bot.send_message(message.chat.id, 'сорян, такая заметка не найдена. Стартаните заново "/start".')
    else:
        bot.send_message(message.chat.id, 'Такой файл с заметками уже существует! ')
        #note_text_new = open(f"{note_name_for_edit}.txt", "w+")
        note_text_edit_new = bot.send_message(message.chat.id, 'Введите новую заметку в этот файл: ')
        bot.register_next_step_handler(note_text_edit_new, edit_note_message_new)
def edit_note_message_new(message):
    note_text_for_edit_new = message.text
    note_text_new = open(f"{note_name_for_edit}.txt", "w+")
    note_text_new.write(note_text_for_edit_new)
    note_text_new.close()
    bot.send_message(message.chat.id, f'Новая заметка {note_name_for_edit} создана.')

def delete_note_handler(call):
    # поиск заданного пользователем файла с заметками и его удаление
    note_name_delete = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
    bot.register_next_step_handler(note_name_delete, delete_note_message)
def delete_note_message(message):
    note_name_for_delete = message.text
    try:
        path = f"{note_name_for_delete}.txt"
        if os.path.isfile(path):
            os.remove(f"{note_name_for_delete}.txt")
            bot.send_message(message.chat.id, 'Файл с заметками удален!')
        else:
            bot.send_message(message.chat.id, 'сорян, такая заметка не найдена')
    except:
        bot.send_message(message.chat.id, "Преобразование 'удаление заметки' прошло неудачно")

def display_sorted_notes_handler(call):
    # вывод всех заметок пользователя в порядке увеличения символов в них
    try:
        notes = [note for note in os.listdir() if note.endswith(".txt")]
        sorted_notes = sorted(notes, key=len)
        bot.send_message(call.message.chat.id,f'это список заметок упорядоченный по названию: \n {sorted_notes}')
        sorted_list = sorted(notes, key=lambda n: len(open(n, 'r').read()))
        bot.send_message(call.message.chat.id,f'\nэто список заметок упорядоченный по количеству символов в них: \n {sorted_list}')
    except:
        bot.send_message(call.message.chat.id,"Преобразование 'вывод всех заметок пользователя в порядке увеличения символов в них' прошло неудачно")

bot.infinity_polling()
