
def what_to_wear(temperature, isRain):
    if 20 < temperature < 30:
        if isRain == 'true':
            print(f" i = {i}, j = {j}, result = Футболку,шорты,дождевик")
        elif isRain == 'false':
            print(f" i = {i}, j = {j}, result = Футболку и шорты")
    elif 0 < temperature <= 20:

        if isRain == 'false':
            print(f" i = {i}, j = {j}, result = Пальто")
        elif isRain == 'strong':

            print(f" i = {i}, j = {j}, result = Пальто, резиновые сапоги и зонт")
        else:
            print(f" i = {i}, j = {j}, result = Пальто и дождевик")
    elif  temperature <= 0:
        print(f" i = {i}, j = {j}, result = Пуховик")

temperature = [-1, 0, 10, 20, 25, 30]
isRain = ['strong', 'true', 'false']

for i in temperature:
    for j in isRain:
        what_to_wear(i,j)
