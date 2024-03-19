# выполненное третье задание
def build_note(note_text, note_name):
    # проверим существует ли файл с заданным названием, если нет то создаем новый,
    # если да - то заменим его на новую заметку
    try:
        file = open(f"{note_name}.txt", "r+", encoding = "utf-8")
    except IOError:
        file = open(f"{note_name}.txt", "w+", encoding = "utf-8")
    file.write(note_text)
    print(f"Заметка {note_name} создана.")

def create_note():
    # создадим файл с заметками
    note_name = input('введите название файла с заметками: ')
    note_text = input('введите текст заметки: ')
    build_note(note_text, note_name)

def read_note():
    # поиск заданного пользователем файла с заметками и вывод текста заметки
    import os.path

    note_name_read = input('введите название файла с заметками: ')
    path = f"{note_name_read}.txt"
    if os.path.isfile(path):
        with open(f"{note_name_read}.txt", 'r') as file:
            lines = file.read()
        print('это сам текст данной заметки: ', lines)
    else:
        print('сорян, такая заметка не найдена')

def edit_note():
    # поиск заданного пользователем файла с заметками и ввод новой заметки в данный файл
    import os.path

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

def delete_note():
    # поиск заданного пользователем файла с заметками и его удаление
    import os

    note_name_delete = input('введите название файла с заметками: ')
    path = f"{note_name_delete}.txt"
    if os.path.isfile(path):
        os.remove(f"{note_name_delete}.txt")
        print('Файл с заметками удален!')
    else:
        print('сорян, такая заметка не найдена')

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
              'пользователем заметки.''\n''n - для выхода выхода из программы без исполнения '
              'действий.''\n''ваш выбор: ').lower()
        if action == '1':
            create_note()
        if action == '2':
            read_note()
        if action == '3':
            edit_note()
        if action == '4':
            delete_note()
        if action == 'n':
            break
        # узнаем желают ли польователи еще сыграть
        #print('\n')
        print(Fore.RED + 'для дальнейшего продолжения работы с заметками нажмите y/n' + Style.RESET_ALL)
        ans = input().lower()
        if ans == 'n':
            break
main()







