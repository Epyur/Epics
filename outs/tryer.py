from cheker import *
from time import sleep
inc_rowe = []
inc_rows = []
def inc_data1(id_col):
    global inc_rowe
    global inc_rows
    for i in range(rb_inc.ncols):  # в цикле по количеству столбцов
        inc_rows.append[i]
        for ii in range(rb_inc.nrows):  # в цикле по количеству всех строк
            data = rb_inc.cell_value(ii, id_col)  # получаем значение ячейки (ii-строка, 0-столбец)
            if str(data) in str(new_writes()):  # сравниваем заданное значение с полученным, если истина
                a = rb_inc.cell_value(ii, i)
                inc_rowe.append(a)

    return inc_rows


def base_saver1(a):
    while len(new_writes()) > 0:
        for c in range(0, len(shs)):
            sheet_base.cell(row=er, column=c + a).value = shs[c]

    bs = base_book.save('БИ4.xlsx')
    return bs

print('twt', inc_data1(0))
print(rb_inc.nrows)