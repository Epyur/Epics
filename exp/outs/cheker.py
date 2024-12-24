from aim_book import *
from inc_files import *

# формируем список данных входящей заявки, отсутствующих в архиве
def inc_data():
    inc_row = []
    for ii in range(rb_inc.nrows):  # в цикле по количеству всех строк
        data = rb_inc.cell_value(ii, 0)  # получаем значение ячейки (ii-строка, 0-столбец)
        if str(new_id()) == str(data):  # сравниваем заданное значение с полученным, если истина
            for i in range(rb_inc.ncols):  # в цикле по количеству столбцов
                a = rb_inc.cell_value(ii, i)
                inc_row.append(a)
    return inc_row

inc_data_list = inc_data() # легализуем результат работы функции в качестве списка

er = int(empty_row())
shs = inc_data()

# записываем данные в строку таблицы
for c in range(0, len(shs)):
    sheet_base.cell(row=er, column=c + 1).value = shs[c]
    base_book.save('../БИ4.xlsx')

print(new_id())

