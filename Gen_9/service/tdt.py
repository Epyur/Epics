import re
import csv
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from Gen_9.service.rout_map import tdt_path


class TermoDataAnalyzer:
    def __init__(self, exp_date=None, start_time=None, series_num=None, delta=None,
                 out_num=None, folder=None):

        self.output_dir = None
        self.delta = delta
        self.out_num = out_num
        self.exp_date = exp_date
        self.start_time = start_time
        self.exp_num = series_num
        self.df_tdt = None
        self.processed_data = None
        self.folder = folder
        if folder is None:
            self.folder = tdt_path
        self.file_path = os.path.join(self.folder, f'{self.exp_date} 00_00.tdt')

    def parse_time(self):
        """Разбирает строку времени на компоненты"""
        match = re.match(r'(\d+):(\d+):(\d+)', self.start_time)
        return map(int, match.groups())

    def load_tdt_data(self, file_path):
        """Загружает и обрабатывает данные из файла термодаты"""
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=' ')
                self.df_tdt = pd.DataFrame(list(reader))
                self._clean_and_rename_columns()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл термодаты не найден: {file_path}")

    def _clean_and_rename_columns(self):
        """Очищает и переименовывает столбцы DataFrame"""
        self.df_tdt = self.df_tdt.drop([0, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], axis=1)
        new_column_names = {
            1: 'Дата',
            2: 'Время',
            4: 'Термопара 1',
            8: 'Термопара 2',
            12: 'Термопара 3',
            16: 'Термопара 4'
        }
        self.df_tdt = self.df_tdt.rename(columns=new_column_names)
        self.df_tdt['Время'] = pd.to_datetime(self.df_tdt['Время'], format='%H:%M:%S')

    def filter_by_time_range(self):
        """Фильтрует данные по временному диапазону"""
        hours, minutes, seconds = self.parse_time()
        start_t = datetime(year=1900, month=1, day=1, hour=hours, minute=minutes, second=seconds)
        delta_time = pd.to_timedelta(self.delta, unit='s')
        end_time = start_t + delta_time
        self.df_tdt = self.df_tdt.loc[self.df_tdt['Время'].between(start_t, end_time)]

    def process_temperature_data(self):
        """Обрабатывает температурные данные"""
        columns_to_convert = ['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4']
        for i in columns_to_convert:
            self.df_tdt[i] = self.df_tdt[i].replace('X', np.nan, regex=True)
        self.df_tdt[columns_to_convert] = self.df_tdt[columns_to_convert].apply(
            lambda x: x.str.replace(',', '.').astype(float)
        )

        # Добавляем среднюю температуру
        self.df_tdt['Тср'] = self.df_tdt[columns_to_convert].mean(axis=1).round(1)

        # Добавляем время в секундах
        self.df_tdt['Время, с'] = (self.df_tdt['Время'] - self.df_tdt['Время'].iloc[0]).dt.total_seconds().astype(int)

        # Удаляем ненужные колонки
        self.df_tdt = self.df_tdt.drop(["Дата", "Время"], axis=1)

    def calculate_max_values(self):
        """Вычисляет максимальные значения температур и время их достижения"""
        temp_columns = ['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср']
        time_column = 'Время, с'
        data_list = []
        for i, col in enumerate(temp_columns, start=1):
            max_value = float(self.df_tdt[col].max())
            time_of_max = int(self.df_tdt.loc[self.df_tdt[col] == max_value, time_column].values[0])
            data_list.append((max_value, time_of_max))
        return data_list

    def save_results(self):
        """Сохраняет результаты в файлы"""
        self.output_dir = os.path.abspath(os.path.join('.', 'out', str(self.out_num)))
        os.makedirs(self.output_dir, exist_ok=True)

        # Сохраняем данные в Excel
        excel_file = os.path.join(self.output_dir, f'{self.out_num}_{self.exp_num}.xlsx')
        self.df_tdt.to_excel(excel_file)

        # Сохраняем график
        self.plot_temperature_data()

    def plot_temperature_data(self):
        """Строит и сохраняет график температур"""
        fig, ax = plt.subplots(figsize=(12, 4))
        self.df_tdt.plot(
            x='Время, с',
            y=['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'],
            ax=ax
        )

        ax.set_xlabel('Время, с')
        ax.set_ylabel('Температура, град.С')
        plt.title(f'График температур\n(Заявка № {self.out_num}, Эксперимент №{self.exp_num})')
        plt.legend(['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'])
        plt.grid(True)

        plot_file = os.path.join(self.output_dir, f'{self.out_num}_{self.exp_num}.jpg')
        plt.savefig(plot_file)
        plt.close()
        return plot_file

    def analyze(self):
        """Основной метод для выполнения анализа"""
        self.load_tdt_data(self.file_path)
        self.filter_by_time_range()
        self.process_temperature_data()
        self.calculate_max_values()
        self.save_results()

        return self.calculate_max_values()
