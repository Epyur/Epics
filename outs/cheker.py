from aim_book import *
from inc_files import *
import sys
import os
print(check_repeater())
# формируем список данных входящей заявки, отсутствующих в архиве
inc_row = []
def inc_data(id_col):
    global inc_row
    for ii in range(rb_inc.nrows):  # в цикле по количеству всех строк
        data = rb_inc.cell_value(ii, id_col)  # получаем значение ячейки (ii-строка, 0-столбец)
        if str(new_id()) == str(data):  # сравниваем заданное значение с полученным, если истина
            for i in range(rb_inc.ncols):  # в цикле по количеству столбцов
                a = rb_inc.cell_value(ii, i)
                inc_row.append(a)
    return inc_row

er = int(empty_row())
shs = inc_data(0)

# формируем функцию записи данных в строку таблицы
def base_saver(a) -> object:
    for c in range(0, len(shs)):
        sheet_base.cell(row=er, column=c + a).value = shs[c]
        bs = base_book.save('БИ4.xlsx')
    return bs


# перепроверяем наличие новых данных и записываем






