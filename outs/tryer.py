from cheker import *


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


def base_saver1(frst_column):
    for i in inc_data1(0):
        for c in range(0, len(i)):
            for n in range(0, len(new_writes())):
                sheet_base.cell(row=er+n, column=c + frst_column).value = i[c]
                bs = base_book.save(ba_f)
                continue
    return bs


for i in inc_data1(0):
    print(i)
print("j")
base_saver1(1)