import inspect
import random
import re
import logging
import time




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

                            elif (row_ == size_map  - 1 ) and count_row > 1:
                                count_row = 4

                            else:

                                count_row  += 1



                            if count_row == 3:
                                # если набралось три подряд строки с long + 2 точками 'free'
                                # добавляем точку в список возможных точек начала корабля

                                #col_start = col_ + 1 if col_ else col_

                                col_start = col_
                                dots_for_start.append(dots_list[row_ -1][col_start])
                                count_row = 2
                            elif count_row == 4:
                                col_start = col_
                                dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                                dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                            elif count_row == 3:
                                   col_start = col_
                                   dots_for_start.append(dots_list[row_ -1][col_start])
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


