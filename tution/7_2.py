
import os.path


class Product:

    def __init__(self, name, weight, category):
        self.name = str(name)
        self.weight = float(weight)
        self.category = str(category)

    def __str__(self):
        return f'{self.name}, {self.weight}, {self.category}'


class Shop:
    __file_name = '7_2/product.txt'

    def get_products(self):
        if os.path.isfile(self.__file_name):
            file = open(self.__file_name, 'r', encoding='utf-8')
            products = file.read()
        else:
            file = open(self.__file_name, 'x', encoding='utf-8')
        file.close()
        return products



    def add(self, *products):
        file = open(self.__file_name, 'a', encoding='utf-8')
        for product in products:
            if product.name in self.get_products():
                print(f'Продукт {product.name} уже есть в магазине')
            else:
                file.write(product.__str__() + '\n')
        file.close()

s1 = Shop()

p1 = Product('Potato', 50.5, 'Vegetables')

p2 = Product('Spaghetti', 3.4, 'Groceries')

p3 = Product('Potato', 5.5, 'Vegetables')



print(p2) # __str__



s1.add(p1, p2, p3)



print(s1.get_products())