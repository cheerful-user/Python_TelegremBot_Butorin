import telebot
from secrets import TOKEN
import logging
import psycopg2

logging.basicConfig(level=logging.ERROR, filename="bot_errors.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

TOKEN
bot = telebot.TeleBot(TOKEN)  # Токен в отдельном файле


# Состояния пользователя
STATE_IDLE = "idle"
STATE_CREATE_EVENT_NAME = "creating_event_name"
STATE_CREATE_EVENT_DATE = "creating_event_date"
STATE_CREATE_EVENT_TIME = "creating_event_time"
STATE_CREATE_EVENT_DETAILS = "creating_event_details"

# Словарь для хранения текущего состояния пользователя
user_states = {}


class Calendar:
    def __init__(self, conn):
        self.conn = conn  # Соединение с базой данных

    # Создать событие
    def create_event(self, event_name, event_date, event_time, event_details, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO events (name, date, time, details, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (event_name, event_date, event_time, event_details, user_id))
        event_id = cur.fetchone()[0]
        self.conn.commit()
        return event_id

    # Прочитать событие по его имени
    def read_event(self, event_name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM events WHERE name = %s", (event_name,))
        result = cur.fetchone()
        return result

    # Показать список всех событий
    def display_events(self, user_id=None):
        cur = self.conn.cursor()
        if user_id:
            cur.execute("SELECT * FROM events WHERE user_id = %s ORDER BY date ASC", (user_id,))
        else:
            cur.execute("SELECT * FROM events ORDER BY date ASC")
        results = cur.fetchall()
        return results

    # Изменить событие по его имени
    def edit_event(self, event_name, new_date=None, new_time=None, new_details=None):
        updates = []
        values = []
        if new_date:
            updates.append("date = %s")
            values.append(new_date)
        if new_time:
            updates.append("time = %s")
            values.append(new_time)
        if new_details:
            updates.append("details = %s")
            values.append(new_details)

        if updates:
            query = f"UPDATE events SET {', '.join(updates)} WHERE name = %s"
            values.append(event_name)

            cur = self.conn.cursor()
            cur.execute(query, tuple(values))
            self.conn.commit()
            return True
        return False

    # Удалить событие по его имени
    def delete_event(self, event_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        self.conn.commit()
        return bool(cur.rowcount)

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="myBD",
    user="postgres",
    password=1
)

# Создаем экземпляр класса Calendar
calendar = Calendar(conn)





# Контекст данных пользователя (словарь, где ключ — chat_id пользователя)
user_context = {}

# Начало создания события
@bot.message_handler(commands=["create_event"])
def event_create_start(message):
    # Устанавливаем состояние пользователя
    user_states[message.chat.id] = STATE_CREATE_EVENT_NAME

    # Начинаем создание события, просим пользователя ввести название
    sent_msg = bot.send_message(message.chat.id, "Введите название события:")
    bot.register_next_step_handler(sent_msg, receive_event_name)

# Прием названия события
def receive_event_name(message):
    if user_states.get(message.chat.id) != STATE_CREATE_EVENT_NAME:
        bot.reply_to(message, "Команды отменены. Введите /create_event, чтобы начать создание события.")
        return

    event_name = message.text
    user_context[message.chat.id] = {'event_name': event_name}

    # Переходим к следующему состоянию
    user_states[message.chat.id] = STATE_CREATE_EVENT_DATE

    # Просим пользователя ввести дату события
    sent_msg = bot.send_message(message.chat.id, "Введите дату события (гггг-мм-дд):")
    bot.register_next_step_handler(sent_msg, receive_event_date)

# Прием даты события
def receive_event_date(message):
    if user_states.get(message.chat.id) != STATE_CREATE_EVENT_DATE:
        bot.reply_to(message, "Команды отменены. Введите /create_event, чтобы начать создание события.")
        return

    event_date = message.text
    user_context[message.chat.id]['event_date'] = event_date

    # Переходим к следующему состоянию
    user_states[message.chat.id] = STATE_CREATE_EVENT_TIME

    # Просим пользователя ввести время события
    sent_msg = bot.send_message(message.chat.id, "Введите время события (чч:мм):")
    bot.register_next_step_handler(sent_msg, receive_event_time)

# Прием времени события
def receive_event_time(message):
    if user_states.get(message.chat.id) != STATE_CREATE_EVENT_TIME:
        bot.reply_to(message, "Команды отменены. Введите /create_event, чтобы начать создание события.")
        return

    event_time = message.text
    user_context[message.chat.id]['event_time'] = event_time

    # Переходим к следующему состоянию
    user_states[message.chat.id] = STATE_CREATE_EVENT_DETAILS

    # Просим пользователя ввести описание события
    sent_msg = bot.send_message(message.chat.id, "Введите описание события:")
    bot.register_next_step_handler(sent_msg, receive_event_description)

# Прием описания события и создание события
def receive_event_description(message):
    if user_states.get(message.chat.id) != STATE_CREATE_EVENT_DETAILS:
        bot.reply_to(message, "Команды отменены. Введите /create_event, чтобы начать создание события.")
        return

    event_details = message.text
    user_data = user_context[message.chat.id]
    user_data['event_details'] = event_details

    # Создаем событие с помощью метода create_event класса Calendar
    event_id = calendar.create_event(
        user_data['event_name'],
        user_data['event_date'],
        user_data['event_time'],
        event_details,
        message.chat.id  # Передаем chat_id пользователя
    )

    # Возвращаем пользователя в начальное состояние
    user_states[message.chat.id] = STATE_IDLE

    # Оповещаем пользователя о завершении создания события
    bot.send_message(message.chat.id, f"Событие {user_data['event_name']} создано и имеет номер {event_id}.")

# Обработчик для чтения события
@bot.message_handler(commands=["read_event"])
def event_read_handler(message):
    try:
        # Получаем название события из сообщения пользователя
        event_name = message.text.split()[1]

        # Читаем событие по имени
        event = calendar.read_event(event_name)

        if event:
            response = f"Ваше событие: \nID: {event[0]} \nНазвание: {event[1]} \nДата: {event[2]} \nВремя: {event[3]} \nДетали: {event[4]}"
        else:
            response = "Событие с данным именем не найдено."

        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "Некорректный формат команды. Используйте: /read_event <имя события>")

# Обработчик для редактирования события
@bot.message_handler(commands=["edit_event"])
def event_edit_handler(message):
    try:
        # Распределяем аргументы из сообщения
        args = message.text.split(' ')
        event_id = int(args[1])  # ID события
        event_name = args[2]  # Новое имя события
        event_date = args[3]  # Новая дата
        event_time = args[4]  # Новое время
        event_details = ' '.join(args[5:])  # Новые детали

        # Редактируем событие, передавая нужные аргументы
        updated_event = calendar.edit_event(event_name, event_date, event_time, event_details)

        if updated_event:
            response = f"Событие с именем '{event_name}' успешно обновлено!"
        else:
            response = "Событие с данным именем не найдено."

        bot.reply_to(message, response)
    except (IndexError, ValueError):
        bot.reply_to(message, "Некорректный формат команды. Используйте: /edit_event <ID> <new_name> <new_date> <new_time> <new_details>")



# Обработчик для удаления события
@bot.message_handler(commands=["delete_event"])
def event_delete_handler(message):
    try:
        # Получаем ID события из сообщения пользователя
        event_id = int(message.text.split()[1])

        # Удаляем событие с помощью метода delete_event класса Calendar
        deleted_event = calendar.delete_event(event_id)

        if deleted_event:
            response = f"Событие с ID {event_id} успешно удалено."
        else:
            response = "Событие с данным ID не найдено."

        # Отправить пользователю подтверждение
        bot.reply_to(message, response)
    except ValueError:
        bot.reply_to(message, "Некорректный формат команды. Используйте: /delete_event <ID>")

# Обработчик для просмотра всех событий
@bot.message_handler(commands=["list_events"])
def events_list_handler(message):
    try:
        # Получаем список всех событий
        all_events = calendar.display_events()

        if all_events:
            response = "\n".join([
                f"ID: {event[0]} \nНазвание: {event[1]} \nДата: {event[2]} \nВремя: {event[3]} \nДетали: {event[4]}\n\n"
                for event in all_events
            ])
        else:
            response = "Нет созданных событий."

        bot.reply_to(message, response)
    except Exception as e:
        logging.error(f"Ошибка при получении списка событий: {str(e)}")
        bot.reply_to(message, "Ошибка при получении списка событий.")

#вывод события, созданного конктретным пользователем
@bot.message_handler(commands=["list_my_events"])
def list_my_events_handler(message):
    try:
        # Получаем список событий текущего пользователя
        all_events = calendar.display_events(user_id=message.chat.id)

        if all_events:
            response = "\n".join([
                f"ID: {event[0]} \nНазвание: {event[1]} \nДата: {event[2]} \nВремя: {event[3]} \nДетали: {event[4]}\n\n"
                for event in all_events
            ])
        else:
            response = "У вас нет созданных событий."

        bot.reply_to(message, response)
    except Exception as e:
        logging.error(f"Ошибка при получении списка ваших событий: {str(e)}")
        bot.reply_to(message, "Ошибка при получении списка событий.")

# Обработчик команды /register
@bot.message_handler(commands=["register"])
def register_handler(message):
    try:
        # Получаем данные пользователя
        user_id = message.chat.id
        username = message.from_user.username

        # Проверяем, зарегистрирован ли пользователь
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE telegram_id = %s", (user_id,))
        count = cur.fetchone()[0]

        if count > 0:
            bot.reply_to(message, "Вы уже зарегистрированы.")
        else:
            # Регистрируем пользователя
            cur.execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s)", (user_id, username))
            conn.commit()
            bot.reply_to(message, "Регистрация прошла успешно.")
    except Exception as e:
        logging.error(f"Ошибка при регистрации пользователя: {str(e)}")
        bot.reply_to(message, "Ошибка при регистрации.")



# Основная точка входа
if __name__ == "__main__":
    bot.polling(non_stop=True)