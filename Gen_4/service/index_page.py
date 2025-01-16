import pandas as pd

from .dictator import *
from .routes import *
import flatdict
from ..methods.comb import *


# получаем словарь входящей заявки
counter_x = 0

while counter_x <= 100:
    counter_x += 1
    x = int(input('Введите номер заявки или 0, для завершения программы: '))
    dict_0 = {'ID': x} # словарь ID
    # print(dict_0)
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

            if dict_2 is False or dict_1['ekn'] == np.nan:
                print('В заявке не указан ЕКН или ЕКН указан не верно')
                ekn_new = int(input('Введите № ЕКН, либо введите 1 - НИОКР Техслужбы СБЕ; \n2 - НИОКР Завода ПИР; 3 - НИОКР завода ПВХ Мембран): '))
                dict_1.update({'екн': ekn_new})
                dict_2 = dict_creator(ekn_book, 'ekn', ekn_new)
                # print(dict_2)
            dict_united = dict_unition(dict_0, dict_1)
            # print(dict_0_1)

            dict_united = dict_unition(dict_united, dict_2)
            # print(dict_0_2)
            dict_3 = combustor(x) # точка входа в модуль comb.py
            if dict_3 is False:
                print(f'В базе данных испытаний по методу 2 ГОСТ 30244 запись с ID {x} отсутствует')
            else:
                dict_united = dict_unition(dict_united, dict_3) # точка выхода из модуля comb,py
            print(dict_united)





# из словаря заявки получаем номер Екн и если он заполнен, то получаем сведения о материале


            zf = pd.DataFrame(list(dict_united.items()))
            ds = zf.to_excel('2.xlsx')