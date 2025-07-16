import inspect
import random
import time
import re


n = 3 # размерность поля
win_strategy_flag = False # вспомогательный флаг, True - если обнаружится выигрышная стратегия



# Функции **************************************
# main_func - основной запуск программы
# Запускаем цикл из n * n повторений, исходя из максимально возможного количества ходов.
# create_map  - Прорисовываем карту поля и создаем список возможных ходов, в виде строк , формата 'X-Y'.
# По мере выполнения ходов, элементы списка будут заменяться на обозначения игроков, 'user', 'comp'
# calc_first_step  - Определяем , кто делает первый ход
# next_step_user - Запускаем функцию расчета координат хода игрока
# next_step_comp - функцмя рассчета координат хода  компьютера.
# Обе функции возвращают координаты хода, проверенные на корректность
# check_win_lose - Запускается анализатор позиций на поле , проверка на выигрыш ,
# проигрыш, а также на предвыигрыш и предпроигрыш, т.е. когда для окончания игры нужен 1 ход.
# Анализатор возвращает либо флаг досрочного окончания игры , либо координаты очередного хода компьютера,
# для выигрыша или предотвращения проигрыша.
# check_last_step  - декоратор проверки корректности введенных координат.


def win_lose_count(str_,flag, type_):
    # Получает на входе строку из 3х позиций, сформированную в  check_win_lose
    # и проверяет наличие условий для досрочного окончания игры по выигрышу или проигрышу ,
 # а также строки с двумя ходами одного игрока и одной свободной клеткой, с учетом, чей следующий ход.
    #print(f"{__LINE__}: {type_}, str_ = {str_}")
    if str_.count('user') == 3:
        return True,'Игра окончена. Победа игрока','text'
    elif str_.count('comp') == 3:
        return True,'Игра окончена. Победа компьютера','text'
    elif str_.count('comp') == 2 and str_.count('user') == 0:
        if flag: # проверяем , чей ход.
            return False, '',''
        else:

            # Предвыигрышная позиция компьютера
            x_y = [i1 for i1 in str_ if '-' in i1][0]
            return False, x_y, 'win'

    elif str_.count('user') == 2 and str_.count('comp') == 0:
        if flag:

            return False, '',''
        else:

            # определяем x,y для предотвращения проигрыша

            x_y = [i1 for i1 in str_ if '-' in i1][0]


            return False, x_y, 'lose'

    else:
        #print(f"{__LINE__}: ")
        return False,'',''


def check_win_lose(flag): # Проверка поля на условия окончания игры и на предвыигрышные и предпроигрышные позиции.
    d ={}
    s = steps_.split(',')
    res1_total, res2_total, res3_total = False, [], []

    for i in range(n): #steps_.split():

        row_ = [s[j] for j in range (i * n , i * n + n )] # формируем строку для анализа

        res1, res2, res3 = win_lose_count(row_,flag,'row') # проверяем 3 или 2 + свободная по строкам
        res1_total = res1_total or res1

        if res2:
            res2_total.append(res2)
            res3_total.append(res3)

        col_ = [s[j] for j in range(i, n * n, n)]  # формируем столбец для анализа
        res1, res2, res3 = win_lose_count(col_,flag, 'col') # проверяем 3 или 2 + свободная по столбцам
        res1_total = res1_total or res1

        if res2:
            res2_total.append(res2)
            res3_total.append(res3)


    dia_  = [s[j] for j in range(0, n**2, n + 1)] # формируем 1 диагональ для анализа

    res1, res2, res3 = win_lose_count(dia_,flag, 'dia1')  # проверяем 3 или 2 + свободная по диагонали, слева направо.
    res1_total = res1_total or res1

    if res2:
        res2_total.append(res2)
        res3_total.append(res3)

    dia_ = [s[j] for j in range(2, n * 2 + 1, n - 1)] # формируем  2 диагональ для анализа

    res1, res2, res3 = win_lose_count(dia_,flag, 'dia2')  # проверяем 3 или 2 + свободная по диагонали, слева направо.
    res1_total = res1_total or res1

    if res2:
        res2_total.append(res2)
        res3_total.append(res3)


    if 'win' in res3_total:
        index_ = res3_total.index('win')
        res2_total = res2_total[index_]
    elif 'lose' in res3_total:
        index_ = res3_total.index('lose')
        res2_total = res2_total[index_]

    return res1_total, res2_total


def check_last_step(func): # декоратор проверки правильности введенных координат
                           # на предмет непересечения с уже сделанными ходами
    def wrapper(step_,res2):
        while True:
            x,y = func(step_,res2)
            if str(x) + '-' + str(y) in steps_:

               break

            else:

                print(f" Некорректные координаты, сделайте ход заново")
        return x, y
    return wrapper


def create_map(n): # Первоначальное создание карты поля без ходов и списка возможных координат ходов.
    global map_, steps_
    map_ = [['-' for i in range(0,n + 1)] for j in range(0, n + 1)]
    map_[0][0] = '*'

    for i in range(1,n + 1):

        map_[0][i] = i
        map_[i][0] = i
    for i in range(n + 1):
        print(*map_[i])
    steps_ = ''
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            steps_ += str(i) + '-' + str(j) + ','
    steps_ = steps_[:-1]

    return map_, steps_

def update_map(map_,x,y,flag): # обновление карты поля.
    global steps_

    map_[x][y] = sign_0 if flag else sign_1
    for i in range(0,n + 1):
        print(*map_[i])
    a = str(x) + '-' + str(y)
    b = 'comp' if flag else 'user'

    s = steps_.replace(f"{a}", b)
    steps_ = s
    return True

def calc_first_step(): #  определяем, кто первый ходит.
    # 0 - компьютер, 1 - игрок
     if random.randint(0, 1):
         #print("Первый ходит игрок")
         num_gamer = 1
     else:
         #print("Первый ходит компьютер")
         num_gamer = 0
     return num_gamer



@check_last_step # проверка координат на непересечение с уже сделанными ходами.
def next_step_user(step_,res2): #ход игрока


    while True:
        a = input(f"     Введите координаты клетки , два числа XY, X - по вертикали Y - по горизонтали:")

        m = re.match(r'(\d{1})\W?(\d{1})$', a) # проверка на наличие 2х цифр, без разделителя или с разделителем
        if  not m:
            print("     Вы ввели неправильные координаты, повторите ввод")
        else:
            break

    x = int(m.group(1))
    y = int(m.group(2))

    return x, y

@check_last_step # проверка координат на непересечение с уже сделанными ходами.
# введена для симметрии с декорированием функции ввода игроком.
def next_step_comp(step_, res2): # ход компьютера
    global win_strategy_flag

    if res2: # закрываем две клетки противника, на одной линии, для избежания проигрыша.

        x,y =  int(res2[0]), int(res2[2])

        return x,y

    if '2-2' in steps_: # если свободна центральная клетка, ставим в нее
        x, y = 2, 2

    elif step_ == 2 : # если центр занят, ставим на левый угол
        x, y = 1, 3

    elif step_ == 3 :

        x_last = step_list[len(step_list) - 1][0]
        y_last = step_list[len(step_list) - 1][1]

        s1 = steps_.split(',')
        s = [s1[i] for i in range(1, n**2, 2)] # множество клеток - вершины креста.
        # если на втором ходе user поставил на одну из этих клеток, компьютер идет по выигрышному алгоритму

        if 'user' in s:

            if x_last in (1,n):
                x, y = x_last, y_last - 1
            else:
                x, y = x_last - 1, y_last

            win_strategy_flag = True

        else: # идем на ничью

            x, y =abs(n + 1 - y_last), abs(n + 1 - x_last)

    else:

        if win_strategy_flag:
            # предпоследний ход

            y_minus2 = step_list[len(step_list) - 2][1] #- координата предпоследнего хода
            x, y = n - 1, y_minus2
        else:
            index_ = steps_.find('-')
            x = int(steps_[index_ - 1:index_])
            y = int(steps_[index_ + 1:index_ + 2])

    return x,y


def main_func():
    global step_list
    global sign_0, sign_1,map_
    sign_0 = '0' #- знак для ходов компьютера
    sign_1 = 'X' #- знак для ходов  игрока

    map_, steps_ = create_map(n) # начальная прорисовка поля и заполение списка возможных ходов
    next_step_flag = calc_first_step() # определяем , кто первый ходит,
                                       # возможные значения 0 - ход компьютера, 1 - игрока

    step_list =[] # список сделанных ходов

    for step_ in range(1, n**2 + 1): # делаем n * n шагов, если не будет досрочного окончания игры
        res1, res2 = check_win_lose(next_step_flag) # проверка наличия выигрышной ,
        # проигрышной , предвыигрышной и предпроигрышной позиции

        if res1: # флаг досрочного окончания игры
            print(f"{res2[0]}")

            return res2
        if next_step_flag: # флаг - кто следующий ходит
            print(f"     Ход игрока")
            x,y = next_step_user(step_,res2) # ход игрока

            step_list.append([x,y,'user']) # добавляем ход в список сделанных ходов
            next_step_flag = 0 # флаг - следующим ходит компьютер
        else:

            x,y = next_step_comp(step_,res2) # рассчет хода компьютера
            print(f"      Ход компьютера: ({x} {y})")
            time.sleep(1)

            step_list.append([x, y, 'comp'])
            next_step_flag = 1  # флаг - следующим ходит игрок

        update_map(map_,x,y,next_step_flag) # обновляем рисунок поля, с учетом сделанного хода
    print(f"     Игра окончена. Ниичья")
    return True



if __name__ == "__main__":

    main_func()







