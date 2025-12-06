import telebot
from secrets import TOKEN
import logging

logging.basicConfig(level=logging.ERROR, filename="bot_errors.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

TOKEN
bot = telebot.TeleBot(TOKEN)  # Токен в отдельном файле

class Calendar:
    def __init__(self):
        self.events = {}  # Хранение событий

    # Создать событие
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

    # Прочитать событие по его ID
    def read_event(self, event_id):
        return self.events.get(event_id, None)

    # Изменить событие по его ID
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

    # Удалить событие по его ID
    def delete_event(self, event_id):
        return self.events.pop(event_id, None)

    # Показать список всех событий
    def list_events(self):
        return self.events.values()

calendar = Calendar()

# Контекст данных пользователя (словарь, где ключ — chat_id пользователя)
user_context = {}

# Начало создания события
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

# Обработчик для чтения события
@bot.message_handler(commands=["read_event"])
def event_read_handler(message):
    try:
        # Получить ID события из сообщения пользователя
        event_id = int(message.text[11:])

        # Прочитать событие с помощью метода read_event класса Calendar
        event = calendar.read_event(event_id)

        if event:
            response = f"Ваше событие: \nID: {event['id']} \nНазвание: {event['name']} \nДата: {event['date']} \nВремя: {event['time']} \nДетали: {event['details']}"
        else:
            response = "Событие с данным ID не найдено."

        # Отправить пользователю информацию о событии
        bot.reply_to(message, response)
    except ValueError:
        bot.reply_to(message, "Некорректный ID события.")

# Обработчик для редактирования события
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

# Обработчик для удаления события
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

# Обработчик для просмотра всех событий
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

# Основная точка входа
if __name__ == "__main__":
    bot.polling(non_stop=True)