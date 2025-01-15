import pandas as pd

from .dictator import *
from .routes import *
import flatdict
from ..methods.comb import *


# получаем словарь входящей заявки
counter_x = 0

while counter_x <= 100:
    counter_x += 1
    x = int(input('Введите номер заявки: '))
    dict_0 = {'ID': x} # словарь ID
    print(dict_0)
    if x == 0:
        print("До свидания!")
        exit()
    else:
        dict_1 = dict_creator(inc_book, 'ID', x) # информация о входящей заявке
        # print(dict_1)
        # print(dict_1.get('ekn'))

        if dict_1 is False:
            print(f'ID {x} отсутствует в базе данных')
        else:
            if dict_1.get('ekn') is not np.nan:
                ekn = dict_1.get('ekn')
                # print(ekn)
                dict_2 = dict_creator(ekn_book, 'ekn', ekn) # получаем словарь информации о материале
                # print(dict_2)
            else:
                print('В заявке не указан ЕКН')
                choice1 = int(input("Выберите действие: \n1 - Продолжить без ЕКН\n2 - Ввести ЕКН\n"))
                if choice1 == 1:
                    pass
                if choice1 == 2:
                    ekn_new = int(input('Введите № ЕКН: '))
                    dict_1.update({'екн': ekn_new})
                    dict_2 = dict_creator(ekn_book, 'ekn', ekn)
                    # print(dict_2)
            dict_0_1 = dict_unition(dict_0, dict_1)
            # print(dict_0_1)
            dict_0_2 = dict_unition(dict_0_1, dict_2)
            print(dict_0_2)
            dict_3 = combustor(x)
            dict_0_3 = dict_unition(dict_0_2, dict_3)
            print(dict_0_3)





# из словаря заявки получаем номер Екн и если он заполнен, то получаем сведения о материале


    zf = pd.DataFrame(list(dict_0_3.items()))
    #
    ds = zf.to_excel('2.xlsx')