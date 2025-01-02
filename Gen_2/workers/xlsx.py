import openpyxl
from Gen_2.excel.routes import bb
import pandas as pd

#читаем целевой файл
base_book = openpyxl.open(bb)
sheet_base = base_book['Sheet']

#определяем строку, в которой нет информации и формируем список ID внесенных в таблицу
def empty_row():
    row_list = []
    index_list = []
    for row in sheet_base['A{}:A{}'.format(sheet_base.min_row, sheet_base.max_row)]:
        for cell in row:
            if cell.value is not None:
                row_list.append(cell.value)
                row_count = len(row_list)
                break
    return (row_count + 1)

# Create a list to store the values
id_list = []

def ids ():    # Iterate through columns
    global id_list
    # Iterate through columns
    for column in sheet_base.iter_cols():
        # Iterate over the cells in the column
        for i, cell in enumerate(column):
            if i == 0:
                continue
            if cell.value is not None:
            # Add the value of the cell to the list
                id_list.append(cell.value)
        return id_list

ids()

df = pd.read_excel(bb)
df.index.name = "№ заявки"