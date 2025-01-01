from Gen_3.internal.xlsx import *
from Gen_3.internal.xls import *

# Формируем список идентификаторов новых входящих заявок
new_writes = []
if inc_id_list() != id_list:
    for i in inc_id_list():
        if i not in id_list:
            new_writes.append(i)
else:
    print('Информация о новых входящих заявках отсутствует')

# формируем список данных входящей заявки, отсутствующих в архиве
inc_rowe = []
inc_rows = []
def inc_data(id_col):
    global inc_rowe
    global inc_rows
    for ii in range(rb_inc.nrows):  # в цикле по количеству всех строк
        data = rb_inc.cell_value(ii, id_col)  # получаем значение ячейки (ii-строка, 0-столбец)
        if str(data) in str(new_writes):  # сравниваем заданное значение с полученным, если истина
            for i in range(rb_inc.ncols):
                a = rb_inc.cell_value(ii, i)
                inc_rowe.append(a)
    inc_rows = [inc_rowe[i:i + len(rb_inc_row)] for i in range(0, len(inc_rowe), len(rb_inc_row))]
    return inc_rows
inc_data(0)

inc_dict = []
for i in inc_rows:
    a = dict(zip(col_index, i))
    inc_dict.append(a)
