import openpyxl
from Gen_3.excel.routes import bb

#читаем целевой файл
base_book = openpyxl.open(bb)
sheet_base = base_book['Sheet']

id_list = []

#определяем строку, в которой нет информации и формируем список ID внесенных в таблицу
for row in sheet_base['A{}:A{}'.format(sheet_base.min_row, sheet_base.max_row)]:
    for cell in row:
        if cell.value is not None:
            id_list.append(cell.value)
            row_count = len(id_list)

del id_list[0]

