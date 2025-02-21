import csv
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *
from pandas import ExcelWriter
import xlsxwriter

from Gen_6.service.routes import TdtFile


# Укажите путь к вашему файлу TDT
def dataframe_tdt(dict_in, delta, out_num, exp_num):
    dict_0 = {}


    exp_date = dict_in['exp_date'][exp_num] # достаем дату из исходного словаря
    date_list = exp_date.split('-') # Разбираем дату на составляющие
    year_of_date = date_list[0] # достаем год
    month_of_date = date_list[1] # достаем месяц
    day_of_date = date_list[2] # достаем день
    date_for_file = day_of_date + '.' + month_of_date + '.' + year_of_date # собираем дату в строчном режим
    file_path = TdtFile(date_for_file) # собираем путь к файлу термодата
    start_time = dict_in['start_time'][exp_num] # достаем время из словаря
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
        # df = df.set_index('Время, с')
        df_2 = df.copy()
        #Формируем словари с данными по максимальным и минимальным температурам
        max_value1 = df['Термопара 1'].max()
        dict_0.update({'tp1_smog':{exp_num: float(max_value1)}})
        max_value2 = df['Термопара 2'].max()
        dict_0.update({'tp2_smog': {exp_num: float(max_value2)}})
        max_value3 = df['Термопара 3'].max()
        dict_0.update({'tp3_smog': {exp_num: float(max_value3)}})
        max_value4 = df['Термопара 4'].max()
        dict_0.update({'tp4_smog': {exp_num: float(max_value4)}})
        max_value_mean = df['Тср'].max()
        dict_0.update({'temp_of_smog': {exp_num: float(round(max_value_mean, 1))}})
        min_value_mean = df['Тср'].min()
        dict_0.update({'tp0_mean': {exp_num: float(round(min_value_mean, 1))}})

        #Формируем словари с данными по времени достижения максимальных температур
        time1 = df.loc[df['Термопара 1'] == max_value1, 'Время, с'].values[0]
        dict_0.update({'time_of_tp1':{exp_num:int(time1)}})
        time2 = df.loc[df['Термопара 2'] == max_value2, 'Время, с'].values[0]
        dict_0.update({'time_of_tp2': {exp_num: int(time2)}})
        time3 = df.loc[df['Термопара 3'] == max_value3, 'Время, с'].values[0]
        dict_0.update({'time_of_tp3': {exp_num: int(time3)}})
        time4 = df.loc[df['Термопара 4'] == max_value4, 'Время, с'].values[0]
        dict_0.update({'time_of_tp4': {exp_num: int(time4)}})
        time_mean = df.loc[df['Тср'] == max_value_mean, 'Время, с'].values[0]
        dict_0.update({'time_of_max_temp': {exp_num: int(time_mean)}})

        dd = str(out_num) + '_' + str(exp_num) + '.xlsx'
        out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
        df.to_excel(out_book)
        fig, ax = plt.subplots(figsize=(12, 4))
        df.plot(x='Время, с', y=['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'], ax=ax)
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
        dict_0.update({'temperature_graph': {exp_num: out_pic}})
        # print(dict_0)
    return dict_0

