import csv
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *
from pandas import ExcelWriter
import xlsxwriter

from .rout_map import TdtFile


# Укажите путь к вашему файлу TDT
def dataframe_tdt(df, delta, out_num):

    df_in = df.reset_index(drop=True, level=0)

    try:
        exp_date = df_in.at[0, 'exp_date'] # достаем дату из исходного датафрейма
        # print(exp_date)
        file_path = TdtFile(exp_date) # собираем путь к файлу термодата
        start_time = df_in.at[0, 'start_time'] # достаем время из датафрейма

        time_string = str(start_time)
        match = re.match(r'(\d+):(\d+):(\d+)', time_string)
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        # Открываем файл для чтения
        with open(file_path, newline='', encoding='utf-8') as file:
            # Создаем объект reader для чтения данных в формате csv
            try:
                reader = csv.reader(file, delimiter=' ')
            except:
                print('No such file')
            exp_num = int(df_in.at[0, 'series_num'])

            df_tdt = pd.DataFrame(list(reader))
            df_tdt = df_tdt.drop([0, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], axis=1)

            new_column_names = {
                1: 'Дата',
                2: 'Время',
                4: 'Термопара 1',
                8: 'Термопара 2',
                12: 'Термопара 3',
                16: 'Термопара 4'
            }
            df_tdt = df_tdt.rename(columns=new_column_names)
            df_tdt['Время'] = pd.to_datetime(df_tdt['Время'], format='%H:%M:%S')


            # Определение начальной и конечной точек временного интервала
            start_t = datetime(year=1900, month=1, day=1, hour=hours, minute=minutes, second=seconds)
            delta_time = pd.to_timedelta(delta, unit='s')
            end_time = start_t + delta_time

            # Фильтрация строк по временному интервалу
            df_tdt = df_tdt.loc[df_tdt['Время'].between(start_t, end_time)]

            columns_to_convert = ['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4']
            df_tdt[columns_to_convert] = df_tdt[columns_to_convert].apply(lambda x: x.str.replace(',', '.').astype(float))
            df_tdt[columns_to_convert] = df_tdt[columns_to_convert].apply(pd.to_numeric)

            average_values = df_tdt[columns_to_convert].mean(axis=1).round(1)
            df_tdt['Тср'] = average_values

            def time_difference_in_seconds(time1, time2):
                difference = time1 - time2
                return difference.total_seconds()
            # Применение функции и добавление новой колонки с разницей в секундах
            df_tdt['Время, с'] = df_tdt['Время'].apply(lambda x: time_difference_in_seconds(x, df_tdt['Время'].iloc[0]))
            df_tdt['Время, с'] = df_tdt['Время, с'].astype(int)

            df_tdt = df_tdt.drop(["Дата", "Время"], axis=1)
            # df = df.set_index('Время, с')

            #Формируем словари с данными по максимальным и минимальным температурам
            max_value1 = df_tdt['Термопара 1'].max()
            df_in.at[0, 'tp1_smog'] = max_value1
            max_value2 = df_tdt['Термопара 2'].max()
            df_in.at[0, 'tp2_smog'] = max_value2
            max_value3 = df_tdt['Термопара 3'].max()
            df_in.at[0, 'tp3_smog'] = max_value3
            max_value4 = df_tdt['Термопара 4'].max()
            df_in.at[0, 'tp4_smog'] = max_value4
            max_value_mean = df_tdt['Тср'].max()
            df_in.at[0, 'temp_of_smog'] = max_value_mean
            min_value_mean = df_tdt['Тср'].min()
            df_in.at[0, 'start_temp'] = min_value_mean


            #Формируем словари с данными по времени достижения максимальных температур
            time1 = df_tdt.loc[df_tdt['Термопара 1'] == max_value1, 'Время, с'].values[0]
            df_in.at[0, 'time_of_tp1'] = time1
            time2 = df_tdt.loc[df_tdt['Термопара 2'] == max_value2, 'Время, с'].values[0]
            df_in.at[0, 'time_of_tp2'] = time2
            time3 = df_tdt.loc[df_tdt['Термопара 3'] == max_value3, 'Время, с'].values[0]
            df_in.at[0, 'time_of_tp3'] = int(time3)
            time4 = df_tdt.loc[df_tdt['Термопара 4'] == max_value4, 'Время, с'].values[0]
            df_in.at[0, 'time_of_tp4'] = int(time4)
            time_mean = df_tdt.loc[df_tdt['Тср'] == max_value_mean, 'Время, с'].values[0]
            df_in.at[0, 'time_of_max_temp'] = int(time_mean)


            dd = str(out_num) + '_' + str(exp_num) + '.xlsx'
            out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
            df_tdt.to_excel(out_book)
            fig, ax = plt.subplots(figsize=(12, 4))
            df_tdt.plot(x='Время, с', y=['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'], ax=ax)
            ax.set_xlabel('Время, с')
            ax.set_ylabel('Температура, град.С')
            plt.title(f'График температур\n(Заявка № {out_num}, Эксперимент №{exp_num})')
            plt.legend(['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'])
            plt.grid(True)
            # plt.show()
            # Сохранение графика в виде изображения
            dd1 = str(out_num) + '_' + str(exp_num) + '.jpg'
            out_pic = os.path.abspath(os.path.join('.', 'out', str(out_num), dd1))
            plt.savefig(out_pic)
            df_out = df_in.copy()
    except Exception as e:
        print(f'Ошибка внутри функции обработки файла термодата: {e}')
        df_out = df_in
    return df_out

