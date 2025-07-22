

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_attrs(self):
        return f"Rectangle: {self.x}, {self.y}, {self.width}, {self.height}"

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b



class Square:
    '''Напишите класс SquareFactory с одним статическим методом,
    принимающим единственный аргумент — сторону квадрата.
     Данный метод должен возвращать объект класса Square с переданной стороной.'''
    '''Создать вычисляемое свойство для класса Square.
    Сделайте метод по вычислению площади свойством.
    Сделайте сторону квадрата свойством, которое можно установить только через сеттер.
    В сеттере добавьте проверку условия, что сторона должна быть неотрицательной.'''

    def __init__(self,side = None):
        self.__side = side

    @property
    def area(self):
        return self.__side ** 2

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, a):
        if a < 0:
            raise ValueError("Side must be more then 0")
        else:
            self.__side = a


class SquareFactory:
    def __init__(self,a):
        self.a = a

    @staticmethod
    def get_side(a):
        return Square(a)

class Circle:
    def __init__(self, r):
        self.r = r
    def get_area_circle(self):
        return 3.1415926 * self.r ** 2
