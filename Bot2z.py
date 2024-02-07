# выполненное первое и второе задания
def draw_board(board):
    from colorama import Fore, Back, Style
    # запустить цикл, который проходит по всем элементам поля, проверяет их значение
    # и в зависимости от ихзначчений раскрашивает пустую ячейку в желтый цвет, 'X' в красный,
    # '0' в синиц
    for x in range(3):
        for y in range(3):
            if board[x][y] == " ":
                if y < 2:
                    print(Back.YELLOW + board[x][y] + Style.RESET_ALL, "| ", end='')
                else:
                    print(Back.YELLOW + board[x][y] + Style.RESET_ALL, "| ")
            elif board[x][y] == "X":
                if y < 2:
                    print(Fore.RED + 'X' + Style.RESET_ALL, "| ", end='')
                else:
                    print(Fore.RED + 'X' + Style.RESET_ALL, "| ")
            elif board[x][y] == "0":
                if y < 2:
                    print(Fore.BLUE + '0'  + Style.RESET_ALL, "| ", end='')
                else:
                    print(Fore.BLUE + '0'  + Style.RESET_ALL, "| ")
        print("---------")

def ask_and_make_move(player, board):
    x, y = ask_move(player, board)
    make_move(player, board, x, y)

def ask_move(player, board):
    from colorama import Fore, Back, Style
    x, y = input(f"Игрок {player}, введите координаты клетки на поле (цифры вводить через пробел): ").strip().split()
    # преобразовать координаты в целые числа
    x, y = int(x), int(y)
    # задать условие, которое проверяет,
    # находится ли координата в пределах поля и свободно ли место
    if (0 <= x <= 2) and (0 <= y <= 2) and board[x][y] == " ":
        return (x, y)
    else:
        print ('место занято, либо вы сходили вне поля. введите координаты снова')
        return ask_move(player, board)

def make_move(player, board, x, y):
    from colorama import Fore, Back, Style
    # записать значение игрока (Х или 0) в ячейку
    if player == 'X':
        board[x][y] = 'X'
    elif player == '0':
        board[x][y] = '0'

def check_win(player, board):
    # проверяем выигрышные комбинации
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def tic_tac_toe():
    while True:
        board = [[" " for i in range(3)] for j in range(3)]
        player = "X"
        # задать бесконечнный цикл, который проводит конкретную игру
        while True:
            draw_board(board)
            ask_and_make_move(player, board)
            # проверка на победу
            if check_win(player, board):
                print(f"Ура!! Игрок {player} победил!")
                break
            # проверка на наличие свободных ячеек
            tie_game = True
            for row in board:
                for col in row:
                    if col != " ":
                        tie_game = False
            if tie_game:
                break
            if player == "X":
                player = "0"
            else:
                player = "X"
        # узнаем желают ли польователи еще сыграть
        print('для дальнейшего продолжения игры нажмите y/n')
        ans = input().lower()
        if ans == 'n':
            break
tic_tac_toe()




