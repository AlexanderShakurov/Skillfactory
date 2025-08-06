import random
import re
import logging
import time



class Player:
    """
        атрибуты
            count_move - количество ходов
            boar_ = ссылка на класс Board
            current_game - словарь со значением имени и типа левого и правого игрока для выбранного режима игры. Ключ - ['left', 'right']
            next_  - 0 или 1  - для переключения игроков между ходами с помощью оператора not
            users_ - словарь со значениями ['left','right'] - для ключа next_. Используется для определения текущего и следующего игрока.

        методы

        make_move - полный цикл хода игрока
            Включает в себя:
                Получение координат клетки очередного хода
                    get_user_coord - от игрока - человека
                        Ручной ввод, проверка корректности.
                    get_comp_coord - от игрока - компьютера
                        Автоматический расчет , случайная выборка свободных клеток, не смежных с уже ранеными или убитыми кораблями.
                Проверка результата попадания в клетку с введенными координатами.
                    check_comp_coord - ввод результата игроком - человеком и его проверка на корректность
                        get_user_answer - форма для ввода ответа игроком
                        check_error_on_user_answer - проверка ответа игрока на корректность, исходя из текущего состояния клеток поля
                    check_user_coord - Расчет и возврат результата игроком - компьютером
                Проверка наступления выигрышной ситуации - все корабли атакуемого игрока уничтожены.
                    Board.check_win - метод класса Board
        метод first_player - определение ,кто первый ходит
        метод input_  - отформатированная нижняя строка экрана для ввода значений
        метод footer_ - нижняя строка экрана с временной задержкой. Для просмотра форм экрана, не требующих ввода .
        """


    def __init__(self, users_=None, next_=None, msg_list=None, count_move=0, board_=None):
        game_list = {'01': {'left': ['0', 'Компьютер'], 'right': ['1', 'Игрок']},
                     '00': {'left': ['0', 'Игрок-1'], 'right': ['0', 'Игрок-2']},
                     '10': {'left': ['1', 'Игрок'], 'right': ['0', 'Компьютер']}}

        self.count_move = count_move
        self.board_ = board_

        self.current_game = game_list[board_.type_game]
        self.next_, self.users_ = self.first_player()


    def first_player(self):  # Определяем, чей первый ход
        logging.info(f"{self.board_}")

        a = random.choice([1, 0])
        b = not a
        s = {1: 'left', 0: 'right'}

        logging.info(f" Первый ход игрока {self.current_game[s[a]][1]}")
        self.board_.msg_list = ['' for i in range(self.board_.size_map)]
        msg_1 = f"Левое поле: {self.current_game['left'][1]}"
        msg_1 = f"{msg_1:<24}"
        msg_2 = f"Правое поле: {self.current_game['right'][1]}"
        msg_2 = f"{msg_2:>24}"
        self.board_.msg_list[0] = f"""{msg_1}{msg_2}"""
        msg_3 = f"""Первый ход делает - {self.current_game[s[a]][1]}"""
        msg_3 = f"{msg_3:^48}"
        self.board_.msg_list[2] = f"""{msg_3}"""

        self.board_.paint_board(self.board_.msg_list)
        self.footer_(2)
        # time.sleep(2)
        # print()
        return a, s

    def input_(self, text_):
        # m_ = "Введите свой выбор XY__:"
        l_text = len(text_)
        l = self.current_game['left'][1]
        r = self.current_game['right'][1]
        m = input(f"{' ' * 2}{l:<13}{' ' * 8}{r:<13}{' ' * 8}{text_:<{len(text_)}}")
        return m

    def footer_(self, time_):
        l = self.current_game['left'][1]
        r = self.current_game['right'][1]
        print(f"{' ' * 2}{l:<13}{' ' * 8}{r:<13}{' ' * 8}", end='')
        time.sleep(time_)
        print()

    def make_move(self, board_):
        logging.info(f"{self.board_.msg_list[0]}")

        type_player = self.current_game[self.users_[self.next_]][0]
        type_next_player = self.current_game[self.users_[not self.next_]][0]
        self.count_move += 1

        # 1 Получение координат хода
        while True:
            if type_player == '1':  # Ручной ввод игроком

                msg = ['' for i in range(self.board_.size_map)]
                msg[0] = f"Ходит {self.current_game[self.users_[self.next_]][1]}"

                msg[1] = f"Введите координаты XY"

                msg[2] = f"X - по вертикали"
                msg[3] = f"Y - по горизонтали"
                msg[4] = f"Q - выход"

                msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                self.board_.paint_board(msg)

                quit_game, x, y = self.get_user_coord(board_)
                self.board_.msg_list = ['' for i in range(self.board_.size_map)]
                self.board_.msg_list[0] = f"Ход {self.current_game[self.users_[self.next_]][1]} - ({x + 1},{y + 1})"

                self.board_.msg_list = [f"{self.board_.msg_list[i]:<48}" for i in range(self.board_.size_map)]

                logging.info(f" Ход игрока {self.users_[self.next_]}, тип {board_.gamers[self.users_[self.next_]]}")

                if quit_game:
                    msg = f"Игра прервана игроком {self.users_[self.next_]}"
                    self.board_msg_list = ['' for i in range(self.board_.size_map)]
                    self.board_msg_list[2] = f"{'Игра завершена':^48}"
                    self.board_.paint_board(self.board_msg_list)
                    return True, msg

            else:  # Автоматические координаты от компьютера
                quit_game, x, y = self.get_comp_coord(board_)
            msg0 = self.board_.msg_list[0]
            self.board_.msg_list = ['' for i in range(self.board_.size_map)]

            self.board_.msg_list[0] = f"Ход {self.current_game[self.users_[self.next_]][1]} - ({x + 1},{y + 1})"

            self.board_.msg_list = [f"{self.board_.msg_list[i]:<48}" for i in range(self.board_.size_map)]

            # self.board_.paint_board(msg)

            logging.info(f"Получены координаты , игрок {self.users_[self.next_]} - ({x},{y})")
            logging.info(f" type_next_player = {type_next_player}")

            # Ответ игрока2 на ход игрока1
            if type_next_player == '1':  # Ручной ответ от соперника user

                res_move = self.check_comp_coord(x, y, board_)
                if res_move:  # Ход принят, возвращен результат

                    board_.update_user_map(res_move, x, y,
                                           self.users_[not self.next_])  # Компьютер обновляет карту user
                    msg0 = self.board_.msg_list[0]
                    self.board_.msg_list = ['' for i in range(self.board_.size_map)]
                    msg1 = f"Ответ {self.current_game[self.users_[not self.next_]][1]} - {res_move}"
                    self.board_.msg_list[0] = f"{msg0:<24}{msg1:<24}"
                    self.board_.msg_list = [f"{self.board_.msg_list[i]:<48}" for i in range(self.board_.size_map)]


                    break
                else:  # Ход не принят. Координаты уже использованы ранее
                    self.board_.msg_list[5] = f"{'Такой ход уже был, введите координаты заново':<48}"
                    pass

            else:  # Автоматический ответ компьютера и обновление карты comp
                res_move = self.check_user_coord(x, y, board_)
                if res_move:  # Ход принят, возвращен результат
                    msg0 = self.board_.msg_list[0]
                    self.board_.msg_list = ['' for i in range(self.board_.size_map)]
                    msg1 = f"Ответ {self.current_game[self.users_[not self.next_]][1]} - {res_move}"
                    msg0 = f"{msg0:<24}"
                    msg1 = f"{msg1:<24}"
                    self.board_.msg_list[0] = msg0[:24] + msg1
                    # self.board_.msg_list[0] = f"{msg1}"

                    self.board_.msg_list = [f"{self.board_.msg_list[i]:<48}" for i in range(self.board_.size_map)]
                    logging.info(f" self.board_.msg_list[0] = {self.board_.msg_list[0]}")
                    break
                else:  # Ход не принят. Координаты уже использованы ранее
                    self.board_.msg_list[5] = f"{'Такой ход уже был, введите координаты заново':<48}"
                    pass

        logging.info(f"Получен ответ от игрока {self.current_game[self.users_[not self.next_]][1]} - {res_move}")
        logging.info(f" self.board_.msg_list[0] = {self.board_.msg_list[0]}")
        self.board_.paint_board(self.board_.msg_list)
        self.footer_(2)



        # Проверяем, не уничтожены ли все корабли у следующего игрока.

        if board_.check_win(self.users_[not self.next_]):
            msg = f"Игра закончена, победил игрок {self.users_[self.next_]}. Всего сделано :{self.count_move} ходов"

            self.board_.msg_list = ['' for i in range(self.board_.size_map)]
            self.board_.msg_list[1] = f"{'Игра завершена':^48}"
            m = f"Выиграл {self.current_game[self.users_[self.next_]][1]}"
            self.board_.msg_list[2] = f"{m:^48}"
            m = f"Сделано {self.count_move} ходов"
            self.board_.msg_list[3] = f"{m:^48}"
            self.board_.paint_board(self.board_.msg_list)
            self.footer_(2)
            return True, msg

        self.next_ = not self.next_
        return False, ''

    def get_comp_coord(self, board):  # Рассчет координат компьютером
        # time.sleep(0.5)
        key_ = self.users_[not self.next_]  # Следующий игрок
        key_present = self.users_[self.next_]
        s = []

        for i in range(board.size_map):
            for j in range(board.size_map):
                if board.board_map[key_][i][j].status_ in ['free', 'busy']:
                    logging.info(
                        f" Проверяем точку board.board_map[{key_}][{i}][{j}].status_ = {board.board_map[key_][i][j].status_}  на соседство с ранеными или убитыми кораблями")

                    m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (1, -1), (1, 1)]
                    m2 = board.check_dot(i, j, ['killed'], m1,
                                         board.board_map[key_])  # Проверка на все соседние "убитые" точки

                    m3 = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    m4 = board.check_dot(i, j, ['X'], m3,
                                         board.board_map[key_])  # Проверка на  соседние диагональные "раненые"
                    if not (m2 and m4):  # flag:
                        s.append((board.board_map[key_][i][j].x, board.board_map[key_][i][j].y))
                        # logging.info(f" В список точек хода компа добавлена ({board.user_map[i][j].x},{board.user_map[i][j].y})")

        logging.info(f" список свободных ячеек для хода comp {s}")
        random_dot_move = random.choice(s)
        # dot_move_row_ = random_dot_move[0] + 1
        # dot_move_col_ = random_dot_move[1] - board.size_map + 1
        dot_move_row_ = random_dot_move[0]
        dot_move_col_ = random_dot_move[1]
        logging.info(f" Ход игрока {key_present} ({dot_move_row_},{dot_move_col_})")

        return True, dot_move_row_, dot_move_col_


    def get_user_coord(self, board):
        # Ход игрока

        logging.info(f"Ход игрока")
        # board.
        text_ = "Введите значение: "
        # self.board_.input_(text_)
        while True:


            m = self.input_(text_)
            m1 = re.match(r'([Qq]$)|(\d{1})\W*(\d{1})', m)
            if m1:
                logging.info(f" {m1.group(1), m1.group(2), m1.group(3)}")
                if m1.group(1):

                    logging.info(f" Игра прервана.")

                    return True, 0, 0
                else:

                    x = int(m1.group(2)) - 1
                    y = int(m1.group(3)) - 1

                    if (x in range(board.size_map)) and (y in range(board.size_map)):
                        status_dot = self.board_.board_map[self.users_[not self.next_]][x][y].status_

                        if status_dot not in ['free', 'busy']:
                            msg = ['' for i in range(self.board_.size_map)]
                            msg[0] = f"Ошибка. Такой ход уже был."
                            msg[1] = f"Повторите ввод"
                            msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                            self.board_.paint_board(msg)
                            logging.error(f" Такой ход уже был, повторите ввод")
                            logging.error(
                                f"self.board_.board_map[self.users_[self.next_]][{x}][{y}].status_ = {status_dot}")

                        else:
                            logging.info(f" Ход  {self.users_[self.next_]} ({x},{y})")
                            msg = ['' for i in range(self.board_.size_map)]
                            msg[0] = f"{self.current_game[self.users_[self.next_]][1]} - ({x + 1},{y + 1})"

                            msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                            self.board_.msg_list = msg


                            return False, x, y

                    else:
                        msg = ['' for i in range(self.board_.size_map)]
                        msg[0] = f"Ошибка.Координаты вне границ поля."

                        msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                        self.board_.paint_board(msg)
                        logging.error(f" Координаты вне диапазона поля, повторите ввод ")

            else:
                logging.error(f" неверные координаты {m}")

                msg = ['' for i in range(self.board_.size_map)]
                msg[0] = f"Ошибка. Недопустимые символы."

                msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                self.board_.paint_board(msg)

    def check_user_coord(self, x, y, board_):  # Проверка введенных координат user

        dot_ = board_.board_map[self.users_[not self.next_]]
        logging.info(f" start ({x},{y}) - {dot_[x][y].status_}")

        if dot_[x][y].status_ == 'free':
            result = 'Мимо'

            dot_[x][y].status_ = 'T'
            logging.info(f" dot_[{x}][{y}].status_ = 'T'")
        elif dot_[x][y].status_ == 'busy':
            logging.info(f" dot_[x][y].status_ == 'busy'")
            try:
                ship_ = dot_[x][y].ship
                ship_.life_ -= 1
                ship_life = ship_.life_
                logging.info(
                    f" проверка объект ship {ship_}, life {ship_.life_}, {ship_.long}, dot_[{x}][{y}] {dot_[x][y].ship}")
            except Exception as er:
                logging.error(f"Ошибка ship_= dot_[x][y].ship или ship_life = ship_.life: {er}")
            logging.info(f" ship_ = {ship_}, ship_life = {ship_life}")
            if ship_life > 0:
                result = 'Ранен'
                dot_[x][y].status_ = 'X'
                logging.info(f" dot_[{x}][{y}].status_ = 'X'")
            else:
                result = 'Убит'
                row0 = ship_.row_
                col0 = ship_.col_
                direct_ = ship_.direction
                for i in range(ship_.long):
                    x = row0 + (0 if direct_ == 'H' else i)
                    y = col0 + (0 if direct_ == 'V' else i)
                    dot_[x][y].status_ = 'killed'
                logging.info(f" dot_[{x}][{y}].status_ = 'Убит'")
        else:
            logging.info(f"Такой ход уже был, dot_[{x}][{y}].status_ = {dot_[{x}][{y}].status_}")
            self.board_msg_list[5] = f"{'Ошибка.Такой ход уже был':<48}"

            self.board_.paint_board(self.board_.msg_list)
            result = False
        logging.info(f"Результат хода - {result}")

        return result

    def check_comp_coord(self, x, y, board_):  # Получение от user результата хода comp
        m1 = {'1': 'Мимо', '2': 'Ранен', '3': 'Убит'}
        m2 = {'1': 'T', '2': 'X', '3': 'Убит'}
        logging.info(f"board_= {board_}")
        while True:

            r = self.get_user_answer()  # получение ручного ответа от user
            res = m1[r.group()]

            if res:
                logging.info(f"ответ игрока {self.users_[not self.next_]}: {res}")

                res11, msg11 = self.check_error_on_user_answer(board_, res, x, y)
                logging.info(f" Результат проверки user's answer {res11},{msg11}")

                if res11:

                    msg0 = self.board_.msg_list[0][:24]
                    msg1 = f"Ответ {self.current_game[self.users_[not self.next_]][1]} - {res}"
                    self.board_.msg_list = ['' for i in range(self.board_.size_map)]
                    self.board_.msg_list[0] = f"{msg0:<24}{msg1:<24}"

                    return res

                else:

                    logging.info(f" Ответ user {msg11}")
                    self.board_.msg_list[5] = f"{msg11:<48}"
                    self.board_.paint_board(self.board_.msg_list)
                    self.footer_(2)

            else:
                logging.info(f"некорректный выбор ответа")

                self.board_.msg_list[5] = f"{'Ошибка.Некорректный выбор ответа':<48}"
                self.board_.paint_board(self.board_.msg_list)

    def get_user_answer(self):
        msg_1 = self.board_.msg_list[0]
        while True:

            self.board_.msg_list[1] = f"{'Введите результат хода.':<48}"
            self.board_.msg_list[2] = f"{'1 - мимо':<48}"
            self.board_.msg_list[3] = f"{'2 - ранен':<48}"
            self.board_.msg_list[4] = f"{'3 - убит':<48}"

            self.board_.paint_board(self.board_.msg_list)
            m = self.input_("Результат: ")


            res = re.match(r'([1-3]{1})', m)

            if not res:
                self.board_.msg_list[5] = f"{'Ошибка. Некорректный ответ.':<48}"
                logging.info(f"некорректный выбор ответа")

            else:

                logging.info(f" принят корректный ответ user {res.group()}")
                return res

    def check_error_on_user_answer(self, board_, res, x, y):  # Проверяем ответ user на корректность
        row_ = x
        col_ = y
        # m = res.group()
        logging.info(
            f"Проверяем ответ {res} игрока {self.current_game[self.users_[not self.next_]][1]}  на ход игрока {self.current_game[self.users_[self.next_]][1]} ({x},{y})")
        logging.info(f" board = {board_})")
        dots_list = self.board_.board_map[self.users_[not self.next_]]

        if res == 'Мимо':

            return True, ''


        elif res == 'Ранен':  # Ранен
            logging.info(f"Обработка ответа Ранен от user ")

            logging.info(f"Поиск среди соседних клеток раненых и убитых ")
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = board_.check_dot(row_, col_, ['X', 'killed'], m1, dots_list)
            if len(m2) > 1:
                msg = "Некорректный ответ. У раненой клетки не может быть более 1 соседней клетки с кораблем"
                logging.info(msg)

                return False, msg

            logging.info(f"Поиск среди соседних диагональных клеток раненых или убитых ")
            m1 = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
            m2 = board_.check_dot(row_, col_, ['X', 'killed'], m1, dots_list)
            if m2:
                msg = "Некорректный ответ. У раненой клетки не может быть диагональной соседней клетки с кораблем"
                logging.info(msg)

                return False, msg

            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = board_.check_dot(row_, col_, ['X'], m1, dots_list)

            if m2:
                logging.info(f"Найдена соседняя раненая точка {m2} ")
                row_2, col_2 = m2[0][0], m2[0][1]

                ship_damaged = dots_list[row_2][col_2].ship
                if ship_damaged.long == 2:
                    msg = f"Некорректный ответ. Три подряд раненые клетки - это должен быть убитый корабль."
                    logging.error(msg)
                    return False, msg

        # elif m == '3':  # Убит
        elif res == 'Убит':  # Убит

            dots_list[row_][col_].status_ = 'killed'
            logging.info(f"Обработка ответа Убит от user ")
            logging.info(f"Проверяем корректность ответа ")
            logging.info(f"Ищем соседнюю убитую клетку ")
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = board_.check_dot(row_, col_, ['killed'], m1, dots_list)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть  соседней клетки с убитым кораблем"
                logging.info(msg)

                return False, msg

            logging.info(f"Ищем соседнюю по диагонали раненую или убитую клетку ")
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = board_.check_dot(row_, col_, ['X', 'killed'], m1, dots_list)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть диагональной соседней клетки с кораблем"
                logging.info(msg)

                return False, msg

        return True, ''

