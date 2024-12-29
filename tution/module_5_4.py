class House:
    def __init__(self, name, number_of_floors):
        self.name = name
        self.number_of_floors = int(number_of_floors)



    def to_go(self):
        self.new_floor = int(input(f'Input floor number of {self.name} house:' ))
        if self.new_floor > self.number_of_floors or self.new_floor < 0:
            print('There are no such floor')
        else:
            for i in range(1, self.new_floor+1):
                print(i)

    def __str__(self):
        return f"Name of house {self.name}, number of floors {self.number_of_floors}"

    def __len__(self):
        return self.number_of_floors

    def __eq__(self, other):
        return self.number_of_floors == other.number_of_floors

    def __add__(self, other):
        return self.number_of_floors + other

    def __lt__(self, other):
        return self.number_of_floors < other.number_of_floors

    def __le__(self, other):
        return self.number_of_floors <= other.number_of_floors

    def __gt__(self, other):
        return self.number_of_floors > other.number_of_floors

    def __ge__(self, other):
        return self.number_of_floors >= other.number_of_floors

    def __ne__(self, other):
        return self.number_of_floors != other.number_of_floors


h1 = House('ЖК "Болото"',  38)
h2 = House('ЖК "Сухие поля"', 9)

print(h1)
print(h2)
print(len(h1))
print(len(h2))
print(h1 == h2)
h1 = h1 + 10
print(h1)
print(h1 < h2.number_of_floors) # почему-то здесь и ниже у other нужно пренудительно указать сравниваемый элемент, без этого формируется ошибка AttributeError: 'int' object has no attribute 'number_of_floors'
print(h1 <= h2.number_of_floors)
print(h1 > h2.number_of_floors) # без прямого указания на элемент формируется ошибка AttributeError: 'int' object has no attribute 'number_of_floors'
print(h1 >= h2.number_of_floors)
print(h1 != h2.number_of_floors)