from exp.outs.data_sources.aim_book import *
from exp.outs.data_sources.inc_files import *

# формируем список данных входящей заявки, отсутствующих в архиве
def inc_data():
    inc_row = []
    for ii in range(inc_sheet.nrows):  # в цикле по количеству всех строк
        data = inc_sheet.cell_value(ii, 0)  # получаем значение ячейки (ii-строка, 0-столбец)
        if str(new_id()) == str(data):  # сравниваем заданное значение с полученным, если истина
            for i in range(inc_sheet.ncols):  # в цикле по количеству столбцов
                a = inc_sheet.cell_value(ii, i)
                inc_row.append(a)
    return inc_row

print(inc_title_row)
print(inc_data())