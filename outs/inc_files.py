import xlrd

# функции разборки книги
def open_file(file, ind): # вызов файла xls и 1 листа в ней
    rb = xlrd.open_workbook(file, formatting_info=True)
    inc_sheet = rb.sheet_by_index(ind)
    return inc_sheet
rb_inc = open_file('excel/inc.xls', 0)

def chose_column(col): # вызов файла xls
    index_column = rb_inc.col_values(colx=col)
    return index_column

def chose_row(row): # вызов файла xls
    title_row = rb_inc.row_values(rowx=row)
    return title_row


# разбираем лист заявок
rb_inc_column = chose_column(0)
rb_inc_row = chose_row(0)

# считаем элементы в титульной строке
def inc_title_inf():
    col_index = []
    count_ = -1
    for i in rb_inc_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, rb_inc_row)) # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

# считываем колонку идентификаторов
def inc_row_inf():
    row_index = []
    count_row = -1
    for i in rb_inc_column:
        count_row += 1
        row_index.append(count_row)
    inf_dict_row = dict(zip(row_index, rb_inc_column)) # проверочный словарь, для сверки индексов и значений строк
    return inf_dict_row

# Формируем список входящих идентификаторов
def inc_id_list():
    inc_id_list = []
    inc_id = rb_inc_column[1:]
    for i in inc_id:
        inc_id_list.append(i)  # список входящих идентификаторов
    return inc_id_list







