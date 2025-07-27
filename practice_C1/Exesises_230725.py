import inspect
import random

from tornado.wsgi import to_wsgi_str


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



class Map:

    ships_list =[(1,4), (2,2), (3,1)] # ключ - длина корабля, значение - количество

    def __init__(self, dim_board):
        self.dim_board = dim_board
        print(f"{__LINE__}: {type(self.dim_board)}")

    def create_coordinate(self):  # начальное создание точек поля
        """ (a,x,y)
        a in ['free', ship_class_name, X, T"""
        
        s = [[Dot(j, i) for i in range(0, self.dim_board )] for j in range(0, self.dim_board )]

        return s

    def create_ships(self, dots_list):

        ship= {}
        ships_list1 = sorted(self.ships_list, reverse=True)

        for i in ships_list1:
            for j in range(i[1]):

                ship[f"{i[0]}-{j}"] = Ship(i[0])
                ship[f"{i[0]}-{j}"].find_free_place(dots_list)
                dots_list = self.place_the_ship(ship[f"{i[0]}-{j}"], dots_list)
        return dots_list

    def place_the_ship(self, ship, dots_list): # записываем координаты точек корабля в объекты точек
        s =[]
        row_ = ship.row_
        col_ = ship.col_

        for i in range(ship.long):
            row1_ = row_ + i if ship.direction == 'V'  else row_
            col1_ = col_ + i if ship.direction == 'H'  else col_
            input(f"{__LINE__}:(row1_, col1_) ({row1_}, {col1_})")
            dots_list[row1_][col1_].status_ = 'busy'
            dots_list[row1_][col1_].ship = ship
            s.append( dots_list[row1_][col1_])
        return dots_list


    def paint_board(self, dot_board):    # рисует доску по списку с точками
        char_ = {'free':'О', 'busy':'B'}
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

    def __init__(self, long, direction = None, row_ = None, col_= None):
        self.long = long # длина корабля
        self.direction = direction # направление корабля, H - горизонт, V - вертик.
        self.row_ = row_ # начальная координата (строка)
        self.col_ = col_ # начальная координата (столбец)

      

    def find_free_place(self, dots_list):
        # dots_list - текущее состояние точек поля
        """ случайно выбирается тип размещения, H - горизонтальный или V - вертикальный
            и координаты начала корабля"""
        type_boat_index = random.randrange(0, map_.dim_board) % 2  # 0 - вертикальный,  не 0 - горизонтальный
        self.direction = 'H' if type_boat_index else 'V'

        print(f"{__LINE__}: длина корабля {self.long}, направление {self.direction} ")


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
            for i in range(0, map_.dim_board - self.long + 1):
                
                count_row = 0
                #for row_ in range (0, map_.dim_board ):
                for j in range (0, map_.dim_board ):
                    col_, row_ = i, j


                    list_ = [True if dots_list[row_][col_ + j].status_ == 'free' else False for j in range(self.long)]

                    if col_ == 0 :
                        list_.append(True if dots_list[row_][col_+ self.long ].status_ == 'free' else False )
                    elif col_ == map_.dim_board - self.long  :
                          
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


                        if count_row == 3:
                            # если набралось три подряд строки с long + 2 точками 'free'
                            # добавляем точку в список возможных точек начала корабля

                            #col_start = col_ + 1 if col_ else col_

                            col_start = col_
                            dots_for_start.append(dots_list[row_ -1][col_start])
                            print(f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                            count_row = 2
                        elif count_row == 4:
                            col_start = col_
                            dots_for_start.append(dots_list[row_ - 1][col_start]) # точка из предпоследней строки
                            print(f"{__LINE__}: ({row_ - 1},{col_start}) добавлена в список точек старта")
                            dots_for_start.append(dots_list[row_][col_start]) # точка из последней строки
                            print(f"{__LINE__}: ({row_ },{col_start}) добавлена в список точек старта")
                        elif count_row == 3:
                               col_start = col_
                               dots_for_start.append(dots_list[row_ -1][col_start])
                               print(f"{__LINE__}: ({row_ -1},{col_start}) добавлена в список точек старта")
                               count_row = 2



                    else: # в строке row_ среди {long}+2 точках есть занятая
                        print(f"{__LINE__}: не все True")
                        count_row = 0


        if self.direction == 'V'  : # Вертикальное расположение
            for i in range(0, map_.dim_board - self.long + 1):

                count_row = 0
                #for row_ in range (0, map_.dim_board ):
                for j in range (0, map_.dim_board ):
                    col_, row_ = j ,i
                    print(f"{__LINE__}: i = {i}, j = {j}")

                    list_ = [True if dots_list[row_ + j][col_].status_ == 'free' else False for j in range(self.long)]
                    list_w = [f"({dots_list[row_ + j][col_].x}, {dots_list[row_ + j][col_].y})-{ dots_list[row_ + j][col_].status_ }" for j in range(self.long)]
                    if row_ == 0 :
                        list_.append(True if dots_list[row_+ self.long ][col_].status_ == 'free' else False )
                        list_w.append(f"({dots_list[row_ + self.long][col_].x}, {dots_list[row_ + self.long][col_].y})-{dots_list[row_ + self.long][col_].status_}" )
                    elif row_ == map_.dim_board - self.long :

                        list_.insert(0,True if dots_list[row_-1][col_ ].status_ == 'free' else False)
                        list_w.insert(0, f"({dots_list[row_ -1][col_].x}, {dots_list[row_ -1][col_].y})-{dots_list[row_ -1][col_].status_}")
                    else:
                        list_.append(True if dots_list[row_+ self.long ][col_ ].status_ == 'free' else False )
                        list_.insert(0, True if dots_list[row_ - 1][col_ ].status_ == 'free' else False)
                        list_w.append(f"({dots_list[row_ + self.long][col_].x}, {dots_list[row_ + self.long][col_].y})-{dots_list[row_ + self.long][col_].status_}" )
                        list_w.insert(0, f"({dots_list[row_ - 1][col_].x}, {dots_list[row_ - 1][col_].y})-{dots_list[row_ - 1][col_].status_}")

                    print(f"{__LINE__}: ({row_},{col_}) - {list_w}")

                    if all(list_):

                        if col_ == 0:
                            count_row += 2
                            print(f"{__LINE__}: row_ = {row_}, col_ = 0, count_row = {count_row}")
                        elif (col_ == map_.dim_board  - 1 ) and count_row > 0:
                            count_row = 4
                            print(f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")
                        else:

                            count_row  += 1
                            print(f"{__LINE__}: row_ = {row_}, col_ = {col_}, count_row = {count_row}")



                        if count_row == 3 :

                            # если набралось три подряд строки с long + 2 точками 'free'
                            # добавляем точку в список возможных точек начала корабля

                            #col_start = col_ + 1 if col_ else col_

                            row_start = row_
                            dots_for_start.append(dots_list[row_start][col_ - 1])
                            print(f"{__LINE__}: ({row_start},{col_ - 1}) добавлена в список точек старта")
                            count_row = 2

                        elif count_row == 4 :

                            #col_start = col_
                            row_start = row_
                            dots_for_start.append(dots_list[row_start][col_ - 1]) # точка из предпоследней строки
                            print(f"{__LINE__}: ({row_start},{col_-1}) добавлена в список точек старта")
                            dots_for_start.append(dots_list[row_start][col_]) # точка из последней строки
                            print(f"{__LINE__}: ({row_start },{col_}) добавлена в список точек старта")
                    else: # в строке row_ среди {long}+2 точках есть занятая
                        print(f"{__LINE__}: не все True , count_row  = 0")
                        count_row = 0
        print(f"{__LINE__}: количество точек {len(dots_for_start)}")

        random_dot_start = random.choice(dots_for_start)

        x = random_dot_start.x
        y = random_dot_start.y
        self.row_ = x
        self.col_ = y
        print(f"{__LINE__}: (x,y) = ({x},{y}) - {self.direction}")
        return random_dot_start.x, random_dot_start.y,  self.direction





































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
    dots_list = map_.create_coordinate() # список из всех точек поля
    #dots_list_all[2][1].status_= 'busy'
    #print(f"{__LINE__}: {dots_list_all[2][1].x}, {dots_list_all[2][1].y}")

    dots_list = map_.create_ships(dots_list)
    #x_start, y_start, type_direction = ship3.find_free_place(dots_list_all)
    #dots_list_all  = map_.place_the_ship(ship3,dots_list_all )
    map_.paint_board(dots_list )





    print(f"{__LINE__}: stop")





