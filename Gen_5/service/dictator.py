from functools import reduce
import numpy as np
import pandas as pd
from collections.abc import MutableMapping

from Gen_5.methods.indicators import group
from Gen_5.service.routes import in_title, out_names

# Формируем переводной словарь для входящих названий
def start_rename():
    df_start = pd.read_excel(in_title)
    df = df_start.set_index('key')
    series_1 = df['val']
    title_dict = series_1.to_dict()
    return title_dict

# формируем словарь из датафрейм с переименованием ключей на основании переводного словаря
def dict_creator(file, index1, val, deleted=None):  #deleted заполнять списком
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
        if deleted is not None:
            for key_x in deleted:
                string_dict.pop(key_x)
    else:
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

    d2 = dict2.copy()
    for key_c in dict1:
        if prefix1 is not False:
            if key_c not in list_dict1:
                dict1[str(prefix1) + '_'+ key_c] = dict1.pop(key_c)
    for key_d in dict2:
        if prefix2 is not False:
            if key_d not in list_dict1:
                d2[str(prefix2) + '_' + key_d] = d2.pop(key_d)
    d = dict1 | d2
    return d

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

def average_exp(dict1, val_list, name, aim_ind, dict2=None, func=None, func2 = None, name2 = None, name3=None, group_dict=None):
    s = sorter(dict1, val_list)
    D = {}
    D2 = {}
    D3 = {}
    for i in s:
        krit = sum(s[i])/len(s[i])
        D.update({i: krit})
        if func is not None:
            real_indicator = func(krit)
            D2.update({i: real_indicator})
            if func2 is not None:
                compair = func2(dict2, aim_ind, real_indicator, group_dict)
                D3.update({i: compair})
        else:
            pass
    dx ={name: D}
    if func is not None:
        dx1 = {name2: D2}
    if func2 is not None:
        dx2 = {name3: D3}
    df = dict1 | dx
    if func is not None:
        df = df|dx1
    if func2 is not None:
        df = df|dx2
    return df

def average_gen(dict1, val_list, name, aim_ind, dict2=None, func=None, func2 = None, name2 = None, name3=None, group_dict=None):
    s = selection2(dict1, val_list)
    s1 = s[0]
    d = sum(s1.values()) / len(s1)
    krit = round(d, 2)
    dx = {name: krit}
    if func is not None:
        real_indicator = func(krit)
        dx1 = {name2: real_indicator}
        if func2 is not None:
            compair = func2(dict2, aim_ind, real_indicator, group_dict)
            dx2 = {name3: compair}
        else:
            pass
    df = dict1 | dx
    if func is not None:
        df = df|dx1
    if func2 is not None:
        df = df|dx2
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
        krit = s[i]
        if target_value == krit:
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

def estimation(dict1, val_list, name, aim_ind, dict2=None, func=None, func2 = None, name2 = None, group_dict=None): # классификация и оценка соответствия без проведения математических операций
    d1 = {}
    d2 = {}
    d3 = {}
    for i in dict1[val_list]:
        krit = dict1[val_list][i]
        if func is not None:
            real_indicator = func(krit)
            d1.update({i: real_indicator})
            d2.update({name: d1})
            if func2 is not None:
                compair = func2(dict2, aim_ind, real_indicator, group_dict)
                d3.update({i: compair})
                d2.update({name2: d3})
            else:
                pass
        else:
            pass
    df = dict1
    if func is not None:
        df = dict1 | d2
    return df

def estimation_lite(dict1, val_list, name, aim_ind, dict2=None, func=None, func2 = None, name2 = None, group_dict=None): # классификация и оценка соответствия без проведения математических операций
    krit = dict1[val_list]
    if func is not None:
        real_indicator = func(krit)
        d1 = {name: real_indicator}
        if func2 is not None:
            compair = func2(dict2, aim_ind, real_indicator, group_dict)
            d2 = {name2: compair}
        else:
            pass
    else:
        pass
    df = dict1
    if func is not None:
        df = dict1 | d1
    if func2 is not None:
        df = df|d2
    return df

# получение значения целевого индикатора (значения словаря 1 уровня)
def aim_indicator(dict1, aim_ind):
    p = dict1[aim_ind]
    return p


def compare_lite(dict1, val_list, name, aim_ind, dict2=None, dict3=None, func=None, name2 = None, group_dict=None):
    dx = dict1
    list1 = []
    for i in val_list:
        indicators = dict1[i]
        list1.append(dict2[indicators])
        min_key = min(list1)
        d2 = {v: k for k, v in dict2.items()}
        real_indicator = d2[min_key]
        dx1 = {name: real_indicator}
        comp = func(dict3, aim_ind, real_indicator, group_dict)
        dx2 = {name2: comp}
        dx = dx|dx1
        dx = dx|dx2
    return dx

def final_rename(dict1):
    df_start = pd.read_excel(out_names)
    df = df_start.set_index('key')
    series_1 = df['val']
    title_dict = series_1.to_dict()
    d = dict1.copy()
    d1 = {}
    for key_c in dict1:
        for key_x in title_dict:
            if key_c == key_x:
                v = title_dict[key_x]
                d[v] = d.pop(key_c)
    for key_v in title_dict:
        v1 = title_dict[key_v]
        d1.update({v1: '-//-'}) # собираем пустой словарь с сортированными ключами
    d = d1 | d
    return d

def exp_counter(dict1, val_list):
    list1 = []
    for i in dict1[val_list]:
        if i is False:
            counter = 1
        else:
            list1.append(i)
            counter = len(list1)
    return counter

def sorter_2(dict1, val_list1, val_list2):
    list1 = []
    for a in dict1[val_list1]:
        for b in dict1[val_list2]:
            if a == b and dict1[val_list2][b] == 'Да':
                list1.append(dict1[val_list1][a])
        try:
            list2 = min(list1)
        except:
            list2 = list1
    return list2

def deleter(dict1, val):
    for i in dict1:
        j = dict1[i]
        for c in j:
            if c != val:
                j.pop(c)
    return dict1