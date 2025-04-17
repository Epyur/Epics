import pandas as pd


df = pd.read_excel('1.xlsx')
print(df)


def findindex(df, column, word):
    df_1 = list(df[column])
    count = -1
    for x in df_1:
        count += 1
        if x == word:
            y = count
    return y

index_0 = findindex(df, 'column 2', 'cleo')

df.at[2, 'column 2'] = df.at[index_0, 'column 2']

print(df)


# Пример DataFrame
data = {
    'A': [1, 2, 3],
    'B': ['apple', 'banana', 'cherry'],
    'C': [10, 20, 30]
}
df_n = pd.DataFrame(data)

# Определяем значение, которое мы хотим найти
value_to_find = 'banana'

# Поиск индекса строки с определенным значением в колонке 'B'
index = df_n.index[df_n['B'] == value_to_find][0]
print(type(index))
# if index:
#     print(f"Индекс строки, содержащей значение '{value_to_find}': {index}")
# else:
#     print(f"Значение '{value_to_find}' не найдено в DataFrame.")