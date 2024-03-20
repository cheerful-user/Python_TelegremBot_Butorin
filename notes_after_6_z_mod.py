# выполненное шестое задание
import re # модуль для работы с поиском вхождения символов

def build_note(note_text, note_name):
    # проверим существует ли файл с заданным названием, если нет то создаем новый,
    # если да - то заменим его на новую заметку
    try:
        try:
            file = open(f"{note_name}.txt", "r+", encoding = "utf-8")
            print('файл найден')
        except IOError:
            file = open(f"{note_name}.txt", "w+", encoding = "utf-8")
            print('файл создан')
        file.write(note_text)
        print(f"Заметка {note_name} создана.")
    except:
        print("Преобразование 'проверки существует ли файл с заданным названием, если нет то создаем новый' прошло неудачно")

def create_note():
    # создадим файл с заметками
    try:
        # проверим название создаваемого файла на наличие запрещенных символов
        note_name = input('введите название файла с заметками: ')
        forbidden_symbols = "\\|/*<>?:"
        pattern = '[{0}]'.format(forbidden_symbols)
        if (re.search(pattern, note_name)):  # набор запрещенных символов символов для Windows
            print("вы ввели недопустимые символы в названии файла. Программа остановлена.")
        else:
            print("в названии файла допустимые символы, отлично")
            note_text = input('введите текст заметки: ')
            build_note(note_text, note_name)
    except:
        print("Преобразование 'создание заметки' прошло неудачно.")

def read_note():
    # поиск заданного пользователем файла с заметками и вывод текста заметки
    import os.path

    try:
        note_name_read = input('введите название файла с заметками: ')
        path = f"{note_name_read}.txt"
        if os.path.isfile(path):
            with open(f"{note_name_read}.txt", 'r') as file:
                lines = file.read()
            print('это сам текст данной заметки: ', lines)
        else:
            print('сорян, такая заметка не найдена')
    except:
        print("Преобразование 'чтение заметки' прошло неудачно")

def edit_note():
    # поиск заданного пользователем файла с заметками и ввод новой заметки в данный файл
    import os.path

    try:
        note_name_edit = input('введите название файла с заметками: ')
        path = f"{note_name_edit}.txt"
        if os.path.isfile(path):
            print('Такой файл с заметками уже существует! ')
            note_text_new = open(f"{note_name_edit}.txt", "w+")
            note_text_edit_new = input('Введите новую заметку в этот файл: ')
            note_text_new.write(note_text_edit_new)
            print(f"Новая заметка {note_name_edit} создана.")
        else:
            print('сорян, такая заметка не найдена')
    except:
        print("Преобразование 'ввод заметки' прошло неудачно")

def delete_note():
    # поиск заданного пользователем файла с заметками и его удаление
    import os

    try:
        note_name_delete = input('введите название файла с заметками: ')
        path = f"{note_name_delete}.txt"
        if os.path.isfile(path):
            os.remove(f"{note_name_delete}.txt")
            print('Файл с заметками удален!')
        else:
            print('сорян, такая заметка не найдена')
    except:
        print("Преобразование 'удаление заметки' прошло неудачно")

# вывод всех заметок пользователя в порядке увеличения символов в них
def display_sorted_notes():
    import os

    try:
        notes = [note for note in os.listdir() if note.endswith(".txt")]
        sorted_notes = sorted(notes, key=len)
        print('это список заметок упорядоченный по названию: \n', sorted_notes)
        sorted_list = sorted(notes, key=lambda n: len(open(n, 'r').read()))
        print('\nэто список заметок упорядоченный по количеству символов в них: \n', sorted_list)
    except:
        print("Преобразование 'вывод всех заметок пользователя в порядке увеличения символов в них' прошло неудачно")

def main():
    import colorama
    from colorama import Fore, Style

    # создадим бесконечный цикл работы с заметками
    while True:
        action = input('Меню выбора действий (нажмите определенную цифру для выбора последующих '
              'действий): ''\n''1 - для создания текстового файла с определенным названием '
              'и текстом заметки.''\n''2 - для вывода на экран содержимого заданной пользователем'
              ' заметки.''\n''3 - для вывода на экран содержимого запрашиваемой пользователем'
              ' заметки и ввода пользователем новой заметки.''\n''4 - для удаления указанной '
              'пользователем заметки.''\n''5 - для упорядочивания заметок по количеству символов '
              'в самих заметках.''\n''n - для выхода выхода из программы без исполнения '
              'действий.''\n''ваш выбор: ').lower()
        if action == '1':
            create_note()
        if action == '2':
            read_note()
        if action == '3':
            edit_note()
        if action == '4':
            delete_note()
        if action == '5':
            display_sorted_notes()
        if action == 'n':
            break
        # если введены любые другие симовлы
        allowed_symbols = "12345n"
        pattern1 = '[{0}]'.format(allowed_symbols)
        if (re.search(pattern1, action)):
            print("Вы молодец!")
        else:
            print("вы сделалили неправильный выбор раздела меню")

        # print('ого, что то пошло не так( попробуте еще раз и сделайте правильный выбор')

        # узнаем желают ли пользователи еще сыграть
        #print('\n')
        print(Fore.RED + 'для дальнейшего продолжения работы с заметками нажмите y/n' + Style.RESET_ALL)
        ans = input().lower()
        if ans == 'n':
            break
main()

