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

h1 = House('ЖК "Болото"',  38)
h2 = House('ЖК "Сухие поля"', 9)

print(h1)
print(h2)
print(len(h1))
print(len(h2))
