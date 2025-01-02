import pandas as pd

from Gen_2.workers.comunication import inc_rows
from Gen_3.internal.connector import *


def base_saver():

    df = inc_df_merged_comb
    ds = df.to_excel(bb)
    return ds

base_saver()
print('Data were added to base')


# print(flam_df_columns)

