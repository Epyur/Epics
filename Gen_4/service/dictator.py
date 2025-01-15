from functools import reduce
import numpy as np
import pandas as pd
from collections.abc import MutableMapping
from Gen_4.service.routes import in_title, comb_book


# Формируем переводной словарь для входящих названий
def start_rename():
    df_start = pd.read_excel(in_title)
    df = df_start.set_index('key')
    series_1 = df['val']
    title_dict = series_1.to_dict()
    return title_dict

# формируем словарь из датафрейм с переименованием ключей на основании переводного словаря
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
         string_dict = False
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

# выбираем из общего словаря пары ключ - значение, над которыми необходимо провести действия
def selection(dict1, val_list):
    list1 = {}
    list2 = val_list
    for i in dict1:
        if i in list2:
            list1.update({i: dict1[i]})
    return list1

# то-же что и selection но словари отбираем в список
def selection2(dict1, val_list):
    list1 = []
    list2 = val_list
    for i in dict1:
        if i in list2:
            list1.append(dict1[i])
    return list1

#  сортируем словари по ключам вложенных словарей/ выводит словарь вида {3: ['Нет'], 2: ['Нет'], 1: ['Нет']}
#  где цифра это ключ вложенного словаря, список это значение вложенного словаря
def sorter(dict1, val_list):
    list1 = selection2(dict1, val_list)
    s = {k: [list1[j][k] for j in range(len(list1))] for k in list1[0].keys()}
    return s

def average_exp(dict1, val_list, name):
    s = sorter(dict1, val_list)
    D = {}
    for i in s:
        mean_i = sum(s[i])/len(s[i])
        D.update({i: mean_i})
    dx ={name: D}
    df = dict1 | dx
    return df

def average_gen(dict1, val_list, name):
    s = selection2(dict1, val_list)
    s1 = s[0]
    d = sum(s1.values()) / len(s1)
    x = round(d, 2)
    dx = {name: x}
    df = dict1|dx
    return df

def differences(dict1, val_list, name):
    s = sorter(dict1, val_list)
    dict2 = {}
    for i in s:
       dif =  100 - s[i][1] * 100 / s[i][0]
       x = round(dif, 2)
       dict2.update({i: x})
    dx = {name: dict2}
    df = dict1|dx
    return df

def search_value(dict1, val_list, name, target_value, aim_value, alternate_value):
    s = sorter(dict1, val_list)
    for i in s:
        val = s[i]
        if target_value == val:
            dx = {name: aim_value}
        else:
            dx = {name: alternate_value}
    df = dict1|dx
    return df
# make dict flat again
def flatten_dict(dict1):
    dic = pd.json_normalize(dict1, sep='_')
    d_flat = dic.to_dict(orient='records')[0]
    return d_flat


def flatten_simple(dict1, val_list):
    d = {}
    for i in dict1:
        for c in val_list:
            if i == c:
                in_d = dict1[i]
                for x in in_d:
                    val = in_d[x]
                    d.update({c: val})
    return d