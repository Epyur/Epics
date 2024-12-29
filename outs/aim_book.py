import openpyxl
from inc_files import *
from tempfile import NamedTemporaryFile

ba_f = 'БИ4.xlsx'

#читаем целевой файл
base_book = openpyxl.open(ba_f)

sheet_base = base_book['Sheet']


id_list = []
#определяем строку, в которой нет информации и формируем список ID внесенных в таблицу
def empty_row():
    global id_list
    row_list = []
    index_list = []
    for row in sheet_base['A{}:A{}'.format(sheet_base.min_row, sheet_base.max_row)]:
        for cell in row:
            if cell.value is not None:
                row_list.append(cell.value)
                row_count = len(row_list)
                index_list.append(str(cell.value))
                id_list = index_list[1:]
            break
    return (row_count + 1)


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


def check_repeater():
    print('Пустой ряд:', empty_row())
    print('Список id содержащихся в архиве:', id_list)
    print('Список id содержащихся в хранилище заявок:', inc_id_list)
    print('Список id отсутствующих в архиве:', new_writes())
    print('Первый отсутствующий ID в архиве:', new_id())


