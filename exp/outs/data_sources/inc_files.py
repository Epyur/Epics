import xlrd

# разбираем файл заявок
rb = xlrd.open_workbook('../../excel/inc.xls', formatting_info=True)
inc_sheet = rb.sheet_by_index(0)
inc_index_column = inc_sheet.col_values(colx=0)
inc_title_row = inc_sheet.row_values(rowx=0)
# считаем элементы в титульной строке
def inc_title_inf():
    col_index = []
    count_ = -1
    for i in inc_title_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, inc_title_row)) # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

# считываем колонку идентификаторов
def inc_row_inf():
    row_index = []
    count_row = -1
    for i in inc_index_column:
        count_row += 1
        row_index.append(count_row)
    inf_dict_row = dict(zip(row_index, inc_index_column)) # проверочный словарь, для сверки индексов и значений строк
    return inf_dict_row

# Формируем список входящих идентификаторов
def inc_id_list():
    inc_id_list = []
    inc_id = inc_index_column[1:]
    for i in inc_id:
        inc_id_list.append(i)  # список входящих идентификаторов
    return inc_id_list







