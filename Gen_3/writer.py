from collections.abc import dict_keys

import pandas as pd

from Gen_3.internal.connector import *


# def base_saver(data, header, aim_file):
#
#     df = pd.DataFrame(data=data, columns=header)
#     df = df.map(lambda v: v.replace('], [', ']\n [') if isinstance(v, str) else v)
#     for r in dataframe_to_rows(df, index=False, header=False):
#         sheet_base.append(r)
#     bs = base_book.save(aim_file)
#     return bs
#
# if id_list != inc_id_list:
#     base_saver(inc_dict_list,inc_title_inf, bb)
#     print('Data were added to base')
# else:
#     print('There are no another data, yet')

count_row = row_count
count_column = 0

for dct in inc_dict:
    count_row += 1
    for i in dct:
        count_column += 1
        val = inc_dict[i]
        dict_keys = dct.keys()
        sheet_base.cell(count_row, count_column).value = val

    base_book.save(bb)

print(row_count)
for i in inc_dict:
    print(i.keys())