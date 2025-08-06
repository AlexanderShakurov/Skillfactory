import inspect
import random
import re
import logging
import time

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

    

    def __init__(self, size_map, ships_list,ships_user = None, ships_comp = None, comp_map = None):
        self.size_map= size_map
        self.ships_list = ships_list

        self.comp_map = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )] # список точек доски comp
        #self.left_map = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )] # список точек доски left
        #logging.info(f"Создан comp_map")
        self.user_map = [[Dot(j, i) for i in range(0 + self.size_map, 2 * self.size_map )] for j in range(0, self.size_map)]
        # self.right_map = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )] # список точек доски right
        self.ships_user = self.create_ships_user()
        #self.ships_comp = self.create_ships()[1]

        # список точек доски gamer
        self.comp_map, self.ships_comp = self.create_ships() # карта поля игрока comp с введенными координатами кораблей
        logging.info(f"В comp_map внесены координаты кораблей")

    def check_win(self, next_): #Проверка наступления выигрыша
        pass

        ships_ = self.ships_user if next_ else self.ships_comp
        gamer_name = 'user' if next_ else 'comp'
        for i in self.ships_comp:
            kkk = self.ships_comp[i]
            logging.info(f" Проверяем все корабли comp {i},{kkk}, {kkk.life_}, {kkk.row_}, {kkk.col_}" )
        for i in self.ships_user :
            kkk = self.ships_comp[i]
            logging.info(f" Проверяем все корабли user {i},{kkk}, {kkk.life_}, {kkk.row_}, {kkk.col_}" )
        for k, v in ships_.items():
            logging.info(f" Проверяем корабли {gamer_name} {k}.life = {v.life_}")
            if v.life_ !=  0:
                return False, gamer_name
            logging.info(f" Все корабли {gamer_name} убиты")
        gamer_win = 'comp' if next_ else 'user'
        return True, gamer_win



    def check_dot(self, x, y, status_dot, m1):
        logging.info(f"Ищем соседнюю клетку типа {status_dot} для точки ({x},{y})")


        s =[]
        for l in range(len(m1)):
            row0 = x + m1[l][0]
            col0 = y + m1[l][1]

            #try:
            if (row0 in range(self.size_map)) and (col0 in range(self.size_map)):
                m2 = self.user_map[row0][col0].status_
                logging.info(f" user_map[{row0}][{col0}].status_ = {m2}")



                if m2 in status_dot :
                    logging.info(f" Найдена соседняя  клетка {status_dot} ({row0},{col0})")

                    s.append((row0,col0))

        return s

    def update_user_map(self,res, x, y): # Обновление dot, ship, board по результату хода comp
        row_ = x
        col_ = y - self.size_map
        m = res.group()
        logging.info(f"Обновление dot, ship, board по результату хода  ({x},{y}) - {m}")

        if m == '1': # Ход мимо
            self.user_map[row_][col_].status_ = 'T'

        elif m == '2': # Ранен
            logging.info(f"Обработка ответа Ранен от user ")
            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1)


            if m2:
                logging.info(f"Найдена соседняя раненая точка {m2} ")
                row_2, col_2 = m2[0][0], m2[0][1]

                ship_damaged = self.user_map[row_2][col_2].ship


                self.user_map[row_][col_].status_ = 'X'
                ship_damaged.long +=1
                self.user_map[row_][col_].ship = ship_damaged
                logging.info(f"Получаем ссылку на корабль из соседней раненой клетки {ship_damaged} ")
            else:

                logging.info(f"Cоседняя раненая точка не найдена,  {m2} ")
                logging.info(f" Присваиваем свободный корабль точке {row_}, {col_}")
                for k, v in self.ships_user.items():
                    logging.info(f" {v.long}")
                    if not v.long:
                        ship_damaged = v
                        ship_damaged.long = 1
                        self.user_map[row_][col_].status_ = 'X'
                        self.user_map[row_][col_].ship = ship_damaged
                        logging.info(f" точке ({row_}{col_}) присвоен корабль {ship_damaged}")
                        break

                # s = [self.ships_user[k] for k,v in self.ships_user.items() if not self.ships_user[k].long]
                # ship_killed = s[0]
                logging.info(f"Выбран неиспользуемый корабль {ship_damaged}")


        elif m == '3': # Убит

            self.user_map[row_][col_].status_ = 'killed'
            logging.info(f"Обработка ответа Убит от user ")
            '''
            logging.info(f"Проверяем корректность ответа ")
            logging.info(f"Ищем соседнюю убитую клетку ")
            
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, [ 'killed'], m1)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть  соседней клетки с убитым кораблем"
                logging.info(msg)

                return False, msg

            logging.info(f"Ищем соседнюю по диагонали раненую или убитую клетку ")
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, ['X','killed'], m1)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть диагональной соседней клетки с кораблем"
                logging.info(msg)

                return False, msg
            '''
            logging.info(f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1)

            #m2 = self.check_dot(row_, col_)
            if m2:
                if len(m2) == 2:

                    logging.info(f"Найдено 2 соседние раненые точки {m2} ")
                    row_2, col_2 = m2[0][0], m2[0][1]
                    row_3, col_3 = m2[1][0], m2[1][1]
                    self.user_map[row_2][col_2].status_ = 'killed'
                    self.user_map[row_3][col_3].status_ = 'killed'
                    ship_killed = self.user_map[row_2][col_2].ship
                    ship_repaired = self.user_map[row_3][col_3].ship # один из кораблей освобождается от привязки к точке
                    self.user_map[row_][col_].ship = ship_killed
                    self.user_map[row_2][col_2].ship = ship_killed
                    self.user_map[row_3][col_3].ship = ship_killed
                    ship_killed.life_ = 0
                    ship_killed.long = 3
                    ship_repaired.life = None

                elif len(m2) == 1:
                    logging.info(f"Найдена 1 смежная раненая точка {m2} ")
                    row_2, col_2 = m2[0][0], m2[0][1]
                    self.user_map[row_2][col_2].status_ = 'killed'

                    ship_killed = self.user_map[row_2][col_2].ship
                    logging.info(f" ship_killed = {ship_killed}")
                    if ship_killed.long == 2:
                        ship_killed.long = 3
                        ship_killed.life = 0
                        delta_row = row_ - row_2
                        delta_col = col_ - col_2
                        row_3 = -2 * (delta_row) + row_
                        col_3 = -2 * (delta_col) + col_
                        logging.info(f" Длина убитого корабля 3, третья точка ({row_3},{col_3}")
                        self.user_map[row_3][col_3].status_ = 'killed'
                    if ship_killed.long == 1:
                        ship_killed.long = 2
                        ship_killed.life = 0
                        logging.info(f" Длина убитого корабля 2")
                else:
                    logging.info(f"Cоседняя раненая клетка не найдена,  {m2} ")
                    logging.info(f" Присваиваем  свободный корабль точке {row_}, {col_}")
                    for k,v in self.ships_user.items():
                        logging.info(f" {v.long}")
                        if not v.long:
                            ship_killed = v
                            ship_killed.long = 1
                            ship_killed.life = 0
                            self.user_map[row_][col_].ship = ship_killed
                            break

                #s = [self.ships_user[k] for k,v in self.ships_user.items() if not self.ships_user[k].long]
                #ship_killed = s[0]
                logging.info(f"Выбран неиспользуемый корабль {ship_killed}")



        #input(f"{__LINE__}: контроль обработки ответа user")
        return True, ''

    def create_ships_user(self):  # создаем объекты кораблей user
        ships_list1 = sorted(self.ships_list, reverse=True)
        ships_user = {}
        for i in ships_list1:
            for j in range(i[1]):
                #ships_user[f"{i[0]}-{j}"] = Ship(i[0])
                ships_user[f"{i[0]}-{j}"] = Ship(None)
        return ships_user

    def create_ships(self): # создаем объекты кораблей comp и размещаем их на карте
        #comp_map = [[Dot(j, i) for i in range(0, self.size_map)] for j in
        #                 range(0, self.size_map)]  # список точек доски comp
        ships_comp = {} # Словарь из всех созданных объектов кораблей компьютера
        ships_list1 = sorted(self.ships_list, reverse=True)
        count_try = 1 # номер попытки размещения кораблей. Для отладки
        while True:
            #Очищаем все точки доски comp
            for i in range(0, self.size_map):
                for j in range(0, self.size_map):
                    self.comp_map[i][j].status_ = 'free'
            res = []
            for i in ships_list1:
                for j in range(i[1]):

                    ships_comp[f"{i[0]}-{j}"] = Ship(i[0], life_ = i[0])
                    res1, res2, res3, res4 = ships_comp[f"{i[0]}-{j}"].find_free_place(self.comp_map, self.size_map)
                    logging.info(f"ship[{i[0]}-{j}]: {res1},{res2},{res3},{res4}")
                    if res1:
                        #logging.info(f"Найдены координаты для  ship[{i[0]}-{j}] ")
                        self.comp_map = self.place_the_ship(ships_comp[f"{i[0]}-{j}"], self.comp_map)
                    res.append(res1)


            if all(res):
                logging.info(f"Все корабли размещены на comp_map")
                for k, v, in ships_comp.items():
                    logging.info(f" {k}: {v}, life {v.life_}, long {v.long}, row_ {v.row_}, col_ {v.col_}" )

                return self.comp_map, ships_comp
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
        char_ = {'free':"◯", 'busy':"B", 'X':'X', 'T':'T', 'killed':'■' }
        board0 = '   1 2 3 4 5 6   --     1 2 3 4 5 6 '
        print(board0)
        board0 = '  -------------  --    -------------'
        print(board0)
        count_row = 1

        for i in range(self.size_map):
            board1, board2 = f"{count_row} |", f"{count_row} |"
            for j in range(self.size_map):
                board1 += char_[self.comp_map[i][j].status_] + '|'
                #logging.info(f"self.user = {self.user_map[i][j].status_}")
                board2 += char_[self.user_map[i][j].status_] + '|'
            count_row += 1
            print(f"{board1}  --  {board2}")
        return True





class Ship:

    def __init__(self, long, direction = None, row_ = None, col_= None, life_ = None):
        self.long = long # длина корабля
        self.direction = direction # направление корабля, H - горизонт, V - вертик.
        self.row_ = row_ # начальная координата (строка)
        self.col_ = col_ # начальная координата (столбец)
        self.life_ = life_
        logging.info(f" Создаем ship {self.long}, {self.direction}, {self.row_}, {self.col_}")

    def check_life(self): # Проверка результата попадания
        self.life_ -= 1
        return self.life_
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



                        #logging.info (f"{row_},{col_}) - {list_}")

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
                                #logging.info (f"({row_ -1},{col_start}) добавлена в список точек старта")
                                count_row = 2
                            elif count_row == 4:
                                col_start = col_
                                dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                                #logging.info (f"({row_ - 1},{col_start}) добавлена в список точек старта")
                                dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                                #logging.info (f"({row_ },{col_start}) добавлена в список точек старта")
                            elif count_row == 3:
                                   col_start = col_
                                   dots_for_start.append(dots_list[row_ -1][col_start])
                                   #logging.info (f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                                   count_row = 2



                        else: # в строке row_ среди {long}+2 точках есть занятая
                            #logging.info (f"{__LINE__}: не все True")

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
                        #logging.info (f"{__LINE__}: i = {i}, j = {j}")

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

                        #logging.info (f"{__LINE__}: ({row_},{col_}) - {list_w}")

                        if all(list_):

                            if col_ == 0:
                                count_row += 2
                                #logging.info (f"{__LINE__}: row_ = {row_}, col_ = 0, count_row = {count_row}")
                            elif (col_ == size_map  - 1 ) and count_row > 1:
                                count_row = 4
                                #logging.info (f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")
                            else:

                                count_row  += 1
                                #logging.info (f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")



                            if count_row == 3 :

                                # если набралось три подряд строки с long + 2 точками 'free'
                                # добавляем точку в список возможных точек начала корабля

                                #col_start = col_ + 1 if col_ else col_

                                row_start = row_
                                dots_for_start.append(dots_list[row_start][col_ - 1])
                                #logging.info (f"{__LINE__}: ({row_start},{col_ - 1}) добавлена в список точек старта")
                                count_row = 2

                            elif count_row == 4 :

                                #col_start = col_
                                row_start = row_
                                dots_for_start.append(dots_list[row_start][col_ - 1]) # точка из предпоследней строки
                                #logging.info (f"{__LINE__}: ({row_start},{col_-1}) добавлена в список точек старта")
                                dots_for_start.append(dots_list[row_start][col_]) # точка из последней строки
                                #logging.info (f"{__LINE__}: ({row_start },{col_}) добавлена в список точек старта")
                        else: # в строке row_ среди {long}+2 точках есть занятая
                            #logging.info (f"{__LINE__}: не все True , count_row  = 0")
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

    def find_free_place_new(self, dots_list, size_map):
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

            #if self.direction == 'H'  :
            for i in range(0, size_map):

                count_row = 0
                #for row_ in range (0, size_map ):
                for j in range (size_map ):
                    if self.direction == 'H':
                        col_, row_ = i, j
                    else:
                        col_, row_ = j, i

                    list_ = [True if dots_list[row_][col_ + j].status_ == 'free' else False for j in range(self.long)]

                    if col_ == 0 :
                        list_.append(True if dots_list[row_][col_].status_ == 'free' else False )

                    elif col_ == size_map - 1 :
                        list_.insert(0,True if dots_list[row_][col_ - 1].status_ == 'free' else False)
                    else:
                        list_.append(True if dots_list[row_][col_].status_ == 'free' else False )
                        list_.insert(0, True if dots_list[row_][col_ - 1].status_ == 'free' else False)

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
                            #logging.info (f"({row_ -1},{col_start}) добавлена в список точек старта")
                            count_row = 2
                        elif count_row == 4:
                            col_start = col_
                            dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                            #logging.info (f"({row_ - 1},{col_start}) добавлена в список точек старта")
                            dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                            #logging.info (f"({row_ },{col_start}) добавлена в список точек старта")
                        elif count_row == 3:
                               col_start = col_
                               dots_for_start.append(dots_list[row_ -1][col_start])
                               #logging.info (f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                               count_row = 2



                    else: # в строке row_ среди {long}+2 точках есть занятая
                        #logging.info (f"{__LINE__}: не все True")

                        count_row = 0
            if dots_for_start:  # если найдена есть хоть одна подходящая точка для начала корабля
                break # выходим из цикла. Иначе пробуем другое направление корабля


        logging.info (f"{__LINE__}: количество точек {len(dots_for_start)}")
        if dots_for_start: # если есть хоть одна подходящая точка для начала корабля
            random_dot_start = random.choice(dots_for_start)

            self.row_ = random_dot_start.x
            self.col_ = random_dot_start.y
            logging.info (f"{__LINE__}: (x,y) = ({self.row_},{self.col_ }) - {self.direction}")
            return True, self.row_,  self.col_ , self.direction
        else:
            return False, False, False, False




    def find_free_place_new2(self, dots_list, size_map, board_):
        # dots_list - текущее состояние точек поля
        """ случайно выбирается тип размещения, H - горизонтальный или V - вертикальный
            и координаты начала корабля"""
        self.direction  = random.choice(['H', 'V'])

        s = ['H', 'V'] if self.direction == 'H'  else ['V', 'H']

        dots_for_start = [] # список точек, подходящих для начала корабля
        for self.direction in s: #
            #logging.info(f" длина корабля {self.long}, направление {self.direction} ")

            for i in range(size_map - self.long):
                for j in range(size_map) :
                    row_ = j if self.direction == 'H' else i
                    col_ = i if self.direction == 'H' else j

                    #logging.info(f"Проверяем ({row_}, {col_}) - начало корабля {self.long} - {self.direction} ")
                    res = board_.check_line_dots(row_, col_, self.direction, self.long, dots_list)
                    if res:
                        #logging.info(f"({row_}, {col_}) - подходит для {self.long} - {self.direction}")
                        dots_for_start.append((row_,col_))

            if dots_for_start:  # если найдена есть хоть одна подходящая точка для начала корабля
                break # выходим из цикла. Иначе пробуем другое направление корабля


        #logging.info (f" количество возможных точек для корабля {len(dots_for_start)}")
        if dots_for_start: # если есть хоть одна подходящая точка для начала корабля
            random_dot_start = random.choice(dots_for_start)

            self.row_ = random_dot_start[0]
            self.col_ = random_dot_start[1]
            #logging.info (f" Контроль001 Выбрана точка (x,y) = ({self.row_},{self.col_ }) - {self.long} - {self.direction}")
            return True, self.row_,  self.col_ , self.direction
        else:
            return False, False, False, False

    def find_free_place_new3(self, dots_list, size_map, board_):
        # dots_list - текущее состояние точек поля
        """ случайно выбирается тип размещения, H - горизонтальный или V - вертикальный
            и координаты начала корабля"""
        self.direction = random.choice(['H', 'V'])

        s = ['H', 'V'] if self.direction == 'H' else ['V', 'H']

        dots_for_start = []  # список точек, подходящих для начала корабля
        for self.direction in s:  #
            # logging.info(f" длина корабля {self.long}, направление {self.direction} ")

            for i in range(size_map - self.long):
                for j in range(size_map):
                    row_ = j if self.direction == 'H' else i
                    col_ = i if self.direction == 'H' else j

                    # logging.info(f"Проверяем ({row_}, {col_}) - начало корабля {self.long} - {self.direction} ")
                    res = board_.check_line_dots(row_, col_, self.direction, self.long, dots_list)
                    if res:
                        # logging.info(f"({row_}, {col_}) - подходит для {self.long} - {self.direction}")
                        dots_for_start.append((row_, col_))

            if dots_for_start:  # если найдена есть хоть одна подходящая точка для начала корабля
                break  # выходим из цикла. Иначе пробуем другое направление корабля

        # logging.info (f" количество возможных точек для корабля {len(dots_for_start)}")
        if dots_for_start:  # если есть хоть одна подходящая точка для начала корабля
            random_dot_start = random.choice(dots_for_start)

            self.row_ = random_dot_start[0]
            self.col_ = random_dot_start[1]
            # logging.info (f" Контроль001 Выбрана точка (x,y) = ({self.row_},{self.col_ }) - {self.long} - {self.direction}")
            return True, self.row_, self.col_, self.direction
        else:
            return False, False, False, False


class Player:

    def __init__(self, next_ = None):
        self.next_ = self.first_player()
        #next_player[0] = 'comp'
        #next_player[1] = 'user'


    def first_player(self): # Определяем, чей первый ход
        first_ = random.randrange(0, 10) & 2
        logging.info(f"first_= {first_}")
        return first_

    def make_move(self, board):
       logging.info(f"self.next_ = {self.next_}")
       if self.next_ :

          self.make_user_move(board)
       else:
           logging.info(f"Ход компьютера")
           print(f"Ход компьютера")
           self.make_comp_move(board)

       self.next_= not self.next_

    def make_comp_move(self, board): # Ход компьютера

        s = []

        for i in range(board.size_map):
            for j in range(board.size_map):
                if board.user_map[i][j].status_ == 'free':
                    logging.info(f" Проверяем точку ({i},{j})  на соседство с ранеными или убитыми кораблями")

                    m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (1, -1), (1, 1)]
                    m2 = board.check_dot(i,j,['X','killed'], m1)

                    if not m2:   #flag:
                        s.append((board.user_map[i][j].x, board.user_map[i][j].y))
                        logging.info(f" В список точек хода компа добавлена ({board.user_map[i][j].x},{board.user_map[i][j].y})")

        logging.info(f" список свободных ячеек для хода comp {s}")
        random_dot_move = random.choice(s)
        dot_move_row_ = random_dot_move[0] + 1
        dot_move_col_ = random_dot_move[1] - board.size_map + 1
        logging.info(f" Ход компьютера ({dot_move_row_ },{dot_move_col_})")
        print(f"{__LINE__}: Ход компьютера ({dot_move_row_ },{dot_move_col_})")
        self.check_comp_move(random_dot_move[0],random_dot_move[1], board)
        #board.check_comp_move(random_dot_move[0],random_dot_move[1])

        #result = board.check_move(x, y, board.comp_map)

        #input(f"{__LINE__}: контроль хода комп, проверь log")


    def make_user_move(self,board): # Ход игрока
        logging.info(f"Ход игрока")
        while True:
            print(f"Ход игрока. Введите координаты XY")
            m = input(f"X -по вертикали, Y - по горизонтали, Q - выход :")
            m1 = re.match(r'([Qq]$)|(\d{1})\W*(\d{1})', m)
            if m1:
                logging.info(f" {m1.group(1), m1.group(2), m1.group(3)}")
                if m1.group(1):
                    pass
                    #finish_game(): # Завершение игры по инициатеве user
                    logging.info(f" Завершение игры по инициатеве user")
                    break
                else:

                    x = int(m1.group(2)) - 1
                    y = int(m1.group(3)) - 1

                    try:
                        status_dot = board.comp_map[x][y].status_
                        logging.info(f" проверяем board_.comp_map[{x},{y}].status_ = {status_dot}")
                        #result = board.check_move(x, y, board.comp_map)
                        result = self.check_user_move(x, y, board.comp_map)
                        if result:
                            print(f"{__LINE__}: Результат хода {result}")
                            break
                        else:
                            print(f"{__LINE__}:Такой ход уже был, повторите ввод")

                    except:
                        logging.error(f" Координаты вне диапазона поля, повторите ввод {x},{y}")
                        print(f"Координаты вне диапазона поля, повторите ввод")
                    input(f"(__LINE__): контроль")
            else:
                logging.error(f" неверные координаты {m}")
                print(f"Недопустимые символы, повторите ввод")

    def check_comp_move(self, x, y, board, player_type = 'user', res = None): #Получение от user результата хода comp
        m1 = {'1': 'Мимо', '2': 'Ранен', '3': 'Убит'}
        m2 = {'1': 'T', '2': 'X', '3': 'Убит'}
        while True:

            if player_type == 'user':
                res = self.user_answer() # получение ручного ответа от user

            if res:
                logging.info(f"ответ user: {m1[res.group()]}")
                print(f"{__LINE__}: Результат хода - {m1[res.group()]}")
                res11, msg11 = self.check_error_on_user_answer(board, res, x, y)
                logging.info(f" Результат проверки user's answer {res11},{msg11}")
                if res11:
                    res1, msg1 = board.update_user_map (res, x, y)  #Обновление карты по итогам хода.
                    break
                else:
                    print(f"{__LINE__}: {msg11}")
                    logging.info(f" Ответ user {msg11}")
            else:
                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")

    def check_user_move(self, x, y, dot_ ): # Проверка введенных координат user
        logging.info(f" start ({x},{y}) - {dot_[x][y].status_}")
        if dot_[x][y].status_ == 'free':
            result = 'Мимо'

            dot_[x][y].status_ = 'T'
            logging.info(f" dot_[{x}][{y}].status_ = 'T'")
        elif dot_[x][y].status_ == 'busy':
            logging.info(f" dot_[x][y].status_ == 'busy'")
            try:
                ship_= dot_[x][y].ship
                ship_.life_ -= 1
                ship_life = ship_.life_
                logging.info(f" проверка объект ship {ship_}, life {ship_.life_}, {ship_.long}, dot_[{x}][{y}] {dot_[x][y].ship}")
            except Exception as er:
                logging.error(f"Ошибка ship_= dot_[x][y].ship или ship_life = ship_.life: {er}")
            logging.info(f" ship_ = {ship_}, ship_life = {ship_life}")
            if ship_life > 0 :
                result = 'Ранен'
                dot_[x][y].status_ = 'X'
                logging.info(f" dot_[{x}][{y}].status_ = 'X'")
            else:
                result = 'Убит'
                row0  = ship_.row_
                col0 = ship_.col_
                direct_ = ship_.direction
                for i in range(ship_.long):
                    x = row0 + (0 if direct_ == 'H' else i)
                    y = col0 + (0 if direct_ == 'V' else i)
                    dot_[x][y].status_ = 'killed'
                logging.info(f" dot_[{x}][{y}].status_ = 'Убит'")
        else:
            logging.info(f"Такой ход уже был")

            result = False
        logging.info(f"Результат хода - {result}")

        return result

    # Редакция ********************************************************88
    def check_error_on_user_answer(self, board, res, x, y): # Проверяем ответ user на корректность
          row_ = x
          col_ = y - board.size_map
          m = res.group()
          logging.info(f"Проверяем ответ user {m} на ход comp ({x},{y})")

          if m == '1': # Ход мимо
              #board.user_map[row_][col_].status_ = 'T'
              return True, ''

          elif m == '2': # Ранен
              logging.info(f"Обработка ответа Ранен от user ")

              logging.info(f"Поиск среди соседних клеток раненых и убитых ")
              m1 = [(-1, -1),(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
              m2 = board.check_dot(row_, col_, ['X', 'killed'], m1)
              if len(m2) > 1 :
                  msg = "Некорректный ответ. У раненой клетки не может быть более 1 соседней клетки с кораблем"
                  logging.info(msg)

                  return False, msg

              logging.info(f"Поиск среди соседних диагональных клеток раненых или убитых ")
              m1 = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
              m2 = board.check_dot(row_, col_, ['X', 'killed'], m1)
              if m2:
                  msg = "Некорректный ответ. У раненой клетки не может быть диагональной соседней клетки с кораблем"
                  logging.info(msg)

                  return False, msg


              logging.info(
                  f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
              m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
              m2 = board.check_dot(row_, col_, ['X'], m1)


              if m2:
                  logging.info(f"Найдена соседняя раненая точка {m2} ")
                  row_2, col_2 = m2[0][0], m2[0][1]

                  ship_damaged = board.user_map[row_2][col_2].ship
                  if ship_damaged.long == 2:
                      msg = f"Некорректный ответ. Три подряд раненые клетки - это должен быть убитый корабль."
                      logging.error(msg)
                      return False, msg
                  ''' Не доделано                                                                                                         
                  elif ship_damaged == 1:                                                                                                 
                      logging.info(f" Проверяем, есть ли свободные для хода клетки с концов корабля")                                     
                      delta_row = row_ - row_2                                                                                            
                      delta_col = col_ - col_2                                                                                            
                      if delta_row:                                                                                                       
                          if min(row_, row_2) > 0:                                                                                        
                              row_min  = min(row_, row_2)                                                                                 
                              col_min = col_                                                                                              
                          elif max(row_, row_2) < board.size_map - 1:                                                                     
                              row_max = max(row_, row_2)                                                                                  
                              col_max = col_                                                                                              
                      '''


          elif m == '3': # Убит

              board.user_map[row_][col_].status_ = 'killed'
              logging.info(f"Обработка ответа Убит от user ")
              logging.info(f"Проверяем корректность ответа ")
              logging.info(f"Ищем соседнюю убитую клетку ")
              m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
              m2 = board.check_dot(row_, col_, [ 'killed'], m1)
              if m2:
                  msg = "Некорректный ответ. У убитой  клетки не может быть  соседней клетки с убитым кораблем"
                  logging.info(msg)

                  return False, msg

              logging.info(f"Ищем соседнюю по диагонали раненую или убитую клетку ")
              m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
              m2 = board.check_dot(row_, col_, ['X','killed'], m1)
              if m2:
                  msg = "Некорректный ответ. У убитой  клетки не может быть диагональной соседней клетки с кораблем"
                  logging.info(msg)

                  return False, msg


          return True, ''


    def user_answer(self): # Получе        #input(f"{__LINE__}: контроль обработки ответа user")                                                                                       ние ответа от игрока user на ход comp
        logging.info(f" ждем ответа        return True, ''                                                                                                                              от user")
        while True:
            m = input(f"Введите результат хода. 1 - мимо, 2 -ранен, 3 - убит :")

            res = re.match(r'([1-3]{1})', m)

            if not res:

                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")
            else:

                logging.info(f" принят корректный ответ user {res.group()}")
                return res

class Board_new:




    def __init__(self, size_map, ships_list,  side_dysplay = None, type_game= '00',
                 gamers_name = None, board_map =None, ships = None, player_ = None):
        self.side_dysplay = side_dysplay # сторона экрана - left, right
        self.player_ = player_
        self.type_game = type_game # тип игрока - user - человек, comp - компьютер
        self.size_map = size_map # Размерность игрового поля
        self.ships_list = ships_list # Список кораблей, длина:количество


        #self.board_map['left'] =  [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )]
        #self.board_map['right'] = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )]
        self.board_map = self.board_map_init()

        self.type_game = self.invite_to_start()
        logging.info(f"{self.type_game}")

        self.gamers = {'left':self.type_game[0], 'right':self.type_game[1]}
        self.board_map = self.board_map_init()
        self.ships = self.create_ships()
        self.gamers_name = {'0':"Компьютер", '1':"Игрок"}




    def board_map_init(self):
        s = {}

        s['left'] = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )]
        s['right'] = [[Dot(j, i) for i in range(0, self.size_map)] for j in range(0, self.size_map)]
        return s

    def paint_board(self, msg_list):    # рисует доску по списку с точками
        logging.info(f"{self.type_game}")
        char_ = {}
        char_['00'] = {'free':"◯", 'busy':"△", 'X':'X', 'T':'T', 'killed':'■' }
        char_['01'] =  {'free':"◯", 'busy':"◯", 'X':'X', 'T':'T', 'killed':'■' }
        char_['10'] =  {'free':"◯", 'busy':"◯", 'X':'X', 'T':'T', 'killed':'■' }

        #board0 = '   1 2 3 4 5 6   --     1 2 3 4 5 6 '
        t = f"{' '* 3}"
        for i in range (1, self.size_map + 1):

            t += f"{i} "
        title = f"{t}{' '* 6}{t}"
        title2 = f"""{' '*8}{"Игра 'Морской' бой":^50}"""
        print(f"{title}{title2}")
        #board0 = '  -------------  --    -------------'
        board0 = f"{' '*2}{'-'*13}{' '*8}{'-'*13}"
        board01 = f"{' '*8}{'-'*50}"
        print(board0 + board01)
        count_row = 1

        for i in range(self.size_map):
            board_left, board_right = f"{count_row} |", f"{count_row} |"
            board_left_ship, board_right_ship = f"{count_row} |", f"{count_row} |"
            for j in range(self.size_map):
                board_left += char_[self.type_game][self.board_map['left'][i][j].status_] + '|'

                #logging.info(f"self.user = {self.user_map[i][j].status_}")
                board_right += char_[self.type_game][self.board_map['right'][i][j].status_] + '|'



            count_row += 1
            logging.info(f"{count_row} - {len(msg_list)}")
            if count_row - 1 <= len(msg_list):
                msg = f"{msg_list[count_row - 2]}"
                logging.info(f"{msg_list[count_row - 2]}")
            else:
                msg =f"{' '*48}"

            msg = f"{msg}" if msg else f"{' '*48}"
            m = f"{board_left}  --  {board_right}{' '*8}{'|'}{msg[:48]}{'|'}"
            logging.info (f" {m}")
            print(m)
            #print(f"{board_left}  --  {board_right}{' '*8}{'|'}{msg}{'|'}")

            #logging.info(f"Контроль123 {board_left_ship} {board_right_ship} ")
        print(board0 + board01)

        #print(f"  {self.gamers_name[self.gamers['left']]:13}{' '*8}{self.gamers_name[self.gamers['right']]:13}")
        return True

    def input_(self, text_):
        #m_ = "Введите свой выбор XY__:"
        l_text = len(text_)

        m = input(f"{' ' * 2}{' ' * 13}{' ' * 8}{' ' * 13}{' ' * 8}{text_:<{len(text_)}}")
        return m

    def invite_to_start(self):
        #paint_board(self, msg_list)
        msg = [' '*24 for _ in range(self.size_map)]
        msg_ = [' '*24 for _ in range(self.size_map)]
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
            long_ = self.ships_list[i][0]         #'⚫'* 
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

        
        #self.paint_board(msg)


        #d = {'00': 'Демо', '10':'Левое поле - игрок, правое поле -компьютер', '01': "Левое поле - компьютер, правое поле - игрок"}
        logging.info("Приглашение к началу игры")
        while True:
            self.paint_board(msg)
            m = self.input_('Введите режим игры: ')
            #print(f"{__LINE__}:Выберите поле и режим игры: 10 - поле игрока слева, 01 - справа, 00 - Демо игра между двумя компьютерами")
            #m_ =     "Введите свой выбор XY__:"
            #lm_ = len(m_)
            #m = input (f"{' '*2}{' '*13}{' '*8}{' '*13}{' '*8}{m_:<{len(m_)}}")

            #m = input(f"{__LINE__}: Введите свой выбор __:")
            res = re.match(r'(\d{1})\W*('r'\d{1}$)', m)

            if res:

                #print(f"{__LINE__} Игра: {d[res.group(1)+res.group(2)]}")
                logging.info(f"Выбрана игра {res.group(1)}-{res.group(2)}")

                return f"{res.group(1)}{res.group(2)}"
            else:
                #print(f"{__LINE__}: Введены некорректные символы, повторите ввод.")
                msg[5] = f"Введены некорректные символы, повторите ввод."

    def create_ships(self):
        logging.info(f" gamers: {self.gamers}")
        ships = {}
        for k, v  in self.gamers.items():
            logging.info(f"создаем корабли для пользователя {k}-{v}")

            if v == '1' : #  - тип user
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
                    res1, res2, res3, res4 = ships_comp[f"{i[0]}-{j}"].find_free_place_new2(self.board_map[v], self.size_map,self)
                    logging.info(f"ship[{v}][{i[0]}-{j}]: {res1},{res2},{res3},{res4}")
                    if res1:
                        #logging.info(f"Найдены координаты для [{i[0]}-{j}] ")
                        self.board_map[v] = self.place_the_ship(ships_comp[f"{i[0]}-{j}"], self.board_map[v])
                    res.append(res1)

            if all(res):
                logging.info(f"Все корабли размещены на comp_map")
                for k, v, in ships_comp.items():
                    logging.info(f" {k}: {v}, life {v.life_}, long {v.long}, row_ {v.row_}, col_ {v.col_}")

                return ships_comp
            else:
                logging.error(f"Не удалось разместить корабли, повторяем попытку")
                #print(f"{__LINE__}: не удалось разместить, попытка {count_try}, повторяем попытку")
                count_try += 1




    def place_the_ship(self, ship, dots_list): # записываем координаты точек корабля в объекты точек
        #s =[]
        row_ = ship.row_
        col_ = ship.col_

        for i in range(ship.long):
            row1_ = row_ + i if ship.direction == 'V'  else row_
            col1_ = col_ + i if ship.direction == 'H'  else col_

            dots_list[row1_][col1_].status_ = 'busy'
            dots_list[row1_][col1_].ship = ship
            #logging.info(f" ship(row1_, col1_) ({row1_}, {col1_})")
            #s.append( dots_list[row1_][col1_])
        return dots_list


    def check_dot(self, x, y, status_dot, m1, dots_list):
        #logging.info(f"Ищем соседнюю клетку типа {status_dot} для точки ({x},{y})")
        #logging.info(f" m1 = {m1}")


        s =[]
        for l in range(len(m1)):
            row0 = x + m1[l][0]
            col0 = y + m1[l][1]

            #try:
            if (row0 in range(self.size_map)) and (col0 in range(self.size_map)):
                m2 = dots_list[row0][col0].status_
                #logging.info(f" dots_list[{row0}][{col0}].status_ = {m2}")



                if m2 in status_dot :
                    #logging.info(f" Найдена соседняя  клетка {status_dot} ({row0},{col0})")

                    s.append((row0,col0))

        return s


    def check_line_dots(self, row_, col_, direct, long, dots_list):
        #logging.info(f"проверяем ({row_},{col_}) для {long} - {direct} - {dots_list}")
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
                            
                #logging.info(f"m1 = {m1}")
                res1 = self.check_dot(row_i, col_i, ['busy'], m1, dots_list)
                if res1:  # если в окружении найдена хоть одна занятая точка
                    return False
            else:  # рассматриваемая точка занята
                return False
        #logging.info(f"контроль({row_},{col_}) подходит для {long} - {direct} - {dots_list}")
        return True

    def update_user_map(self, res, x, y, gamer_name):  # Обновление dot, ship, board по результату хода comp
        # 04.08.25
        row_ = x
        col_ = y
        #m = res.group()
        dots_list = self.board_map[gamer_name]
        logging.info(f"Обновление карты user после хода {gamer_name}  ({x},{y}) - {res}")

        #if m == '1':  # Ход мимо
        if res == 'Мимо':  # Ход мимо
            dots_list[row_][col_].status_ = 'T'

        elif res == 'Ранен':
        #elif m == '2':  # Ранен
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

                # s = [self.ships_user[k] for k,v in self.ships_user.items() if not self.ships_user[k].long]
                # ship_killed = s[0]
                logging.info(f"Выбран неиспользуемый корабль {ship_damaged}")

        elif res == 'Убит':
        #elif m == '3':  # Убит

            dots_list[row_][col_].status_ = 'killed'
            logging.info(f"Обработка ответа Убит от user ")
            '''
            logging.info(f"Проверяем корректность ответа ")
            logging.info(f"Ищем соседнюю убитую клетку ")

            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, [ 'killed'], m1)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть  соседней клетки с убитым кораблем"
                logging.info(msg)

                return False, msg

            logging.info(f"Ищем соседнюю по диагонали раненую или убитую клетку ")
            m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, ['X','killed'], m1)
            if m2:
                msg = "Некорректный ответ. У убитой  клетки не может быть диагональной соседней клетки с кораблем"
                logging.info(msg)

                return False, msg
            '''
            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1, dots_list)

            # m2 = self.check_dot(row_, col_)
            if m2:
                if len(m2) == 2:

                    logging.info(f"Найдено 2 соседние раненые точки {m2} ")
                    row_2, col_2 = m2[0][0], m2[0][1]
                    row_3, col_3 = m2[1][0], m2[1][1]
                    dots_list[row_2][col_2].status_ = 'killed'
                    dots_list[row_3][col_3].status_ = 'killed'
                    ship_killed = dots_list[row_2][col_2].ship
                    ship_repaired = dots_list[row_3][
                        col_3].ship  # один из кораблей освобождается от привязки к точке
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

                # s = [self.ships_user[k] for k,v in self.ships_user.items() if not self.ships_user[k].long]
                # ship_killed = s[0]
                logging.info(f"Выбран неиспользуемый корабль {ship_killed}")

        # input(f"{__LINE__}: контроль обработки ответа user")
        return True, ''

    def check_win(self, next_player_): #Проверяем жизни  кораблей игрока, чей следующий ход
        # current_player_ in ['left', 'right']
         for k, v in self.ships[next_player_].items():
             logging.info(f" {k}.life = {v.life_}")
             if (v.life_ is None) or (v.life_ > 0):
                 logging.info(f" {k}.life = {v.life_}")
                 return False
         return True


class Player_new:


    def __init__(self,users_ = None, next_= None, msg_list = None, count_move = 0, board_ = None):
        game_list = {'01': {'left': ['0', 'Компьютер'], 'right': ['1', 'Игрок']},
                     '00': {'left': ['0', 'Игрок-1'], 'right': ['0', 'Игрок-2']},
                     '10': {'left': ['1', 'Игрок'], 'right': ['0', 'Компьютер']}}

        self.count_move = count_move
        self.board_ = board_

        self.current_game = game_list[board_.type_game]
        self.next_, self.users_ = self.first_player()


    def intro(self, board_): # Сообщения для вывода на экран
        msg = []
        msg.append(f" Ход {board_.gamers_nameboard_.gamers[self.users[self.next_]]}а")
        return msg

    def first_player(self): # Определяем, чей первый ход
        logging.info(f"{self.board_}")


        a = random.choice([1, 0])
        b =  not a
        s = {1: 'left', 0:'right'}


        logging.info(f" Первый ход игрока {self.current_game[s[a]][1]}")
        self.board_.msg_list = ['' for i in range(self.board_.size_map)]
        msg_1 = f"Левое поле: {self.current_game['left'][1]}"
        msg_1 = f"{msg_1:<24}"
        msg_2 = f"Правое поле: {self.current_game['right'][1]}"
        msg_2 = f"{msg_2:>24}"
        self.board_.msg_list[0] = f"""{msg_1}{msg_2}"""
        msg_3 =  f"""Первый ход {self.current_game[s[a]][1]}"""
        msg_3 = f"{msg_3:<48}"
        self.board_.msg_list[2] = f"""{msg_3}"""

        self.board_.paint_board(self.board_.msg_list)
        time.sleep(4)
        print()
        return a, s

    def input_(self, text_):
        # m_ = "Введите свой выбор XY__:"
        l_text = len(text_)
        l = self.current_game['left'][1]
        r = self.current_game['right'][1]
        m = input(f"{' ' * 2}{l:<13}{' ' * 8}{r:<13}{' ' * 8}{text_:<{len(text_)}}")
        return m
    


    def make_move(self, board_):
       #print(f"{__LINE__}: Ход игрока {self.users_[self.next_]} ")
       #type_player = board_.gamers[self.users_[self.next_]]    # тип игрока , который ходит (0 - компьютер, 1 - user)
       #type_next_player = board_.gamers[self.users_[not self.next_]] # тип игрока, который проверяет ход
       #logging.info(f"Ход игрока {self.users_[self.next_]}, тип игрока {type_player}")
       #logging.info(f" board_ = {board_}")
       type_player = self.current_game[self.users_[self.next_]][0]
       type_next_player = self.current_game[self.users_[not self.next_]][0]
       self.count_move += 1





       #1 Получение координат хода
       while True:
           if type_player == '1': #    Ручной ввод игроком
               msg = ['' for i in range(self.board_.size_map)]
               msg[0] = f"Ходит {self.current_game[self.users_[self.next_]][1]}"

               msg[1] = f"Введите координаты XY"

               msg[2] = f"X - по вертикали"
               msg[3] = f"Y - по горизонтали"
               msg[4] = f"Q - выход"

               msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
               self.board_.paint_board(msg)

               quit_game,x,y = self.get_user_coord(board_)
               logging.info(f" Ход игрока {self.users_[self.next_]}, тип {board_.gamers[self.users_[self.next_]]}")

               if quit_game:

                   msg = f"Игра прервана игроком {self.users_[self.next_]}"
                   return True, msg

           else:   # Автоматические координаты от компьютера
               quit_game, x, y = self.get_comp_coord(board_)

           msg = ['' for i in range(self.board_.size_map)]
           msg[0] = f"Ход игрока {self.current_game[self.users_[self.next_]][1]} - ({x + 1},{y + 1})"

           msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]

           #self.board_.paint_board(msg)

           logging.info(f"Получены координаты , игрок {self.users_[self.next_]} - ({x},{y})")
           logging.info(f" type_next_player = {type_next_player}")

           # Ответ игрока2 на ход игрока1
           if type_next_player == '1': #   Ручной ответ от соперника user

               res_move = self.check_comp_coord(x, y, board_)
               if res_move: # Ход принят, возвращен результат

                   board_.update_user_map(res_move, x, y, self.users_[not self.next_]) # Компьютер обновляет карту user
                   self.board_.paint_board(self.board_.msg_list)
                   time.sleep(3)
                   break
               else: # Ход не принят. Координаты уже использованы ранее
                   pass

           else: # Автоматический ответ компьютера и обновление карты comp
               res_move = self.check_user_coord(x, y, board_)
               if res_move: # Ход принят, возвращен результат
                   break
               else: # Ход не принят. Координаты уже использованы ранее         
                   pass                                                     

       logging.info(f"Получен ответ от игрока {self.users_[not self.next_]} - {res_move}")
       print(f"{__LINE__}: Ответ игрока {self.users_[not self.next_]} - {res_move}")

       # Проверяем, не уничтожены ли все корабли у следующего игрока.

       if board_.check_win(self.users_[not self.next_]):
           msg = f"Игра закончена, победил игрок {self.users_[self.next_]}. Всего сделано :{self.count_move} ходов"
           return True, msg

       self.next_ = not self.next_
       return False, ''

    def get_comp_coord(self, board): # Рассчет координат компьютером
        time.sleep(0.5)
        key_ = self.users_[not self.next_] # Следующий игрок
        key_present =     self.users_[self.next_]
        s = []

        for i in range(board.size_map):
            for j in range(board.size_map):
                if board.board_map[key_][i][j].status_  in ['free','busy']:
                    logging.info(f" Проверяем точку board.board_map[{key_}][{i}][{j}].status_ = {board.board_map[key_][i][j].status_ }  на соседство с ранеными или убитыми кораблями")

                    m1 = [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (1, -1), (1, 1)]
                    m2 = board.check_dot(i,j,['killed'], m1, board.board_map[key_]) # Проверка на все соседние "убитые" точки

                    m3 = [(-1, -1),(-1, 1), (1, -1), (1, 1)]
                    m4 = board.check_dot(i, j, ['X'], m3, board.board_map[key_]) # Проверка на  соседние диагональные "раненые"
                    if not (m2 and m4) :    #flag:
                        s.append((board.board_map[key_][i][j].x, board.board_map[key_][i][j].y))
                        #logging.info(f" В список точек хода компа добавлена ({board.user_map[i][j].x},{board.user_map[i][j].y})")

        logging.info(f" список свободных ячеек для хода comp {s}")
        random_dot_move = random.choice(s)
        #dot_move_row_ = random_dot_move[0] + 1
        #dot_move_col_ = random_dot_move[1] - board.size_map + 1
        dot_move_row_ = random_dot_move[0]
        dot_move_col_ = random_dot_move[1]
        logging.info(f" Ход игрока { key_present} ({dot_move_row_ },{dot_move_col_})")
        print(f"{__LINE__}: Ход игрока {key_present} ({dot_move_row_ + 1},{dot_move_col_ + 1})")
        return True, dot_move_row_, dot_move_col_
        #self.check_comp_move(random_dot_move[0],random_dot_move[1], board)
        #board.check_comp_move(random_dot_move[0],random_dot_move[1])

        #result = board.check_move(x, y, board.comp_map)

        #input(f"{__LINE__}: контроль хода комп, проверь log")

    def get_user_coord(self,board):
        # Ход игрока

        logging.info(f"Ход игрока")
        #board.
        text_ = "Введите значение: "
        #self.board_.input_(text_)
        while True:

            #print(f"Ход игрока. Введите координаты XY")
            #m = input(f"X -по вертикали, Y - по горизонтали, Q - выход :")
            m = self.input_(text_)
            m1 = re.match(r'([Qq]$)|(\d{1})\W*(\d{1})', m)
            if m1:
                logging.info(f" {m1.group(1), m1.group(2), m1.group(3)}")
                if m1.group(1):
                   #pass
                   #finish_game(): # Завершение игры по инициатеве user
                   logging.info(f" Игра прервана.")
                   #break
                   return True, 0,0
                else:

                    x = int(m1.group(2)) - 1
                    y = int(m1.group(3)) - 1

                    if (x in range(board.size_map))  and (y in range(board.size_map)):
                        status_dot =  board.board_map[self.users_[self.next_]][x][y].status_
                        if status_dot != 'free':
                            msg = ['' for i in range(self.board_.size_map)]
                            msg[0] = f"Ошибка. Такой ход уже был."
                            msg[1] = f"Повторите ввод"
                            msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                            self.board_.paint_board(msg)
                            logging.error(f" Такой ход уже был, повторите ввод")
                            #print(f"{__LINE__}:Такой ход уже был, повторите ввод")
                        else:
                            logging.info(f" Ход  {self.users_[self.next_]} ({x},{y})")
                            msg = ['' for i in range(self.board_.size_map)]
                            msg[0] = f"{self.current_game[self.users_[self.next_]][1]} - ({x + 1},{y + 1})"

                            msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                            self.board_.msg_list = msg
                            #self.board_.paint_board(msg)
                            #input(f"{__LINE__}: контроль")


                            return False, x,y

                    else:
                        msg = ['' for i in range(self.board_.size_map)]
                        msg[0] = f"Координаты вне диапазона поля, повторите ввод"

                        msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                        self.board_.paint_board(msg)
                        logging.error(f" Координаты вне диапазона поля, повторите ввод ")
                        #print(f"Координаты вне диапазона поля, повторите ввод")
            else:
                logging.error(f" неверные координаты {m}")
                print(f"Недопустимые символы, повторите ввод")
                msg = ['' for i in range(self.board_.size_map)]
                msg[0] = f"Недопустимые символы, повторите ввод"

                msg = [f"{msg[i]:<48}" for i in range(self.board_.size_map)]
                self.board_.paint_board(msg)




    def check_user_coord(self, x, y, board_ ): # Проверка введенных координат user
    #def update_comp_map(self, x, y, board_): #Обновление компьютером своей карты
        dot_ = board_.board_map[self.users_[not self.next_]]
        logging.info(f" start ({x},{y}) - {dot_[x][y].status_}")

        if dot_[x][y].status_ == 'free':
            result = 'Мимо'

            dot_[x][y].status_ = 'T'
            logging.info(f" dot_[{x}][{y}].status_ = 'T'")
        elif dot_[x][y].status_ == 'busy':
            logging.info(f" dot_[x][y].status_ == 'busy'")
            try:
                ship_= dot_[x][y].ship
                ship_.life_ -= 1
                ship_life = ship_.life_
                logging.info(f" проверка объект ship {ship_}, life {ship_.life_}, {ship_.long}, dot_[{x}][{y}] {dot_[x][y].ship}")
            except Exception as er:
                logging.error(f"Ошибка ship_= dot_[x][y].ship или ship_life = ship_.life: {er}")
            logging.info(f" ship_ = {ship_}, ship_life = {ship_life}")
            if ship_life > 0 :
                result = 'Ранен'
                dot_[x][y].status_ = 'X'
                logging.info(f" dot_[{x}][{y}].status_ = 'X'")
            else:
                result = 'Убит'
                row0  = ship_.row_
                col0 = ship_.col_
                direct_ = ship_.direction
                for i in range(ship_.long):
                    x = row0 + (0 if direct_ == 'H' else i)
                    y = col0 + (0 if direct_ == 'V' else i)
                    dot_[x][y].status_ = 'killed'
                logging.info(f" dot_[{x}][{y}].status_ = 'Убит'")
        else:
            logging.info(f"Такой ход уже был")
            print(f"{__LINE__} Такой ход уже был, повторите ввод")
            input(f"{__LINE__}: контроль")
            result = False
        logging.info(f"Результат хода - {result}")

        return result


    def check_comp_coord(self, x, y, board_): #Получение от user результата хода comp
        m1 = {'1': 'Мимо', '2': 'Ранен', '3': 'Убит'}
        m2 = {'1': 'T', '2': 'X', '3': 'Убит'}
        logging.info(f"board_= {board_}")
        while True:


            r = self.get_user_answer() # получение ручного ответа от user
            res = m1[r.group()]

            if res:
                logging.info(f"ответ игрока {self.users_[not self.next_]}: {res}")
                print(f"{__LINE__}: ответ игрока {self.users_[not self.next_]}: {res}")
                res11, msg11 = self.check_error_on_user_answer(board_, res, x, y)
                logging.info(f" Результат проверки user's answer {res11},{msg11}")

                if res11:
                    #res1, msg1 = board_.update_user_map (res, x, y, self.users_[not self.next_])  #Обновление карты по итогам хода.

                    msg = f"{self.current_game[self.users[not self.next_]]} ответ {res}"
                    self.board_msg_list[0] = (self.board_msg_list[0] +
                                              f"{msg:<24}")

                    return res
                    #break
                else:
                    print(f"{__LINE__}: {msg11}")
                    logging.info(f" Ответ user {msg11}")
            else:
                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")

    def get_user_answer(self):
        msg_1 = self.board_.msg_list[0]
        while True:

            self.board_.msg_list[1] = f"Введите результат хода. 1 - мимо, 2 -ранен, 3 - убит"
            self.board_.msg_list[2] = f"1 - мимо"
            self.board_.msg_list[3] = f"2 - ранен"
            self.board_.msg_list[4] = f"3 - убит"
            self.board_.paint_board(self.board_.msg_list)
            m = self.input_("Результат: ")
            #m = input(f"Введите результат хода. 1 - мимо, 2 -ранен, 3 - убит :")

            res = re.match(r'([1-3]{1})', m)

            if not res:
                self.board_.msg_list[5] = f"некорректный выбор ответа, повторите ввод"
                logging.info(f"некорректный выбор ответа")
                #print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")
            else:

                logging.info(f" принят корректный ответ user {res.group()}")
                return res


    def check_error_on_user_answer(self, board_, res, x, y):  # Проверяем ответ user на корректность
        row_ = x
        col_ = y
        #m = res.group()
        logging.info(f"Проверяем ответ {res} игрока {self.users_[not self.next_]}  на ход игрока {self.users_[self.next_]} ({x},{y})")
        logging.info(f" board = {board_})")
        dots_list = board_.board_map[self.users_[not self.next_]]
        #if m == '1':  # Ход мимо
        if res == 'Мимо' :
            # board.user_map[row_][col_].status_ = 'T'
            return True, ''

        #elif m == '2':  # Ранен
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
                ''' Не доделано                                                                                                         
                elif ship_damaged == 1:                                                                                                 
                    logging.info(f" Проверяем, есть ли свободные для хода клетки с концов корабля")                                     
                    delta_row = row_ - row_2                                                                                            
                    delta_col = col_ - col_2                                                                                            
                    if delta_row:                                                                                                       
                        if min(row_, row_2) > 0:                                                                                        
                            row_min  = min(row_, row_2)                                                                                 
                            col_min = col_                                                                                              
                        elif max(row_, row_2) < board.size_map - 1:                                                                     
                            row_max = max(row_, row_2)                                                                                  
                            col_max = col_                                                                                              
                    '''


        #elif m == '3':  # Убит
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


def main_game():

    Board_width = Board_length = 6 # Задаем размерность полей
    ships_list =[(1,4), (2,2), (3,1)] # ключ - длина корабля, значение - количество кораблей этой длины
    board_ = Board(size_map = 6, ships_list = ships_list)
    player_= Player()


    while True:
        board_.paint_board()
        player_.make_move(board_)
        win_, gamer_win = board_.check_win (player_.next_)
        if win_:
            print(f"{__LINE__}: Игра закончена, выиграл {gamer_win}")
            logging.info("Игра закончена, выиграл {gamer_win}")
            return True


def main_game_new():
    # 03082025
    board_long = 6 # Задаем размерность полей
    ships_list =[(1,4), (2,2), (3,1)] # ключ - длина корабля, значение - количество кораблей этой длины

    board_ = Board_new(size_map = board_long, ships_list = ships_list)
    player_ = Player_new(board_ = board_)
    #board_.player = player_




    while True:
        #board_.paint_board(player_)

        quit_game, msg = player_.make_move(board_)
        if quit_game:
            board_.paint_board(player_)
            print(f"{__LINE__}:{msg}")
            logging.info(f"{msg }")
            return True





if __name__ == '__main__':
    #main_game()
    main_game_new()













