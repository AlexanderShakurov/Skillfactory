import inspect
import random
import re
import logging

logging.basicConfig(handlers=[logging.FileHandler(filename="./skill.log",
                                                 encoding='utf-8', mode='w')],
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)




class LineNo:
    def __str__(self):
        return (f"{inspect.currentframe().f_back.f_code.co_name}"
                f":{inspect.currentframe().f_back.f_lineno}")


__LINE__ = LineNo()


class Dot:
    """класс точки поля
    x,y - координаты,
    status_ in ['free', 'busy', 'lost', 'goal'}
    free - свободна
    busy - занята кораблем, выстрела по клетке не было (карта компьютера)
    lost - был выстрел мимо в клетку
    goal - был точный выстрел

    """

    def __init__(self, x, y, status_ ='free', ship = None) :

        self.x = x
        self.y = y
        self.status_ = status_  # free - свободна, busy - занята, T - было холостое попадание, X - было точное попадание
        self.ship = ship    # ссылка на объект корабля, который занимает точку



class Board:

    

    def __init__(self, size_map, ships_list):
        self.size_map= size_map
        self.ships_list = ships_list
        self.comp_map = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )] # список точек доски comp
        #logging.info(f"Создан comp_map")
        self.user_map = [[Dot(j, i) for i in range(0 + self.size_map, 2 * self.size_map )] for j in range(0, self.size_map)]
        for j in self.user_map:
            for i in range(0, self.size_map):
                #logging.info(f"user_map = {j.x}, {j.y}, {j.status_}")
                logging.info(f"user_map = {j[i].x}, {j[i].y}, {j[i].status_}")
        logging.info(f"Создан user_map")
        # список точек доски gamer
        self.comp_map = self.create_ships(self.comp_map) # карта компьютера с введенными координатами кораблей
        logging.info(f"В user_map внесены координаты кораблей")

    def create_ships(self, comp_map): # создаем объекты кораблей и размещаем их на карте
        comp_map = [[Dot(j, i) for i in range(0, self.size_map)] for j in
                         range(0, self.size_map)]  # список точек доски comp
        ship= {} # Словарь из всех созданных объектов кораблей компьютера
        ships_list1 = sorted(self.ships_list, reverse=True)
        count_try = 1 # номер попытки создания кораблей. Для теста
        while True:
            #Очищаем все точки доски comp
            for i in range(0, self.size_map):
                for j in range(0, self.size_map):
                    comp_map[i][j].status_ = 'free'
            res = []
            for i in ships_list1:
                for j in range(i[1]):

                    ship[f"{i[0]}-{j}"] = Ship(i[0])
                    res1, res2, res3, res4 = ship[f"{i[0]}-{j}"].find_free_place(comp_map, self.size_map)
                    logging.info(f"ship[{i[0]}-{j}]: {res1},{res2},{res3},{res4}")
                    if res1:
                        #logging.info(f"Найдены координаты для  ship[{i[0]}-{j}] ")
                        comp_map = self.place_the_ship(ship[f"{i[0]}-{j}"], comp_map)
                    res.append(res1)


            if all(res):
                logging.info(f"Все корабли размещены на comp_map")
                return comp_map
            else:
                logging.error(f"Не удалось разместить корабли, повторяем попытку")
                print(f"{__LINE__}: не удалось разместить, попытка {count_try}, повторяем")
                count_try +=1

    def place_the_ship(self, ship, dots_list): # записываем координаты точек корабля в объекты точек
        #s =[]
        row_ = ship.row_
        col_ = ship.col_

        for i in range(ship.long):
            row1_ = row_ + i if ship.direction == 'V'  else row_
            col1_ = col_ + i if ship.direction == 'H'  else col_

            dots_list[row1_][col1_].status_ = 'busy'
            dots_list[row1_][col1_].ship = ship
            logging.info(f" ship(row1_, col1_) ({row1_}, {col1_})")
            #s.append( dots_list[row1_][col1_])
        return dots_list


    def paint_board(self):    # рисует доску по списку с точками
        char_ = {'free':'О', 'busy':'B'}
        board0 = '   1 2 3 4 5 6   --     1 2 3 4 5 6 '
        print(board0)
        board0 = '  -------------  --    -------------'
        print(board0)
        count_row = 1
        # Вставка 30.07.2025
        for i in range(self.size_map):
            board1, board2 = f"{count_row} |", f"{count_row} |"
            for j in range(self.size_map):
                board1 += char_[self.comp_map[i][j].status_] + '|'
                logging.info(f"self.user = {self.user_map[i][j].status_}")
                board2 += char_[self.user_map[i][j].status_] + '|'
            count_row += 1
            print(f"{board1}  --  {board2}")
        return True



    def update_coordinate(self,x,y):


        """обновление координат
           прорисовка поля"
           x,y - очередной ход
           x = 0 , y = 0 - первичное создание поля"""

        pass



    def strike(self, gamer): # Ход игрока или компьютера

        """ gamer in ['comp', 'user']
        x,y  - координаты выстрела
        Проверяет координаты на корректность
        Проверяет координаты на попадание
        Передает координаты update_Board
        Возвращает x, y """
        pass



class Ship:

    def __init__(self, long, direction = None, row_ = None, col_= None):
        self.long = long # длина корабля
        self.direction = direction # направление корабля, H - горизонт, V - вертик.
        self.row_ = row_ # начальная координата (строка)
        self.col_ = col_ # начальная координата (столбец)
        logging.info(f" Создаем ship {long}, {direction}, {row_}, {col_}")
      

    def find_free_place(self, dots_list, size_map):
        # dots_list - текущее состояние точек поля
        """ случайно выбирается тип размещения, H - горизонтальный или V - вертикальный
            и координаты начала корабля"""
        type_boat_index = random.randrange(0, size_map) % 2  # 0 - вертикальный,  не 0 - горизонтальный
        self.direction = 'H' if type_boat_index else 'V'
        s = ['H', 'V'] if type_boat_index else ['V', 'H']

        for self.direction in s: #
            logging.info(f" длина корабля {self.long}, направление {self.direction} ")


            #  Горизонтальное расположение

            s = {}
            """ Идем по очереди, по строкам. Проверяем точки от (col_, row_) до (col_ + long_, row_
            на dot.staus_ == 'free'
            Если все точки 'free', увеличиваем счетчик 
            Если набралось три подряд идущие s[i] = True, отмечаем точку (col_ + 1, row_ + 1) как одну из возможных
            точек начала корабля.
            Добывляем найденную точку в список точек, из которого потом случайным образом будет выбрана одна 
            и присвоена данному экземпляру корабля в качестве начальной."""
            dots_for_start = [] # список возможных точек начала корабля


            if self.direction == 'H'  :
                for i in range(0, size_map - self.long + 1):

                    count_row = 0
                    #for row_ in range (0, size_map ):
                    for j in range (0, size_map ):
                        col_, row_ = i, j


                        list_ = [True if dots_list[row_][col_ + j].status_ == 'free' else False for j in range(self.long)]

                        if col_ == 0 :
                            list_.append(True if dots_list[row_][col_+ self.long ].status_ == 'free' else False )
                        elif col_ == size_map - self.long  :

                            list_.insert(0,True if dots_list[row_][col_ - 1].status_ == 'free' else False)
                        else:
                            list_.append(True if dots_list[row_][col_ + self.long ].status_ == 'free' else False )
                            list_.insert(0, True if dots_list[row_][col_ - 1].status_ == 'free' else False)



                        logging.info (f"{row_},{col_}) - {list_}")

                        if all(list_):

                            if row_ == 0:
                                count_row += 2
                                #logging.info (f"{__LINE__}: row_ = {row_}")
                            elif (row_ == size_map  - 1 ) and count_row > 1:
                                count_row = 4
                                #logging.info (f"{__LINE__}: row_ = {row_}")
                            else:
                                #logging.info (f"{__LINE__}: row_ = {row_}")
                                count_row  += 1
                            #logging.info (f" count_row = {count_row}")


                            if count_row == 3:
                                # если набралось три подряд строки с long + 2 точками 'free'
                                # добавляем точку в список возможных точек начала корабля

                                #col_start = col_ + 1 if col_ else col_

                                col_start = col_
                                dots_for_start.append(dots_list[row_ -1][col_start])
                                logging.info (f"({row_ -1},{col_start}) добавлена в список точек старта")
                                count_row = 2
                            elif count_row == 4:
                                col_start = col_
                                dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                                logging.info (f"({row_ - 1},{col_start}) добавлена в список точек старта")
                                dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                                logging.info (f"({row_ },{col_start}) добавлена в список точек старта")
                            elif count_row == 3:
                                   col_start = col_
                                   dots_for_start.append(dots_list[row_ -1][col_start])
                                   logging.info (f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                                   count_row = 2



                        else: # в строке row_ среди {long}+2 точках есть занятая
                            logging.info (f"{__LINE__}: не все True")

                            count_row = 0
            if dots_for_start:  # если есть хоть одна подходящая точка для начала корабля
                break # выходим из цикла. Иначе пробуем другое направление корабля
            # Конец H части

            if self.direction == 'V'  : # Вертикальное расположение
                for i in range(0, size_map - self.long + 1):

                    count_row = 0
                    #for row_ in range (0, size_map ):
                    for j in range (0, size_map ):
                        col_, row_ = j ,i
                        logging.info (f"{__LINE__}: i = {i}, j = {j}")

                        list_ = [True if dots_list[row_ + j][col_].status_ == 'free' else False for j in range(self.long)]
                        list_w = [f"({dots_list[row_ + j][col_].x}, {dots_list[row_ + j][col_].y})-{ dots_list[row_ + j][col_].status_ }" for j in range(self.long)]
                        if row_ == 0 :
                            list_.append(True if dots_list[row_+ self.long ][col_].status_ == 'free' else False )
                            list_w.append(f"({dots_list[row_ + self.long][col_].x}, {dots_list[row_ + self.long][col_].y})-{dots_list[row_ + self.long][col_].status_}" )
                        elif row_ == size_map - self.long :

                            list_.insert(0,True if dots_list[row_-1][col_ ].status_ == 'free' else False)
                            list_w.insert(0, f"({dots_list[row_ -1][col_].x}, {dots_list[row_ -1][col_].y})-{dots_list[row_ -1][col_].status_}")
                        else:
                            list_.append(True if dots_list[row_+ self.long ][col_ ].status_ == 'free' else False )
                            list_.insert(0, True if dots_list[row_ - 1][col_ ].status_ == 'free' else False)
                            list_w.append(f"({dots_list[row_ + self.long][col_].x}, {dots_list[row_ + self.long][col_].y})-{dots_list[row_ + self.long][col_].status_}" )
                            list_w.insert(0, f"({dots_list[row_ - 1][col_].x}, {dots_list[row_ - 1][col_].y})-{dots_list[row_ - 1][col_].status_}")

                        logging.info (f"{__LINE__}: ({row_},{col_}) - {list_w}")

                        if all(list_):

                            if col_ == 0:
                                count_row += 2
                                logging.info (f"{__LINE__}: row_ = {row_}, col_ = 0, count_row = {count_row}")
                            elif (col_ == size_map  - 1 ) and count_row > 1:
                                count_row = 4
                                logging.info (f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")
                            else:

                                count_row  += 1
                                logging.info (f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")



                            if count_row == 3 :

                                # если набралось три подряд строки с long + 2 точками 'free'
                                # добавляем точку в список возможных точек начала корабля

                                #col_start = col_ + 1 if col_ else col_

                                row_start = row_
                                dots_for_start.append(dots_list[row_start][col_ - 1])
                                logging.info (f"{__LINE__}: ({row_start},{col_ - 1}) добавлена в список точек старта")
                                count_row = 2

                            elif count_row == 4 :

                                #col_start = col_
                                row_start = row_
                                dots_for_start.append(dots_list[row_start][col_ - 1]) # точка из предпоследней строки
                                logging.info (f"{__LINE__}: ({row_start},{col_-1}) добавлена в список точек старта")
                                dots_for_start.append(dots_list[row_start][col_]) # точка из последней строки
                                logging.info (f"{__LINE__}: ({row_start },{col_}) добавлена в список точек старта")
                        else: # в строке row_ среди {long}+2 точках есть занятая
                            logging.info (f"{__LINE__}: не все True , count_row  = 0")
                            count_row = 0
            if dots_for_start:  # если есть хоть одна подходящая точка для начала корабля
                break # выходим из цикла. Иначе пробуем другое направление корабля
            # Конец V части
        # Конец цикла [H,V]
        logging.info (f"{__LINE__}: количество точек {len(dots_for_start)}")
        if dots_for_start: # если есть хоть одна подходящая точка для начала корабля
            random_dot_start = random.choice(dots_for_start)

            self.row_ = random_dot_start.x
            self.col_ = random_dot_start.y
            logging.info (f"{__LINE__}: (x,y) = ({self.row_},{self.col_ }) - {self.direction}")
            return True, self.row_,  self.col_ , self.direction
        else:
            return False, False, False, False


class Player:

    def __init__(self, next_ = None):
        self.next_ = self.first_player()
        #next_player[0] = 'comp'
        #next_player[1] = 'user'


    def first_player(self): # Определяем, чей первый ход
        first_ = random.randrange(0, 1)
        return first_

    def make_move(self):
       if self.next_ :
          logging.info(f"Ход игрока")
          print(f"Ход игрока. Введите координаты")
          m = input(f" XY, X -по вертикали, Y - по горизонтали, Q - выход :")
       else:
           logging.info(f"Ход компьютера")
           print(f"Ход компьютера")

       self.next_= not self.next_


    def check_shot_coordinates(func):  # декоратор проверки правильности введенных координат
        # на предмет непересечения с уже сделанными ходами


        def wrapper(*args, **kwargs):
            while True:
                x, y = func(*args, **kwargs)
                print(f"{__LINE__}: ({x},{y})")
                try:
                    status_ = args[1][x][y].status_
                    print(f"{__LINE__}: args[1] = args[{x}][{y}].status_ = {status_}")


                    if status_ not in ['free', 'busy']:
                        print(f"{__LINE__}: в эту клетку ранее уже был сделан ход. Повторите ввод")
                    else:
                        print(f"{__LINE__}: ход ({x},{y}) принят")
                        break
                except IndexError:
                    print(f"{__LINE__}: введены координаты вне границ поля. Повторите ввод")


            return x, y


        return wrapper

    @check_shot_coordinates
    def take_shot(self,dots_list_): # ход игрока
        m  = input(f"Ход игрока. Введите координаты клетки, XY. X - по вертикали, Y -  по горизонтали :")
        m = re.match(r'(\d{1})\W*(\d{1})', m)
        x, y  = m.group(1), m.group(2)
        print(f"{__LINE__} Вы ввели ({x},{y})")
        return int(x), int(y)







































def main_game():

    Board_width = Board_length = 6 # Задаем размерность полей
    ships_list =[(1,4), (2,2), (3,1)] # ключ - длина корабля, значение - количество кораблей этой длины
    board_ = Board(size_map = 6, ships_list = ships_list)
    player_= Player()


    for _ in range(10):
        board_.paint_board()
        player_.make_move()
        input(f"{__LINE__}: контроль")


    next_gamer = {0:'comp', 1:'user'}

    next_gamer_index = Board.whos_first_strike() # возвращает индекс игрока, чей первый ход, 0: comp, 1: user

    x, y, = 0, 0  # начальные координаты игры, для инициализации чистого поля

    while True: # Игра началась
        Board_.update_Board(x, y)
        Board_.strike(next_gamer[next_gamer_index])
        next_gamer_index = not next_gamer_index



if __name__ == '__main__':
    main_game()
    #board= Board(6)
    '''
    gamer = Player()
    print(f"{__LINE__}:{Board_.dim_board}")
    dots_list = Board_.create_coordinate() # список из всех точек поля
    #dots_list_all[2][1].status_= 'busy'
    #print(f"{__LINE__}: {dots_list_all[2][1].x}, {dots_list_all[2][1].y}")

    dots_list = Board_.create_ships(dots_list)
    #x_start, y_start, type_direction = ship3.find_free_place(dots_list_all)
    #dots_list_all  = Board_.place_the_ship(ship3,dots_list_all )
    Board_.paint_board(dots_list )
    x, y = gamer.take_shot(dots_list)
    print(f"{__LINE__}: ({x},{y})")
    '''
    





    print(f"{__LINE__}: stop")





