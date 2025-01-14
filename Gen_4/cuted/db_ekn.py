from .dictator import dict_creator
from .index_page import index_ekn
from .routes import *

# def ekn_search(ekn):
#     ekn_df_start = pd.read_excel(ekn_book)
#     ekn_df_columns = ekn_df_start.columns.tolist()
#     ekn_df = ekn_df_start.rename(
#         columns={'ID (EKH)': 'ekn', 'code': 'type_of_product', 'Семейство': 'family', 'Название': "product_name",
#                  'Толщина, мм': 'thickness', 'Цвет': "color", 'Группа горючести': 'comb_group',
#                  'Группа воспламеняемости': 'flam_group', 'Группа РП': 'prop_group', 'КИ': 'oxy_index', 'СТО': 'sto',
#                  'Производитель': 'producer', 'full discr': 'full_descr',
#                  'shot discr (вносится в протокол)': 'description'})
#     ekn_df_1 = ekn_df.set_index('ekn')
#     if ekn in ekn_df_1.index:
#         ekn_string = ekn_df_1.loc[ekn].copy()
#         ekn_string_dict = ekn_string.to_dict()
#         #print(ekn_string_dict)
#     else:
#         print('Сведения о материале с ЕКН указанным в заявке отсутствует')
#         ekn_string_dict = {}
#     return ekn_string_dict


