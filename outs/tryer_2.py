from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

from cheker import *
import pandas as pd

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
print(inc_rows)

df = pd.DataFrame(data=inc_rows, columns=rb_inc_row)
df = df.map(lambda v: v.replace(',', '\n') if isinstance(v, str) else v)

for r in dataframe_to_rows(df, index=False, header=False):
    sheet_base.append(r)

for row in sheet_base:
    for cell in row:
        cell.alignment = Alignment(wrapText=True)

base_book.save(ba_f)