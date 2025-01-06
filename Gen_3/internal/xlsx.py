from Gen_3.excel.routes import bb, ekn_book
import pandas as pd
import numpy as np

ekn_df_start = pd.read_excel(ekn_book)
ekn_df_columns = ekn_df_start.columns.tolist()
ekn_df = ekn_df_start.rename(columns={'ID (EKH)': 'ekn', 'code': 'type_of_product', 'Семейство': 'family', 'Название': "product_name", 'Толщина, мм': 'thickness', 'Цвет': "color", 'Группа горючести': 'comb_group', 'Группа воспламеняемости': 'flam_group', 'Группа РП': 'prop_group', 'КИ': 'oxy_index', 'СТО': 'sto', 'Производитель': 'producer', 'full discr': 'full_descr', 'shot discr (вносится в протокол)': 'description'})
ekn_df['thickness_ch'] = np.nan
ekn_df_columns_new = ekn_df.columns.tolist()
