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

    def find_start_coordinate(self,long, map_board):
        """Возвращает начальные координаты для размещения корабля, длиной long
        return x,y """


        # Ищем случайное число типа корабля - горизонтальный, вертикальный
        type_boat_index = random.randrange(0, self.dim_board)  % 2 # 0 - вертикальный,  не 0 - горизонтальный

        type_boat = 'H' if type_boat_index else 'V'
        if type_boat_index:
            col_= random.randrange(1, self.dim_board - long) # если type горизонтальный, столбец может быть от 1 до dim_board - long
            row_ = random.randrange(1,6) # строка может быть любой из размера поля

        else:
            col_ = random.randrange(1, self.dim_board - long)  # если вертикальный, строка может быть от 1 до dim_board - long
            row_ = random.randrange(1, 6)
        return row_, col_, type_boat

        # Проверяем, может ли быть размещен корабль с полученными параметрами , с учетом текущего состояния поля

        res = Ship(row_start, col_start, )


        # Ищем случайное число строки
        # Ищем случайное число стобца
        # Перебираем все строки и столбцы и находим подъодящую точку начала корабля
        # Возвращаем координаты начала и тип корабля.

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

    def __init__(self, row_start, col_start, long, type_, current_map):
        self.row_start = row_start # начальный столбец
        self.col_start, = col_start # начальная строка
        self.long = long # длина
        self.type_ = type_ # расположение - вертикальное или горизонтальное
        self.current_map = current_map # текущая карта поля

    def check_coordinate(self):
        s  = []
        if type_ == 'H':
            for i in range(-1, long+2): # идем вдоль корабля
                # если горизонтальное направление , увеличиваем col
                # если вертикальное  - увеличиваем row
                






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
    s = map_.create_coordinate()
    # map_.paint_board(s)
    row_, col_, type_boat_ = map_.find_free_dot(1, s)
    print (f"{__LINE__}: {row_}, {col_}, {type_boat_}")




