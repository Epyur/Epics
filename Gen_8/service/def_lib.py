import pandas as pd
from wx.py.PyCrust import original
from .rout_map import *


def DictTitlesRename(aim_df, source_of_titles, key, val):
    df_start = pd.read_excel(source_of_titles)
    df = df_start.set_index(key)
    series_1 = df[val]
    title_dict = series_1.to_dict()
    df_a = aim_df
    df_a = df_a.rename(columns=title_dict)
    return df_a


def excel_column_to_dataframe_headers(excel_file, sheet_name, column_index):
    # Читаем Excel файл
    df_source = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Получаем значения из указанного столбца
    new_headers = df_source.iloc[:, column_index].tolist()

    # Создаем новый DataFrame с полученными заголовками
    df_new = pd.DataFrame(columns=new_headers)

    return df_new


def TakeDfFormExcel(file_nam,
                    filtre_column=None,
                    searched_index = None, ):
    try:
        df_start = pd.read_excel(file_nam)
        d_f = df_start.reset_index()

        if filtre_column:
            filtered_df = d_f[d_f[filtre_column].isin(searched_index)]
        else:
            return print('Номер не найден')
    except Exception as e:
        print(f'Ошибка:{e}')
        filtered_df = filtered_df.reset_index(drop=True)

    df_rename = DictTitlesRename(filtered_df, in_title, 'key', 'val')
    df_new = excel_column_to_dataframe_headers(in_title, 'Sheet1', 1)


    # Устанавливаем ключи
    target_df = df_new.set_index('index')
    original_columns = target_df.columns
    source_df = df_rename.set_index('index')

    # Заполнение пропущенных значений
    filled_df = target_df.combine_first(source_df)


    filled_df = filled_df[original_columns]
    filled_df = filled_df.sort_values(by='inc_ID', ascending=True)
    filled_df = filled_df.reset_index(drop=True, level=0)
    return filled_df

# функция преобразования формата дата в строку
def convert_date_format(df, columns):
    for col in columns:
        try:
            if pd.api.types.is_datetime64_dtype(df[col]):
                df[col] = df[col].dt.strftime('%d.%m.%Y')
            elif df[col].dtype == 'object':
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d.%m.%Y')
        except Exception as e:
            print(f"Ошибка при преобразовании столбца {col}: {e}")
    return df
# заполнение данных в строке из других датафреймов
def DfFiller(bd,
             df,
             aim_column,
             aim_value,
             control_column,
             control_value,
             columns_list,
             x = None):
    try:
        df_full = pd.read_excel(bd)
        df_filtered = df_full[df_full[aim_column] == aim_value]
        target_row = df[df[control_column] == control_value]
        if not target_row.empty and not df_filtered.empty:
            # Получаем индекс найденной строки
            target_index = target_row.index[0]
            source_index = df_filtered.index[0]
            # Переносим данные
            for item in columns_list:
                df.at[target_index, item] = df_filtered.at[source_index, item]
        else:
            print(f"По ID {x} строка с заданным условием не найдена")
        # print(ekn_df_filtered)
    except Exception as e:
        print(f'Ошибка здесь: {e}')
    return df

# разделить строку (для экспериментов без заявок)
def split_row(df, columns_to_move, columns_to_remove, columns_to_drop):
    # ищем строку
    target_row = df[df['series_num'] == 101]
    if not target_row.empty:
        # Получаем индекс найденной строки
        target_index = target_row.index[0]
        # print(target_index)
    # Создаем копию исходной строки
    new_row = df.loc[target_index].copy()

    # Переносим значения в новую строку
    for col in columns_to_move:
        new_row[col] = df.at[target_index, col]

    df.at[target_index, 'series_num'] = 1  # или другое значение по умолчанию
    new_row['series_num'] = 0

    # print(new_index)
    new_row_tr = new_row.reset_index()
    new_row_tr = new_row_tr.transpose()
    new_row_tr.columns = new_row_tr.iloc[0]
    new_row_tr = new_row_tr[1:]

    #формируем порядок колонок
    original_column = df.columns
    # Удаляем значения из исходной строки, которые нужно было удалить
    df.drop(columns=columns_to_drop, inplace=True)
    # Добавляем новую строку в конец датафрейма
    df_f = pd.concat([df, new_row_tr], ignore_index=True)
    df_f = df_f[original_column]
    df_f = df_f.sort_values(by='series_num', ascending=True).reset_index(drop=True, level=0)
    for col in columns_to_remove:
        df_f.at[0, col] = None

    return df_f

def MeanValue(df, list_to_mean, name_of_aim_column):
    df[name_of_aim_column] = df[list_to_mean].mean(axis=1).round(2)
    return df

def SpreadAndFill(df, col_list):
    
    for i in range(1, len(df)):
        for col in col_list:    
            mean_x = df.at[0, col]        
            df.at[i, col] = mean_x
    return df

def merge_duplicate_rows(df, key_columns, fixated_columns):
    # Создаем словарь для хранения объединенных строк
    merged_rows = {}
    
    # Находим все дубликаты
    duplicates = df.groupby(key_columns).groups
    
    for _, group in duplicates.items():
        if len(group) > 1:  # Если есть более одной строки с одинаковыми ключами
            max_index = len(group) - 1
            base_row = df.iloc[group[max_index]].copy()
            
            # Проходим по всем остальным строкам
            for i in range(0, len(group)-1):
                current_row = df.iloc[group[i]]
                
                # Заменяем значения в определенных колонках
                for col in df.columns:
                    for col1 in fixated_columns:
                        if pd.isna(base_row[col]) and not pd.isna(current_row[col]):
                            base_row[col] = current_row[col]
                        # Для остальных колонок берем первое найденное ненулевое значение
                        elif col == col1:
                            base_row[col] = current_row[col]
                        
            # Сохраняем объединенную строку
            merged_rows[group[0]] = base_row
            
    # Создаем новый DataFrame из объединенных строк
    result_df = df.copy()
    for index, row in merged_rows.items():
        result_df.loc[index] = row
        
    # Удаляем дубликаты, оставив только строки с минимальными индексами
    result_df = result_df.drop_duplicates(subset=key_columns, keep='first')
    
    return result_df

