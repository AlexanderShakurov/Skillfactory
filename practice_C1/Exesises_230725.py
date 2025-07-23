class Map:
    high = 6
    width = 6

    def __init__(self):
        self.x = x
        self.y = y



    def map_update(self):
        """обновление координат
           прорисовка поля"""
        pass


class Ship:

    def __init__(self, x, y, long):
        self.x = x
        self.y = y
        self.long = long


def see_butle():

    map_width = map_length = 6 """ Задаем размерность полей"""
    ship_type = dict()
    user_map = Map(6,6)
    ai_map = Map(6,6)
    user_map.update(0, 0) """ создаем карту игрока user """
    ai_map.apdate(0, 0) """ создаем карту игрока ai """

    first_step() # определение, чей первый ход
    """Создаем классы кораблей"""
    ship3_1 = Ship(3)
    ship2_1 = Ship(2)
    ship2_2 = Ship(2)
    ship1_1 = Ship(1)
    ship1_2 = Ship(1)
    ship1_3 = Ship(1)
    ship1_4 = Ship(1)
