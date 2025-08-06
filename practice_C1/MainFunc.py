from Board import Board
from Player import Player




def main_func():

    board_long = 6 # Задаем размерность полей
    ships_list =[(1,4), (2,2), (3,1)] # ключ - длина корабля, значение - количество кораблей этой длины

    board_ = Board(size_map = board_long, ships_list = ships_list)
    player_ = Player(board_ = board_)

    while True:

        quit_game, msg = player_.make_move(board_)
        if quit_game:
            return True





if __name__ == '__main__':

    main_func()
