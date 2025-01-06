import pandas as pd

dummy_data1 = {
        'id': ['no1', 'no2', 'no3', 'no4', 'no5'],
        'Feature1': ['A', 'C', 'E', 'G', 'I'],
        'Feature2': ['B', 'D', 'F', 'H', 'J']}

dummy_data2 = {
        'id': ['no5', 'no3', 'no1', 'no8', 'no12'],
        'Feature1': ['K', 'M', 'O', 'Q', 'S'],
        'Feature2': ['L', 'N', 'P', 'R', 'T']}

dummy_data3 = {
        'id': ['no1', 'no2', 'no3', 'no4', 'no5', 'no7', 'no8', 'no9', 'no10', 'no11'],
        'Feature1': [12, 13, 14, 15, 16, 17, 15, 12, 13, 23],
        'Feature2': [12, 13, 14, 15, 16, 17, 15, 12, 13, 23]}

df1 = pd.DataFrame(dummy_data1, columns = ['id', 'Feature1', 'Feature2'])
df2 = pd.DataFrame(dummy_data2, columns = ['id', 'Feature1', 'Feature2'])
df3 = pd.DataFrame(dummy_data3, columns = ['id', 'Feature1', 'Feature2'])


names = ['df1_', 'df2_', 'df3_']
dfs = [df1, df2, df3]

df_final = pd.concat([df.set_index('id').add_prefix(name) for name, df in zip(names, dfs)], axis=1).dropna()

print(df_final)

