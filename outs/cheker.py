from aim_book import *
from inc_files import *
from time import sleep

# формируем список данных входящей заявки, отсутствующих в архиве
inc_row = []
def inc_data():
    global inc_row
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

# формируем функцию записи данных в строку таблицы
def base_saver(a) -> object:
    for c in range(0, len(shs)):
        sheet_base.cell(row=er, column=c + a).value = shs[c]
        bs = base_book.save('БИ4.xlsx')
    return bs


# перепроверяем наличие новых данных и записываем
while int(len(new_writes()) > 0):
    base_saver(1)
else:
    print('Перенос данных завершен')





