from Gen_2.workers.xls import *
import math
# Разбираем результаты испытаний на горючесть
# разбираем книгу результатов
c_book = open_file(comb_book, 0) # open the book of measures
c_title_row = c_book.row_values(rowx=0) # form title row names
c_id_column = c_book.col_values(colx=2) # form list of incoming request id
c_ser_number = c_book.col_values(colx=24) # form list of research number


    # формируем библиотеку титулов
def title_dict(title):
    col_index = []
    count_ = -1
    for i in c_title_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, title))  # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

c_title_inf_dict = title_dict(c_title_row)

# Формируем список входящих идентификаторов
def c_id_list():
    c_id_list = []
    c_id = c_id_column[0:]
    for i in c_id:
        c_id_list.append(i)  # список входящих идентификаторов
    return c_id_list