import inspect
import random


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

    def __init__(self, x, y, status_ ='free') :

        self.x = x
        self.y = y
        self.status_ = status_

class Map:

    def __init__(self, dim_board):
        self.dim_board = dim_board
        print(f"{__LINE__}: {type(self.dim_board)}")

    def create_coordinate(self):  # начальное создание точек поля
        """ (a,x,y)
        a in ['free', ship_class_name, X, T"""
        
        s = [[Dot(i, j) for i in range(1, self.dim_board + 1)] for j in range(1, self.dim_board + 1)]
        return s

    def paint_board(self, dot_board):    # рисует доску по списку с точками
        char_ = {'free':'О'}
        board0 = '   1 2 3 4 5 6   --     1 2 3 4 5 6 '
        print(board0)
        board0 = '  -------------  --    -------------'
        print(board0)
        count_row = 1
        for i in dot_board:

            board1, board2 = f"{count_row} |", f"{count_row} |"
            for j in i:
                board1 += char_[j.status_] + '|'
                board2 += char_[j.status_] + '|'
            count_row += 1
            print (f"{board1}  --  {board2}")
        return dot_board

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
        Передает координаты update_map
        Возвращает x, y """
        pass

    def whos_first_strike(self):
        """Определяет , чей первый ход
        Возвращает gamer in ['comp', 'user]"""
        pass

class Ship:

    def __init__(self, long):
        self.long = long # длина корябля

      

    def find_free_place(self, dots_list):
        # dots_list - текущее состояние точек поля
        """ случайно выбирается тип размещения, H - горизонтальный или V - вертикальный
            и координаты начала корабля"""
        type_boat_index = random.randrange(0, map_.dim_board) % 2  # 0 - вертикальный,  не 0 - горизонтальный
        type_boat = 'H' if type_boat_index else 'V'

        print(f"{__LINE__}: длина корабля {self.long}, направление {type_boat} ")


        #  Горизонтальное расположение

        s = {}
        """ Идем по очереди, по строкам. Проверяем точки от (col_, row_) до (col_ + long_, row_
        на dot.staus_ == 'free'
        Если все точки 'free', записываем в s[row_]  True, иначе False
        Если набралось три подряд идущие s[i] = True, отмечаем точку (col_ + 1, row_ + 1) как одну из возможных
        точек начала корабля.
        Добывляем найденную точку в список точек, из которого потом случайным образом будет выбрана одна 
        и присвоена данному экземпляру корабля в качестве начальной."""
        dots_for_start = [] # список возможных точек начала корабля
        #for col_ in range(0, map_.dim_board - self.long + 1):# идем по столбцам от -1 до map_.dim_board - self.long)
        type_boat = 'V'
        if type_boat == 'H'  :
            for i in range(0, map_.dim_board - self.long + 1):
                
                count_row = 0
                #for row_ in range (0, map_.dim_board ):
                for j in range (0, map_.dim_board ):
                    col_, row_ = i, j


                    list_ = [True if dots_list[row_][col_].status_ == 'free' else False for j in range(self.long)]

                    if (col_ == 0 and type_boat == 'H' ) :
                        list_.append(True if dots_list[row_][col_+ self.long ].status_ == 'free' else False )
                    elif (col_ == map_.dim_board - self.long and type_boat == 'H' ) :
                          
                        list_.insert(0,True if dots_list[row_][col_ - 1].status_ == 'free' else False)
                    else:
                        list_.append(True if dots_list[row_][col_ + self.long ].status_ == 'free' else False )
                        list_.insert(0, True if dots_list[row_][col_ - 1].status_ == 'free' else False)



                    print(f"{__LINE__}: ({row_},{col_}) - {list_}")

                    if all(list_):

                        if row_ == 0:
                            count_row += 2
                            print(f"{__LINE__}: row_ = {row_}")
                        elif (row_ == map_.dim_board  - 1 ) and count_row > 0:
                            count_row = 4
                            print(f"{__LINE__}: row_ = {row_}")
                        else:
                            print(f"{__LINE__}: row_ = {row_}")
                            count_row  += 1
                        print(f"{__LINE__}: count_row = {count_row}")


                        if (count_row == 3) and (type_boat == 'H' ) :
                            # если набралось три подряд строки с long + 2 точками 'free'
                            # добавляем точку в список возможных точек начала корабля

                            #col_start = col_ + 1 if col_ else col_

                            col_start = col_
                            dots_for_start.append(dots_list[row_ -1][col_start])
                            print(f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                            count_row = 2
                        elif (count_row == 4) and (type_boat == 'H' ) :
                            col_start = col_
                            dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                            print(f"{__LINE__}: ({row_ - 1},{col_start}) добавлена в список точек старта")
                            dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                            print(f"{__LINE__}: ({row_ },{col_start}) добавлена в список точек старта")
                        elif (count_row == 3) and (type_boat == 'V' ):
                               col_start = col_
                               dots_for_start.append(dots_list[row_ -1][col_start])
                               print(f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                               count_row = 2



                    else: # в строке row_ среди {long}+2 точках есть занятая
                        print(f"{__LINE__}: не все True")
                        count_row = 0


        if type_boat == 'V'  :
            for i in range(0, map_.dim_board - self.long + 1):

                count_row = 0
                #for row_ in range (0, map_.dim_board ):
                for j in range (0, map_.dim_board ):
                    col_, row_ = j ,i


                    list_ = [True if dots_list[row_][col_].status_ == 'free' else False for _ in range(self.long)]

                    if (col_ == 0 and type_boat == 'V' ) :
                        list_.append(True if dots_list[row_][col_+ self.long ].status_ == 'free' else False )
                    elif (col_ == map_.dim_board - self.long and type_boat == 'V' ) :

                        list_.insert(0,True if dots_list[row_][col_ - 1].status_ == 'free' else False)
                    else:
                        list_.append(True if dots_list[row_][col_ + self.long ].status_ == 'free' else False )
                        list_.insert(0, True if dots_list[row_][col_ - 1].status_ == 'free' else False)
                    print(f"{__LINE__}: ({row_},{col_}) - {list_}")

                    if all(list_):

                        if row_ == 0:
                            count_row += 2
                            print(f"{__LINE__}: row_ = {row_}")
                        elif (row_ == map_.dim_board  - 1 ) and count_row > 0:
                            count_row = 4
                            print(f"{__LINE__}: row_ = {row_}")
                        else:
                            print(f"{__LINE__}: row_ = {row_}")
                            count_row  += 1
                        print(f"{__LINE__}: count_row = {count_row}")


                        if (count_row == 3) and (type_boat == 'V' ) :

                            # если набралось три подряд строки с long + 2 точками 'free'
                            # добавляем точку в список возможных точек начала корабля

                            #col_start = col_ + 1 if col_ else col_

                            col_start = col_
                            dots_for_start.append(dots_list[row_ -1][col_start])
                            print(f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                            count_row = 2

                        elif (count_row == 4) and (type_boat == 'V' ) :

                            col_start = col_
                            dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                            print(f"{__LINE__}: ({row_ - 1},{col_start}) добавлена в список точек старта")
                            dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                            print(f"{__LINE__}: ({row_ },{col_start}) добавлена в список точек старта")
                    else: # в строке row_ среди {long}+2 точках есть занятая
                        print(f"{__LINE__}: не все True")
                        count_row = 0
        print(f"{__LINE__}: {dots_list}")
        return dots_list





































def main_game():

    map_width = map_length = 6 # Задаем размерность полей
    ship_type = dict() # Длины - количество кораблей
    ship_type[1]= 4
    ship_type[2]= 2
    ship_type[3]= 1

    map_ = Map(6,6)

    ships = []
    for i in range(len(ship_type, -1)):
        for j in range(ship_type[i]):
            x, y = map.free_coordinate(i) # "Получаем начальные координаты корабля, исходя из его длины
            ships.append(Ship(i,j, x, y)) #Создаем экземпляр корабля и добавляем в список экземпляров кораблей

    next_gamer = {0:'comp', 1:'user'}

    next_gamer_index = map.whos_first_strike() # возвращает индекс игрока, чей первый ход, 0: comp, 1: user

    x, y, = 0, 0  # начальные координаты игры, для инициализации чистого поля

    while True: # Игра началась
        map_.update_map(x, y)
        map_.strike(next_gamer[next_gamer_index])
        next_gamer_index = not next_gamer_index



if __name__ == '__main__':
    map_ = Map(6)
    print(f"{__LINE__}:{map_.dim_board}")
    dots_list_all = map_.create_coordinate() # список из всех точек поля

    ship3 = Ship(3)
    dot_list_for_start = ship3.find_free_place(dots_list_all)

    for i in dot_list_for_start :
        print(f"{__LINE__}: {i}")





