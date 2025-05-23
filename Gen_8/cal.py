import pandas as pd

from Gen_8.service.tdtold import dataframe_tdt

data = [{'exp_date': '13.05.2025', 'start_time': '16:29:00', 'series_num': 2}]

df = pd.DataFrame(data)

dataframe_tdt(df, 900, 'cal')