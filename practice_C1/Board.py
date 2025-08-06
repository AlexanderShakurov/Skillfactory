
import random
import re
import logging
import time
from Ship import Ship
from dot import Dot


class Board:

    """
    атрибуты
        
    """

    def __init__(self, size_map, ships_list,  type_game='00',
                 gamers_name=None, board_map=None, ships=None, player_=None):

        self.player_ = player_
        self.type_game = type_game
        self.size_map = size_map  # Размерность игрового поля
        self.ships_list = ships_list  # Список кораблей, длина:количество

        self.board_map = self.board_map_init()

        self.type_game = self.invite_to_start()

        self.gamers = {'left': self.type_game[0], 'right': self.type_game[1]}
        self.board_map = self.board_map_init()
        self.ships = self.create_ships()
        self.gamers_name = {'0': "Компьютер", '1': "Игрок"}

    def board_map_init(self):
        s = {}

        s['left'] = [[Dot(j, i) for i in range(0, self.size_map)] for j in range(0, self.size_map)]
        s['right'] = [[Dot(j, i) for i in range(0, self.size_map)] for j in range(0, self.size_map)]
        return s

    def paint_board(self, msg_list):  # рисует весь экран, кроме нижней строки
        logging.info(f"{msg_list[0]}")
        char_ = {}
        char_['00'] = {'free': "◯", 'busy': "△", 'X': 'X', 'T': 'T', 'killed': '■'}
        char_['01'] = {'free': "◯", 'busy': "◯", 'X': 'X', 'T': 'T', 'killed': '■'}
        char_['10'] = {'free': "◯", 'busy': "◯", 'X': 'X', 'T': 'T', 'killed': '■'}

        # board0 = '   1 2 3 4 5 6   --     1 2 3 4 5 6 '
        t = f"{' ' * 3}"
        for i in range(1, self.size_map + 1):
            t += f"{i} "
        title = f"{t}{' ' * 6}{t}"
        title2 = f"""{' ' * 8}{"Игра 'Морской' бой":^50}"""
        print(f"{title}{title2}")
        # board0 = '  -------------  --    -------------'
        board0 = f"{' ' * 2}{'-' * 13}{' ' * 8}{'-' * 13}"
        board01 = f"{' ' * 8}{'-' * 50}"
        print(board0 + board01)
        count_row = 1

        for i in range(self.size_map):
            board_left, board_right = f"{count_row} |", f"{count_row} |"

            for j in range(self.size_map):
                board_left += char_[self.type_game][self.board_map['left'][i][j].status_] + '|'


                board_right += char_[self.type_game][self.board_map['right'][i][j].status_] + '|'

            count_row += 1

            if count_row - 1 <= len(msg_list):
                msg = f"{msg_list[count_row - 2]}"

            else:
                msg = f"{' ' * 48}"

            msg = f"{msg}" if msg else f"{' ' * 48}"
            m = f"{board_left}  --  {board_right}{' ' * 8}{'|'}{msg[:48]}{'|'}"

            print(m)

        print(board0 + board01)


        return True

    def input_(self, text_):

        m = input(f"{' ' * 2}{' ' * 13}{' ' * 8}{' ' * 13}{' ' * 8}{text_:<{len(text_)}}")
        return m

    def invite_to_start(self):
        # paint_board(self, msg_list)
        msg = [' ' * 24 for _ in range(self.size_map)]
        msg_ = [' ' * 24 for _ in range(self.size_map)]
        ############ Первый экран - правила
        msg[0] = f"""{'Обозначение клеток:':<24}"""
        msg[1] = f"""{"Свободная :'◯'":<48}"""
        msg[2] = f"""{"Ранен:'X'":<48}"""
        msg[3] = f"""{"Убит:'■'":<48}"""
        msg[4] = f"""{"Ход мимо:'T'":<48}"""
        msg[5] = f"""{"Корабль противника:'△'":<48}"""
        msg_[0] = f"""{'Корабли на поле:':<24}"""
        msg[0] += msg_[0]
        for i in range(len(self.ships_list)):
            logging.info(f"{self.ships_list[i]}")
            long_ = self.ships_list[i][0]  # '⚫'*
            cnt_ = self.ships_list[i][1]
            msg_[i + 1] = f"""длина {long_} - {cnt_} ед."""

            msg[i + 1] = msg[i + 1][:24] + f"{msg_[i + 1]:24}"

        self.paint_board(msg)
        m = self.input_('Для продолжения нажмите Enter')

        msg = ['' for _ in range(self.size_map)]

        msg[0] = f"""{"Введите режим игры, в формате 'DD'":<48}"""
        msg[1] = f"""{"Игра против компьютера: ":<48}"""

        msg[2] = f"""{"Левое поле игрока: '10'":<24}{"Правое поле игрока: '01'":>24}"""

        msg[4] = f"""{"Демо игра - компьютер против компьютера '00'":<48}"""

        logging.info("Приглашение к началу игры")
        while True:
            self.paint_board(msg)
            m = self.input_('Введите режим игры: ')

            res = re.match(r'([0,1])\W*([0,1])', m)

            if res:


                logging.info(f"Выбрана игра {res.group(1)}-{res.group(2)}")

                return f"{res.group(1)}{res.group(2)}"
            else:

                msg[5] = f"Ошибка.Введены некорректные символы."

    def create_ships(self):
        logging.info(f" gamers: {self.gamers}")
        ships = {}
        for k, v in self.gamers.items():
            logging.info(f"создаем корабли для пользователя {k}-{v}")

            if v == '1':  # - тип user
                ships[k] = self.create_ships_user()

            else:
                ships[k] = self.create_ships_comp(k)

        return ships

    def create_ships_user(self):  # создаем объекты кораблей user
        ships_list1 = sorted(self.ships_list, reverse=True)
        ships_user = {}
        for i in ships_list1:
            for j in range(i[1]):
                # ships_user[f"{i[0]}-{j}"] = Ship(i[0])
                ships_user[f"{i[0]}-{j}"] = Ship(None)
        return ships_user

    def create_ships_comp(self, v):  # создаем объекты кораблей comp и размещаем их на карте

        ships_comp = {}  # Словарь из всех созданных объектов кораблей компьютера
        ships_list1 = sorted(self.ships_list, reverse=True)
        count_try = 1  # номер попытки размещения кораблей. Для отладки
        while True:
            # Очищаем все точки доски comp
            for i in range(0, self.size_map):
                for j in range(0, self.size_map):
                    self.board_map[v][i][j].status_ = 'free'
            res = []
            for i in ships_list1:
                for j in range(i[1]):

                    ships_comp[f"{i[0]}-{j}"] = Ship(i[0], life_=i[0])
                    res1, res2, res3, res4 = ships_comp[f"{i[0]}-{j}"].find_free_place_new2(self.board_map[v],
                                                                                            self.size_map, self)

                    if res1:

                        self.board_map[v] = self.place_the_ship(ships_comp[f"{i[0]}-{j}"], self.board_map[v])
                    res.append(res1)

            if all(res):

                return ships_comp
            else:

                count_try += 1

    def place_the_ship(self, ship, dots_list):  # записываем координаты точек корабля в объекты точек
        # s =[]
        row_ = ship.row_
        col_ = ship.col_

        for i in range(ship.long):
            row1_ = row_ + i if ship.direction == 'V' else row_
            col1_ = col_ + i if ship.direction == 'H' else col_

            dots_list[row1_][col1_].status_ = 'busy'
            dots_list[row1_][col1_].ship = ship

        return dots_list

    def check_dot(self, x, y, status_dot, m1, dots_list):


        s = []
        for l in range(len(m1)):
            row0 = x + m1[l][0]
            col0 = y + m1[l][1]

            # try:
            if (row0 in range(self.size_map)) and (col0 in range(self.size_map)):
                m2 = dots_list[row0][col0].status_
                # logging.info(f" dots_list[{row0}][{col0}].status_ = {m2}")

                if m2 in status_dot:
                    # logging.info(f" Найдена соседняя  клетка {status_dot} ({row0},{col0})")

                    s.append((row0, col0))

        return s

    def check_line_dots(self, row_, col_, direct, long, dots_list):
        # logging.info(f"проверяем ({row_},{col_}) для {long} - {direct} - {dots_list}")
        m1 = [(-1, - 1), (-1, 0), (-1, 1), (0, - 1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(long):
            row_i = row_ + (i if direct == 'V' else 0)
            col_i = col_ + (i if direct == 'H' else 0)

            if dots_list[row_i][col_i].status_ == 'free':
                if long == 1:
                    m1 = [(-1, - 1), (-1, 0), (-1, 1), (0, - 1), (0, 1), (1, -1), (1, 0), (1, 1)]
                else:

                    if direct == 'H':

                        if i == 0:  # начальная точка корабля

                            m1 = [(-1, - 1), (-1, 0), (-1, 1), (0, - 1), (1, -1), (1, 0), (1, 1)]

                        elif i == long - 1:  # конечная точка корабля
                            m1 = [(-1, - 1), (-1, 0), (-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]
                        else:  # средняя точка корабля
                            m1 = [(-1, 0), (0, 1)]

                    else:  # Вертикально направление

                        if i == 0:

                            m1 = [(-1, - 1), (0, -1), (1, - 1), (-1, 1), (0, 1), (1, 1), (-1, 0)]

                        elif i == long - 1:
                            m1 = [(-1, - 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

                        else:
                            m1 = [(-1, 0), (0, 1)]

                # logging.info(f"m1 = {m1}")
                res1 = self.check_dot(row_i, col_i, ['busy'], m1, dots_list)
                if res1:  # если в окружении найдена хоть одна занятая точка
                    return False
            else:  # рассматриваемая точка занята
                return False
        # logging.info(f"контроль({row_},{col_}) подходит для {long} - {direct} - {dots_list}")
        return True

    def update_user_map(self, res, x, y, gamer_name):  # Обновление dot, ship, board по результату хода comp
        # 04.08.25
        row_ = x
        col_ = y
        # m = res.group()
        dots_list = self.board_map[gamer_name]
        logging.info(f"Обновление карты user после хода {gamer_name}  ({x},{y}) - {res}")

        # if m == '1':  # Ход мимо
        if res == 'Мимо':  # Ход мимо
            dots_list[row_][col_].status_ = 'T'

        elif res == 'Ранен':
            # elif m == '2':  # Ранен
            logging.info(f"Обработка ответа Ранен от user ")
            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1, dots_list)

            if m2:
                logging.info(f"Найдена соседняя раненая точка {m2} ")
                row_2, col_2 = m2[0][0], m2[0][1]

                ship_damaged = dots_list[row_2][col_2].ship

                dots_list[row_][col_].status_ = 'X'
                ship_damaged.long += 1
                dots_list[row_][col_].ship = ship_damaged
                logging.info(f"Получаем ссылку на корабль из соседней раненой клетки {ship_damaged} ")
            else:

                logging.info(f"Cоседняя раненая точка не найдена,  {m2} ")
                logging.info(f" Присваиваем свободный корабль точке {row_}, {col_}")
                for k, v in self.ships[gamer_name].items():
                    logging.info(f" {v.long}")
                    if not v.long:
                        ship_damaged = v
                        ship_damaged.long = 1
                        dots_list[row_][col_].status_ = 'X'
                        dots_list[row_][col_].ship = ship_damaged
                        logging.info(f" точке ({row_}{col_}) присвоен корабль {ship_damaged}")
                        break


                logging.info(f"Выбран неиспользуемый корабль {ship_damaged}")

        elif res == 'Убит':


            dots_list[row_][col_].status_ = 'killed'
            logging.info(f"Обработка ответа Убит от user ")
            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1, dots_list)

            if m2:
                if len(m2) == 2:

                    logging.info(f"Найдено 2 соседние раненые точки {m2} ")
                    row_2, col_2 = m2[0][0], m2[0][1]
                    row_3, col_3 = m2[1][0], m2[1][1]
                    dots_list[row_2][col_2].status_ = 'killed'
                    dots_list[row_3][col_3].status_ = 'killed'
                    ship_killed = dots_list[row_2][col_2].ship
                    ship_repaired = dots_list[row_3][col_3].ship  # один из кораблей освобождается от привязки к точке
                    dots_list[row_][col_].ship = ship_killed
                    dots_list[row_2][col_2].ship = ship_killed
                    dots_list[row_3][col_3].ship = ship_killed
                    ship_killed.life_ = 0
                    ship_killed.long = 3
                    ship_repaired.life = None

                elif len(m2) == 1:
                    logging.info(f"Найдена 1 смежная раненая точка {m2} ")
                    row_2, col_2 = m2[0][0], m2[0][1]
                    dots_list[row_2][col_2].status_ = 'killed'

                    ship_killed = dots_list[row_2][col_2].ship
                    logging.info(f" ship_killed = {ship_killed}")
                    if ship_killed.long == 2:
                        ship_killed.long = 3
                        ship_killed.life = 0
                        delta_row = row_ - row_2
                        delta_col = col_ - col_2
                        row_3 = -2 * (delta_row) + row_
                        col_3 = -2 * (delta_col) + col_
                        logging.info(f" Длина убитого корабля 3, третья точка ({row_3},{col_3}")
                        dots_list[row_3][col_3].status_ = 'killed'
                    if ship_killed.long == 1:
                        ship_killed.long = 2
                        ship_killed.life = 0
                        logging.info(f" Длина убитого корабля 2")
                else:
                    logging.info(f"Cоседняя раненая клетка не найдена,  {m2} ")
                    logging.info(f" Присваиваем  свободный корабль точке {row_}, {col_}")
                    for k, v in self.ships[gamer_name].items():
                        logging.info(f" {v.long}")
                        if not v.long:
                            ship_killed = v
                            ship_killed.long = 1
                            ship_killed.life = 0
                            dots_list[row_][col_].ship = ship_killed
                            break


                logging.info(f"Выбран неиспользуемый корабль {ship_killed}")

        # input(f"{__LINE__}: контроль обработки ответа user")
        return True, ''

    def check_win(self, next_player_):  # Проверка на все убитые корабли
        # current_player_ in ['left', 'right']
        for k, v in self.ships[next_player_].items():
            logging.info(f" {k}.life = {v.life_}")
            if (v.life_ is None) or (v.life_ > 0):
                logging.info(f" {k}.life = {v.life_}")
                return False
        return True