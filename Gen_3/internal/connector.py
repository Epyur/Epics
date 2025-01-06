from Gen_3.internal.xlsx import *
from Gen_3.internal.xls import *


inc_df_merged = inc_df.merge(ekn_df, how='left', on=["ekn"])
inc_df_merged_2 = inc_df_merged.merge(cust_df, how='left', on=['cust_mail']).set_index("ID")

inc_list_ = inc_df_merged_2.columns.tolist()
# print(inc_list_)


inc_df_merged_comb = inc_df_merged_2.merge(combustion(), how='left', on=["ID"])
inc_df_merged_comb_flam = inc_df_merged_comb.merge(flamability(), how='left', on=["ID"]).set_index("ID")

