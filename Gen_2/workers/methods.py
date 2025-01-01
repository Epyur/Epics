from Gen_2.workers.xls import *
import math
# Разбираем результаты испытаний на горючесть
# разбираем книгу результатов
c_book = open_file(comb_book, 0) # open the book of measures
c_title_row = c_book.row_values(rowx=0) # form title row names
c_id_column = c_book.col_values(colx=2) # form list of incoming request id
c_ser_number = c_book.col_values(colx=24) # form list of research number


    # формируем библиотеку титулов
def title_dict_1(title):
    col_index = []
    count_ = 25
    for i in c_title_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, title))  # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

c_title_inf_dict_1 = title_dict_1(c_title_row)


def title_dict_2(title):
    col_index = []
    count_ = 52
    for i in c_title_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, title))  # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

c_title_inf_dict_2 = title_dict_2(c_title_row)

def title_dict_3(title):
    col_index = []
    count_ = 79
    for i in c_title_row:
        count_ += 1
        col_index.append(count_)
    inf_dict_col = dict(zip(col_index, title))  # проверочный словарь, для сверки индексов и наименований столбцов
    return inf_dict_col

c_title_inf_dict_3 = title_dict_3(c_title_row)
c_title_dict = {**c_title_inf_dict_1, **c_title_inf_dict_2,**c_title_inf_dict_3}

# inc_dict = {}
# inc_dict_list = []
# def inc_bible(num):
#     global inc_dict
#     global inc_dict_list
#     id_column = []
#     count = num
#     for i in inc_rows:
#         for n in i:
#             count += 1
#             id_column.append(count)
#             inc_dict = dict(zip(id_column, i))
#         inc_dict_list.append(inc_dict)
#     return inc_dict_list
# inc_bible(-1)