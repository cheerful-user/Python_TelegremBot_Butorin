#
import re # модуль для работы с поиском вхождения символов
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
from telebot import types
from secrets import TOKEN
TOKEN
bot=telebot.TeleBot(TOKEN)

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


  #markup = types.ReplyKeyboardMarkup()
  #button1 = types.KeyboardButton('создание текстового файла с определенным названием '
  #            'и текстом заметки.')
  #button2 = types.KeyboardButton('вывод на экран содержимого заданной пользователем заметки.')
  #button3 = types.KeyboardButton('вывод на экран содержимого запрашиваемой пользователем'
  #            ' заметки и ввода пользователем новой заметки.')
  #button4 = types.KeyboardButton('удалени указанной пользователем заметки.')
  #button5 = types.KeyboardButton('упорядочивание заметок по количеству символов в самих заметках.')
  #buttonN = types.KeyboardButton('выход из программы без исполнения действий.')
  #markup.row(button1)
  #markup.row(button2)
  #markup.row(button3)
  #markup.row(button4)
  #markup.row(button5)
  #markup.row(buttonN)
#@bot.message_handler(content_types=['text'])


#обработка действия кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'bt1':
        create_note_handler(call)
    if call.data == 'bt2':
        read_note()
    if call.data == 'bt3':
        edit_note()
    if call.data == 'bt4':
        delete_note()
    if call.data == 'bt5':
        display_sorted_notes()
    if call.data == 'hlp':
        bot.answer_callback_query(callback_query_id=call.id, text='Нажата кнопка помощи.😉', show_alert=True)
        bot.send_message(call.message.chat.id, 'Вам представлен бот для работы с заметками. Если что-то пошло не так, '
                                          'попробуйте стартануть "/start"еще раз')

#def build_note_msg(message):
    #if (message.text == 1):
    #bot.send_message(message.chat.id, 'файл найден')

def build_note(note_text, note_name):
    # проверим существует ли файл с заданным названием, если нет то создаем новый,
    # если да - то заменим его на новую заметку
    try:
        try:
            file = open(f"{note_name}.txt", "r+", encoding = "utf-8")


            # подскажите как вывести сообщение о том, что файл с введенным пользователем файл существует, в прежних заданиях было так:
            # bot.send_message(message.chat.id, 'файл найден') причем поиск файла и запись в него осуществляется правильно.
            # и правильно ли я подобрал необходимые модули? и общий ход решения?
            # ниже вставлен код задания 6 задания без необходимой обработки для телеграмм бота
            # может быть вы сможете отправить мне какой то общий код с необходимым синтаксисом для решения пободной задачи





            bot.send_message(message.chat.id, 'файл найден')
            bot.send_message(message.chat.id, f"файл создан")
        except IOError:
            file = open(f"{note_name}.txt", "w+", encoding = "utf-8")
            def build_note_msg1(message):
                bot.send_message(message.chat.id, f"файл создан")
        file.write(note_text)
        def build_note_msg2(message):
            bot.send_message(message.chat.id, f"Заметка {note_name} создана.")
    except:
        def build_note_msg3(message):
            bot.send_message(message.chat.id, "Преобразование 'проверки существует ли файл с заданным названием, если нет то создаем новый' прошло неудачно")



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










    # bot.send_message(message.chat.id, f"заметка {note_name} создана, с текстом {note_text}")
    #except:
    #    bot.send_message(call.message.chat.id, "Преобразование 'создание заметки' прошло неудачно.")


  #  bot.answer_callback_query(call.id)

# вывод сообщения -  bot.send_message(message.chat.id, 'Произошла ошибка.')


bot.infinity_polling()



