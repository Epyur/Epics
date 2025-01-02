import openpyxl
from Gen_3.excel.routes import bb, ekn_book
import pandas as pd

# #читаем целевой файл
# base_book = openpyxl.open(bb)
# sheet_base = base_book['Sheet']
#
# id_list = []
#
# #определяем строку, в которой нет информации и формируем список ID внесенных в таблицу
# for row in sheet_base['A{}:A{}'.format(sheet_base.min_row, sheet_base.max_row)]:
#     for cell in row:
#         if cell.value is not None:
#             id_list.append(cell.value)
#             row_count = len(id_list)
#
# del id_list[0]

ekn_df_start = pd.read_excel(ekn_book)
ekn_df_columns = ekn_df_start.columns.tolist()
ekn_df = ekn_df_start.rename(columns={'ID (EKH)': 'ekn', 'code': 'type_of_product', 'Семейство': 'family', 'Название': "product_name", 'Толщина, мм': 'thickness', 'Цвет': "color", 'Группа горючести': 'comb_group', 'Группа воспламеняемости': 'flam_group', 'Группа РП': 'prop_group', 'КИ': 'oxy_index', 'СТО': 'sto', 'Производитель': 'producer', 'full discr': 'full_descr', 'shot discr (вносится в протокол)': 'description'})
ekn_df_columns_new = ekn_df.columns.tolist()
