import openpyxl
from inc_file import *


#читаем целевой файл
base_book = openpyxl.open('../../excel/БИ3.1.xlsx')
sheet_inc = base_book['INc']

#индексируем листы в книге
def sheet_inf():
    sheet_count = -1
    sheet_index = []
    for i in base_book:
        sheet_count += 1
        sheet_index.append(sheet_count)
        sheet_dict = dict(zip(sheet_index, base_book.sheetnames))
    return(sheet_dict)
#print(sheet_inf())

#индексируем столбцы
def row_inf():
    global sheet_inc
    t_index = sheet_inc['2']
    frst_row = []
    for cell in t_index:
        frst_row.append(cell.value)
        titles = dict(zip(t_index, frst_row))
    return (titles)
#print(row_inf())

sheet_inf()
row_inf()
id_list = []
#определяем строку, в которой нет информации и формируем список ID внесенных в таблицу
def empty_row():
    global id_list
    row_list = []
    index_list = []
    for row in sheet_inc['A{}:A{}'.format(sheet_inc.min_row, sheet_inc.max_row)]:
        for cell in row:
            if cell.value is not None:
                row_list.append(cell.value)
                row_count = len(row_list)
                index_list.append(str(cell.value))
                id_list = index_list[2:]
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
        a = 'Новые записи отсутствуют'
    return(a)

print('Пустой ряд:', empty_row())
print('Список id содержащихся в архиве:', id_list)
print('Список id содержащихся в хранилище заявок:', inc_id_list)
print('Список id отсутствующих в архиве:', new_writes())
print('Первый отсутствующий ID в архиве', new_id())


