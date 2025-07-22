'''В проекте «Дом питомца» добавим новую услугу — электронный кошелек.
 Необходимо создать класс «Клиент», который будет содержать данные о клиентах
  и их финансовых операциях. О клиенте известна следующая информация: имя, фамилия, город, баланс.

Далее сделайте вывод о клиентах в консоль в формате:

«Иван Петров. Москва. Баланс: 50 руб.»'''



class Cat:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def get(self):
        return self.name, self.gender, self.age


class Customer:
    def __init__(self, name, surname, city, balanse = 0):
        self.name = name
        self.surname = surname
        self.city = city
        self.balanse = balanse

    def get_info(self):
        return f"{self.name} {self.surname}. {self.city}. "