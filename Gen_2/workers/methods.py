from Gen_2.workers.xls import *
import math
import pandas as pd

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

c_df = pd.read_excel(comb_book)
c_df.index.name = '№ Записи заявки на испытания'
c_df_1 = c_df.iloc[:, 2]

