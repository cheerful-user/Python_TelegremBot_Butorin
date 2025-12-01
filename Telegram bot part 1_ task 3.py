"""
!!!
если правильно, то не могу подобрать код, который создает обработчик для создания событий
правильно ли я создал класс Calendar и его методы?

"""

#
import re  # модуль для работы с поиском вхождения символов
import telebot
from telebot import types
from secrets import TOKEN
import datetime
import os
import logging

logging.basicConfig(level=logging.ERROR, filename="bot_errors.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
import os.path

TOKEN
bot = telebot.TeleBot(TOKEN)  # токен в отдельном файле


class Calendar:
    def __init__(self):
        self.events = {}

    # Создать метод create_event
    def create_event(self, event_name, event_date, event_time, event_details):
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
        }
        self.events[event_id] = event
        return event_id

    # метод чтения события  для получения информации о собитии по его ID
    def read_events(self, event_id):
        return self.events.get(event_id, None)

    # метод для изменеения деталей событитя по его ID, принимает ID события и новые данные, которые нужно обновить
    def edit_event(self, event_id, event_name=None, event_date=None, event_time=None, event_details=None):
        event = self.events.get(event_id)
        if not event:
            return None
        if event_name:
            event["name"] = event_name
        if event_date:
            event["date"] = event_date
        if event_time:
            event["time"] = event_time
        if event_details:
            event["details"] = event_details
        return event

    # метод для удаления события по его ID. метод удааляет собитие и возвращает его если оно было найдено
    def delete_event(self, event_id):
        return self.events.pop(event_id, None)

    # метод для получения списка всех событий. возвращает все события из клендаря
    def list_events(self):
        return self.events.values()

    def build_note(self, note_text, note_name, bot, chat_id):
        # проверим существует ли файл с заданным названием, если нет то создаем новый,
        # если да - то заменим его на новую заметку
        try:
            with open(f"{note_name}.txt", "w", encoding="utf-8") as file:
                file.write(note_text)
                bot.send_message(chat_id, f'Успешое создание заметки! Можете стартануть заново "/start".')
        except Exception as e:
            bot.send_message(chat_id, f'ошибка при создании заметки: {e}. Стартаните заново "/start".')
            logging.error(f"Error writing to file {note_name}: {e}")

    def create_note_handler(self, call):
        # введем имя заметки и запишем ее в переменную
        sent_name_zam = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
        bot.register_next_step_handler(sent_name_zam, self.write_name_zam)

    def write_name_zam(self, message):
        note_name = message.text.strip()
        forbidden_symbols = "\\|/*<>?:"
        pattern = '[{0}]'.format(forbidden_symbols)
        if (re.search(pattern, note_name)):  # набор запрещенных символов символов для Windows
            bot.send_message(message.chat.id,
                             'вы ввели недопустимые символы в названии файла. Стартаните заново "/start".')
        else:
            bot.send_message(message.chat.id, 'в названии файла допустимые символы, отлично')
            # введем текст заметки и запишем его в переменную
            sent_text_zam = bot.send_message(message.chat.id, 'введите текст заметки: ')
            bot.register_next_step_handler(sent_text_zam,
                                           lambda msg: self.write_text_zam(msg, note_name, message.chat.id))

    def write_text_zam(self, message, note_name, chat_id):
        note_text = message.text
        self.build_note(note_text, note_name, bot, chat_id)

    def read_note_handler(self, call):
        # поиск заданного пользователем файла с заметками и вывод текста заметки
        note_name_read = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
        bot.register_next_step_handler(note_name_read, self.read_note_message)

    def read_note_message(self, message):
        note_name_for_read = message.text
        try:
            path = f"{note_name_for_read}.txt"
            if os.path.isfile(path):
                with open(f"{note_name_for_read}.txt", 'r', encoding="utf-8") as file:
                    lines = file.read()
                bot.send_message(message.chat.id,
                                 f'это сам текст данной заметки: "{lines}". Можете стартануть заново "/start".')
            else:
                bot.send_message(message.chat.id, 'сорян, такая заметка не найдена. Стартаните заново "/start".')
        except Exception as e:
            bot.send_message(message.chat.id, f"Преобразование 'чтение заметки' прошло неудачно, ошибка {e}")

    def edit_note_handler(self, call):
        # поиск заданного пользователем файла с заметками и ввод новой заметки в данный файл
        note_name_edit = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
        bot.register_next_step_handler(note_name_edit, self.edit_note_message)

    def edit_note_message(self, message):
        global note_name_for_edit
        note_name_for_edit = message.text
        path = f"{note_name_for_edit}.txt"
        if not os.path.isfile(path):
            bot.send_message(message.chat.id, 'сорян, такая заметка не найдена. Стартаните заново "/start".')
        else:
            with open(f"{note_name_for_edit}.txt", 'r', encoding="utf-8") as file:
                lines = file.read()
            bot.send_message(message.chat.id, f'Супер, такой файл существует, текст данной заметки: "{lines}".')
            note_text_edit_new = bot.send_message(message.chat.id, 'Введите новую заметку в этот файл: ')
            bot.register_next_step_handler(note_text_edit_new, self.edit_note_message_new)

    def edit_note_message_new(self, message):
        note_text_for_edit_new = message.text
        note_text_new = open(f"{note_name_for_edit}.txt", "w+")
        note_text_new.write(note_text_for_edit_new)
        note_text_new.close()
        bot.send_message(message.chat.id, f'Новая заметка {note_name_for_edit} создана. Стартаните заново "/start".')

    def delete_note_handler(self, call):
        # поиск заданного пользователем файла с заметками и его удаление
        note_name_delete = bot.send_message(call.message.chat.id, 'введите название файла с заметками: ')
        bot.register_next_step_handler(note_name_delete, self.delete_note_message)

    def delete_note_message(self, message):
        note_name_for_delete = message.text
        try:
            path = f"{note_name_for_delete}.txt"
            if os.path.isfile(path):
                os.remove(f"{note_name_for_delete}.txt")
                bot.send_message(message.chat.id, 'Файл с заметками обнаружен и удален! Стартаните заново "/start".')
            else:
                bot.send_message(message.chat.id, 'сорян, такая заметка не найдена')
        except Exception as e:
            bot.send_message(message.chat.id, f"Преобразование 'удаление заметки' прошло неудачно, ошибка {e}")

    def display_sorted_notes_handler(self, call):
        # вывод всех заметок пользователя в порядке увеличения символов в них
        try:
            notes = [note for note in os.listdir() if note.endswith(".txt")]
            sorted_notes = sorted(notes, key=len)
            bot.send_message(call.message.chat.id, f'это список заметок упорядоченный по названию: \n {sorted_notes}')
            sorted_list = sorted(notes, key=lambda n: len(open(n, 'r').read()))
            bot.send_message(call.message.chat.id,
                             f'\nэто список заметок упорядоченный по количеству символов в них: \n {sorted_list}')
        except Exception as e:
            bot.send_message(call.message.chat.id,
                             f"Преобразование 'вывод всех заметок пользователя в порядке увеличения символов в них' прошло неудачно, ошибка {e}")


calendar = Calendar()

# добавление обработчиков событий календаря

# Контекст данных пользователя (словарь, где ключ — chat_id пользователя)
user_context = {}

# Создать обработчик для создания событий
@bot.message_handler(commands=["create_event"])
def event_create_start(message):
    # Начинаем создание события, просим пользователя ввести название
    sent_msg = bot.send_message(message.chat.id, "Введите название события:")
    bot.register_next_step_handler(sent_msg, receive_event_name)

# Прием названия события
def receive_event_name(message):
    event_name = message.text
    user_context[message.chat.id] = {'event_name': event_name}

    # Просим пользователя ввести дату события
    sent_msg = bot.send_message(message.chat.id, "Введите дату события (гггг-мм-дд):")
    bot.register_next_step_handler(sent_msg, receive_event_date)

# Прием даты события
def receive_event_date(message):
    event_date = message.text
    user_context[message.chat.id]['event_date'] = event_date

    # Просим пользователя ввести время события
    sent_msg = bot.send_message(message.chat.id, "Введите время события (чч:мм):")
    bot.register_next_step_handler(sent_msg, receive_event_time)

# Прием времени события
def receive_event_time(message):
    event_time = message.text
    user_context[message.chat.id]['event_time'] = event_time

    # Просим пользователя ввести описание события
    sent_msg = bot.send_message(message.chat.id, "Введите описание события:")
    bot.register_next_step_handler(sent_msg, receive_event_description)

# Прием описания события и создание события
def receive_event_description(message):
    event_details = message.text
    user_data = user_context[message.chat.id]
    user_data['event_details'] = event_details

    # Создаем событие с помощью метода create_event класса Calendar
    event_id = calendar.create_event(user_data['event_name'], user_data['event_date'], user_data['event_time'], event_details)

    # Оповещаем пользователя о завершении создания события
    bot.send_message(message.chat.id, f"Событие {user_data['event_name']} создано и имеет номер {event_id}.")





# Создать обработчик для чтения событий
@bot.message_handler(commands=["read_event"])
def event_read_handler(message):
    try:
        # Получить ID события из сообщения пользователя
        event_id = int(message.text[11:])

        # Прочитать событие с помощью метода read_events класса Calendar
        event = calendar.read_events(event_id)

        if event:
            response = f"Ваше событие: \nID: {event['id']} \nНазвание: {event['name']} \nДата: {event['date']} \nВремя: {event['time']} \nДетали: {event['details']}"
        else:
            response = "Событие с данным ID не найдено."

        # Отправить пользователю информацию о событии
        bot.reply_to(message, response)
    except ValueError:
        bot.reply_to(message, "Некорректный ID события.")


# Создать обработчик для редактирования событий
@bot.message_handler(commands=["edit_event"])
def event_edit_handler(message):
    try:
        # Получаем данные из сообщения пользователя
        args = message.text.split(' ')
        event_id = int(args[1])
        event_name = args[2]
        event_date = args[3]
        event_time = args[4]
        event_details = ' '.join(args[5:])

        # Редактируем событие с помощью метода edit_event класса Calendar
        updated_event = calendar.edit_event(event_id, event_name, event_date, event_time, event_details)

        if updated_event:
            response = f"Событие с ID {event_id} успешно обновлено!"
        else:
            response = "Событие с данным ID не найдено."

        # Отправить пользователю подтверждение
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "Недостаточно данных для редактирования события.")


# Создать обработчик для удаления событий
@bot.message_handler(commands=["delete_event"])
def event_delete_handler(message):
    try:
        # Получаем ID события из сообщения пользователя
        event_id = int(message.text[13:])

        # Удаляем событие с помощью метода delete_event класса Calendar
        deleted_event = calendar.delete_event(event_id)

        if deleted_event:
            response = f"Событие с ID {deleted_event['id']} успешно удалено."
        else:
            response = "Событие с данным ID не найдено."

        # Отправить пользователю подтверждение
        bot.reply_to(message, response)
    except ValueError:
        bot.reply_to(message, "Некорректный ID события.")


# Создать обработчик для просмотра всех событий
@bot.message_handler(commands=["list_events"])
def events_list_handler(message):
    try:
        # Получаем список всех событий с помощью метода list_events класса Calendar
        all_events = calendar.list_events()

        if all_events:
            response = "\n".join([
                f"ID: {event['id']} \nНазвание: {event['name']} \nДата: {event['date']} \nВремя: {event['time']} \nДетали: {event['details']}\n\n"
                for event in all_events
            ])
        else:
            response = "Нет созданных событий."

        # Отправить пользователю список событий
        bot.reply_to(message, response)
    except:
        bot.reply_to(message, "Ошибка при получении списка событий.")







def main():
    # создадим и расположим кнопки
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
        bot.send_message(message.chat.id,
                         f'<i>Приветствую Вас, <b>{message.from_user.first_name}</b>, в нашем Телеграмм боте! \nПеред Вами'
                         f' меню выбора действий (нажмите нужную баттон): \n1 - для создания текстового'
                         f' файла с определенным названием и текстом заметки.\n2 - для вывода на экран содержимого'
                         f' заданной пользователем заметки.\n3 - для вывода на экран содержимого запрашиваемой'
                         f' пользователем заметки и ввода пользователем новой заметки.\n4 - для удаления указанной'
                         f' пользователем заметки.\n5 - для упорядочивания заметок по количеству символов в самих'
                         f' заметках.</i>', \
                         parse_mode='html', reply_markup=markup)
        global chat_id  # запомним в глобальную переменную id активного чата с пользователем
        chat_id = message.chat.id

    # обработка действия кнопок
    @bot.callback_query_handler(func=lambda call: True)
    def handle(call):
        if call.data == 'bt1':
            calendar.create_note_handler(call)
        if call.data == 'bt2':
            calendar.read_note_handler(call)
        if call.data == 'bt3':
            calendar.edit_note_handler(call)
        if call.data == 'bt4':
            calendar.delete_note_handler(call)
        if call.data == 'bt5':
            calendar.display_sorted_notes_handler(call)
        if call.data == 'hlp':
            bot.answer_callback_query(callback_query_id=call.id, text='Нажата кнопка помощи.😉', show_alert=True)
            bot.send_message(call.message.chat.id,
                             'Вам представлен бот для работы с заметками. Если что-то пошло не так, '
                             'попробуйте стартануть "/start"еще раз')


if __name__ == "__main__":
    main()

bot.infinity_polling()
