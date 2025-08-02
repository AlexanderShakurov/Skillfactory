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

    

    def __init__(self, size_map, ships_list,ships_user = None, ships_comp = None, comp_map = None):
        self.size_map= size_map
        self.ships_list = ships_list

        self.comp_map = [[Dot(j, i) for i in range(0, self.size_map )] for j in range(0, self.size_map )] # список точек доски comp
        #logging.info(f"Создан comp_map")
        self.user_map = [[Dot(j, i) for i in range(0 + self.size_map, 2 * self.size_map )] for j in range(0, self.size_map)]
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
        logging.info(f"Обновление dot, ship, board по результату хода comp ({x},{y}) - {m}")

        if m == '1': # Ход мимо
            self.user_map[row_][col_].status_ = 'T'

        elif m == '2': # Ранен
            logging.info(f"Обработка ответа Ранен от user ")

            logging.info(f"Поиск среди соседних клеток раненых и убитых ")
            m1 = [(-1, -1),(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, ['X', 'killed'], m1)
            if len(m2) > 1 :
                msg = "Некорректный ответ. У раненой клетки не может быть более 1 соседней клетки с кораблем"
                logging.info(msg)

                return False, msg

            logging.info(f"Поиск среди соседних диагональных клеток раненых или убитых ")
            m1 = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
            m2 = self.check_dot(row_, col_, ['X', 'killed'], m1)
            if m2:
                msg = "Некорректный ответ. У раненой клетки не может быть диагональной соседней клетки с кораблем"
                logging.info(msg)

                return False, msg


            logging.info(
                f"Проверяем смежные клетки (кроме диагональных) на предмет ранен, для объединения в один корабль")
            m1 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            m2 = self.check_dot(row_, col_, ['X'], m1)


            if m2:
                logging.info(f"Найдена соседняя раненая точка {m2} ")
                row_2, col_2 = m2[0][0], m2[0][1]

                ship_damaged = self.user_map[row_2][col_2].ship
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

                        self.user_map[row_][col_].ship = ship_damaged
                        logging.info(f" точке ({row_}{col_}) присвоен корабль {ship_damaged}")
                        break

                # s = [self.ships_user[k] for k,v in self.ships_user.items() if not self.ships_user[k].long]
                # ship_killed = s[0]
                logging.info(f"Выбран неиспользуемый корабль {ship_damaged}")


        elif m == '3': # Убит

            self.user_map[row_][col_].status_ = 'killed'
            logging.info(f"Обработка ответа Убит от user ")
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
        # Вставка 30.07.2025
        for i in range(self.size_map):
            board1, board2 = f"{count_row} |", f"{count_row} |"
            for j in range(self.size_map):
                board1 += char_[self.comp_map[i][j].status_] + '|'
                #logging.info(f"self.user = {self.user_map[i][j].status_}")
                board2 += char_[self.user_map[i][j].status_] + '|'
            count_row += 1
            print(f"{board1}  --  {board2}")
        return True

    def check_comp_move(self, x, y, player_obj, player_type = 'user', res = None): #Получение от user результата хода comp
        m1 = {'1': 'Мимо', '2': 'Ранен', '3': 'Убит'}
        m2 = {'1': 'T', '2': 'X', '3': 'Убит'}
        while True:

            if player_type == 'user':
                res = player_obj.user_answer() # получение ручного ответа от user

            '''
            logging.info(f" ждем ответа от user")
            while True:
                m = input (f"Введите результат хода. 1 - мимо, 2 -ранен, 3 - убит :")
                m1 = {'1':'Мимо', '2': 'Ранен', '3': 'Убит'}
                m2 = {'1':'T', '2': 'X', '3': 'Убит'}
                res = re.match(r'([1-3]{1})',m)
            '''

            if res:
                logging.info(f"ответ user: {m1[res.group()]}")
                print(f"{__LINE__}: Результат хода - {m1[res.group()]}")
                res1, msg1 = self.update_user_map (res, x, y)  #Обновление карты по итогам хода.
                if res1:
                    break
                else:
                    print(f"{__LINE__}: {msg1}")
            else:
                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")



    def check_move(self, x, y, dot_ ): # Проверка введенных координат user
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
                        result = board.check_move(x, y, board.comp_map)
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
                res1, msg1 = board.update_user_map (res, x, y)  #Обновление карты по итогам хода.
                if res1:
                    break
                else:
                    print(f"{__LINE__}: {msg1}")
                    logging.info(f" Ответ user {msg1}")
            else:
                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")

    def user_answer(self): # Получение ответа от игрока user на ход comp
        logging.info(f" ждем ответа от user")
        while True:
            m = input(f"Введите результат хода. 1 - мимо, 2 -ранен, 3 - убит :")

            res = re.match(r'([1-3]{1})', m)

            if not res:

                logging.info(f"некорректный выбор ответа")
                print(f"{__LINE__}:некорректный выбор ответа, повторите ввод")
            else:

                logging.info(f" принят корректный ответ user {res.group()}")
                return res

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


    while True:
        board_.paint_board()
        player_.make_move(board_)
        win_, gamer_win = board_.check_win (player_.next_)
        if win_:
            print(f"{__LINE__}: Игра закончена, выиграл {gamer_win}")
            logging.info("Игра закончена, выиграл {gamer_win}")
            return True





if __name__ == '__main__':
    main_game()
    #board= Board(6)

    











