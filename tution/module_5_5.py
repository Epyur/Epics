

class House:

    houses_history = []

    def __new__(cls, *args, **kwargs):
        cls.houses_history.append(args[0])
        return object.__new__(cls)

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
        return f"Name of house: {self.name}, \nNumber of floors: {self.number_of_floors}"

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

    def __del__(self):
        print(f'{self.name} снесен, но он останется в истории')


h1 = House("Building Tall Tower", "26")
h2 = House('House #2', '9')
h3 = House('House #3', '14')

print(h1)
print(House.houses_history)
print(h2)
print(h3)
print(House.houses_history)

del h3
