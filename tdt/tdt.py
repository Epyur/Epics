import csv
import re

import pandas as pd
import matplotlib.pyplot as plt
from datetime import *

from pandas import ExcelWriter
import xlsxwriter

# Укажите путь к вашему файлу TDT
def dataframe_tdt(file, start_time, delta):
    file_path = file
    time_string = start_time
    match = re.match(r'(\d+):(\d+):(\d+)', time_string)
    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    # Открываем файл для чтения
    with open(file_path, newline='', encoding='utf-8') as file:
        # Создаем объект reader для чтения данных в формате csv
        reader = csv.reader(file, delimiter=' ')
        df = pd.DataFrame(list(reader))
        df = df.drop([0, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], axis=1)

        new_column_names = {
            1: 'Дата',
            2: 'Время',
            4: 'Термопара 1',
            8: 'Термопара 2',
            12: 'Термопара 3',
            16: 'Термопара 4'
        }
        df = df.rename(columns=new_column_names)
        df['Время'] = pd.to_datetime(df['Время'], format='%H:%M:%S')
        # df['Время'] = df['Время'].apply(lambda x: x.strftime('%H:%M:%S'))

        # Определение начальной и конечной точек временного интервала
        start_t = datetime(year=1900, month=1, day=1, hour=hours, minute=minutes, second=seconds)
        delta_time = pd.to_timedelta(delta, unit='s')
        end_time = start_t + delta_time

        # Фильтрация строк по временному интервалу
        df = df.loc[df['Время'].between(start_t, end_time)]

        columns_to_convert = ['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4']
        df[columns_to_convert] = df[columns_to_convert].apply(lambda x: x.str.replace(',', '.').astype(float))
        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric)

        average_values = df[columns_to_convert].mean(axis=1).round(1)
        df['Тср'] = average_values

        def time_difference_in_seconds(time1, time2):
            difference = time1 - time2
            return difference.total_seconds()
        # Применение функции и добавление новой колонки с разницей в секундах
        df['Время, с'] = df['Время'].apply(lambda x: time_difference_in_seconds(x, df['Время'].iloc[0]))
        df['Время, с'] = df['Время, с'].astype(int)

        df = df.drop(["Дата", "Время"], axis=1)
        df = df.set_index('Время, с')
        df_2 = df.copy()
    return df_2
df = dataframe_tdt('24.01.2025 00_00.tdt', '11:36:20', 700)
print(df)

d_f = df.to_dict()
print(d_f)

    # # Нахождение максимального значения
    # max_value1 = df['Термопара 1'].max()
    # max_value2 = df['Термопара 2'].max()
    # max_value3 = df['Термопара 3'].max()
    # max_value4 = df['Термопара 4'].max()
    # max_value_mean = df['Тср'].max()
    #
    #
    #
    #
    #
    #
    #
    # # print("Типы данных колонок в датафрейме:\n", df.dtypes)
    #
    # # file_name = "tdt.xlsx"
    # # df.to_excel(file_name)
    # fig, ax = plt.subplots(figsize=(12, 4))
    # df.plot(x='Время, с', y=['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'], ax=ax)
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Temperature')
    # plt.title('График температур')
    # plt.legend(['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'])
    # plt.grid(True)
    # # plt.show()
    # # Сохранение графика в виде изображения
    # plt.savefig('age_graph.jpg')
    # # Экспорт DataFrame в Excel файл с использованием ExcelWriter
    #
    # # Экспорт данных в Excel
    # writer = pd.ExcelWriter('output_combined.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='Sheet1')
    #
    # # Добавление изображения графика на лист
    # workbook = writer.book
    # worksheet = writer.sheets['Sheet1']
    # worksheet.insert_image('C2', 'age_graph.jpg')
    #
    # # Сохранение файла
    # workbook.close()