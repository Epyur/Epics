import pandas as pd
from Gen_2.workers.comunication import *
from Gen_2.workers.xlsx import *

def base_saver(data, header, aim_file):
    df = pd.DataFrame(data=data, columns=header)
    df = df.map(lambda v: v.replace('], [', ']\n [') if isinstance(v, str) else v)

    for r in dataframe_to_rows(df, index=False, header=False):
        sheet_base.append(r)

    bs = base_book.save(aim_file)
    return bs

if id_list != inc_id_list:
    base_saver(inc_rows,rb_inc_row, bb)
    print('Data were added to base')
else:
    print('There are no another data, yet')