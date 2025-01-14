import numpy as np
import pandas as pd
from Gen_4.service.routes import in_title, comb_book


# Формируем переводной словарь для входящих названий
def start_rename():
    df_start = pd.read_excel(in_title)
    df = df_start.set_index('key')
    series_1 = df['val']
    title_dict = series_1.to_dict()
    return title_dict

def dict_creator(file, index1, val):
    title_dict = start_rename()
    df_start = pd.read_excel(file)
    df_columns = df_start.columns.tolist()
    titles = list(title_dict)

    for key_s in titles:
        if key_s not in df_columns:
            title_dict.pop(key_s)

    df = df_start.rename(columns=title_dict)

    df_index = df.set_index(index1)
    if val in df_index.index:
        string = df_index.loc[val].copy()
        string_dict = string.to_dict()
        # print(ekn_string_dict)
    else:
         print(f'Указанное значение {index1} отсутствует в базе данных')
         string_dict = {}
    return string_dict

# объединение словарей: замена значений в первом словаре только если поле пустое, в противном случае значение из второго словаря стирается. Нужно быть внимательным при выборе порядка словарей.
# + при необходимости можно добавить префикс к названию ключей в объединяемых словарях
def dict_unition(dict1, dict2, prefix1=False, prefix2=False):
    list_dict1 = []
    list_key = []
    # ищем совпадающие ключи в соединяемых словарях, составляем два списка
    for key_a in dict1:
        for key_b in dict2:
            if key_a == key_b:
                if dict1.get(key_a) is np.nan:
                    list_dict1.append(key_a)
                if dict1.get(key_a) is not np.nan:
                    list_key.append(key_b)
                    #print(list_key)
                else:
                    pass

    # удаляем совпадающие записи и переносим в первый список записи, отсутствующие в нем, затем удаляем повторяющиеся записи из второго словаря
    if len(list_key) > 0:
        for i in list_key:
            dict2.pop(i)
    if len(list_dict1) > 0:
        for x in list_dict1:
            val = dict2.get(x)
            dict1 = dict1 | {x: val}
            dict2.pop(x)
            #print(val)

    for key_c in dict1:
        if prefix1 is not False:
                if key_c not in list_dict1:
                    dict1[str(prefix1) + '_'+ key_c] = dict1.pop(key_c)
    for key_d in dict2:
        if prefix2 is not False:
            if key_d not in list_dict1:
                dict2[str(prefix2) + '_' + key_d] = dict2.pop(key_d)
    d = dict1 | dict2
    return d

# def dict_sorting(dict1):
#     key_list_1 = []
#     key_list_2 = []
#     val_list = []
#     for i in dict1:
#         key_list_1.append(i)
#         internal_dict = dict1.get(i)
#         for x in internal_dict:
#             key_list_2.append(x)
#             val = internal_dict.get(x)
#             val_list.append(val)
#     internal_dict = dict(zip(key_list_1, val_list))
#     sorted_dict = dict(zip(key_list_2, internal_dict))
#     return sorted_dict

def experiment(dict1):
    list1 = []
    list2 = ['len_1', 'len_2', 'len_3', 'len_4']
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    for i in dict1:
        if i in list2:
            list1.append(dict1.get(i))



    print(list1)

