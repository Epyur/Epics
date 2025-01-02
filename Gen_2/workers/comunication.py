from Gen_2.workers.xlsx import *
from Gen_2.workers.xls import *
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from Gen_2.workers.methods import *

inc_id_list = inc_id_list()
# Сравниваем имеющийся и входящий списки, выбираем новые записи
def new_writes():
    global id_list
    global inc_id_list
    new_writes = []
    for i in inc_id_list:
        if i not in id_list:
            new_writes.append(i)
    return new_writes


def new_id():
    list_1 = new_writes()
    if len(list_1) > 0:
        a = list_1[0]
    else:
        False
        a = 'Новые записи отсутствуют'
    return(a)

# формируем список данных входящей заявки, отсутствующих в архиве
inc_rowe = []
inc_rows = []
def inc_data1(id_col):
    global inc_rowe
    global inc_rows
    for ii in range(rb_inc.nrows):  # в цикле по количеству всех строк
        data = rb_inc.cell_value(ii, id_col)  # получаем значение ячейки (ii-строка, 0-столбец)
        if str(data) in str(new_writes()):  # сравниваем заданное значение с полученным, если истина
            for i in range(rb_inc.ncols):
                a = rb_inc.cell_value(ii, i)
                inc_rowe.append(a)
    inc_rows = [inc_rowe[i:i + len(rb_inc_row)] for i in range(0, len(inc_rowe), len(rb_inc_row))]
    return inc_rows
inc_data1(0)
empty_row = empty_row()

def check_repeater():
    print('Пустой ряд:', empty_row)
    print('Список id содержащихся в архиве:', id_list)
    print('Список id содержащихся в хранилище заявок:', inc_id_list)
    print('Список id отсутствующих в архиве:', new_writes())
    print('Первый отсутствующий ID в архиве:', new_id())

inc_dict = {}
inc_dict_list = []
def inc_bible(num):
    global inc_dict
    global inc_dict_list
    id_column = []
    count = num
    for i in inc_rows:
        for n in i:
            count += 1
            id_column.append(count)
            inc_dict = dict(zip(id_column, i))
        inc_dict_list.append(inc_dict)
    return inc_dict_list
inc_bible(-1)

gen_title_dict = {**inc_dict, **c_title_inf_dict_1, **c_title_inf_dict_2, **c_title_inf_dict_3}


# ------------------ Проверяем наличие записей результатов экспериментов -------------------------------
#if
