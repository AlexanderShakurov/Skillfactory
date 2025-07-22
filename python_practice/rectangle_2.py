import sys
sys.path.append(r'D:\projects\Skillfactory\practice_C1')

from Rectangle import Rectangle, Square, Circle, SquareFactory

#далее создаём два прямоугольника
p = SquareFactory.get_side(12)
print(p.a)
