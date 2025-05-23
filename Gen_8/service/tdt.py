import csv
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *
from pandas import ExcelWriter
import xlsxwriter

from .rout_map import TdtFile, ns, calibration  # Предполагается, что calibration содержит путь к калибровочному файлу


def dataframe_tdt(df, delta, out_num, file_path=None, calibration_file_path=calibration):
    df_in = df.reset_index(drop=True, level=0)

    try:
        exp_date = df_in.at[0, ns[33]]
        if file_path is None:
            file_path = TdtFile(exp_date)
        else:
            file_path = file_path
        start_time = df_in.at[0, ns[69]]

        time_string = str(start_time)
        match = re.match(r'(\d+):(\d+):(\d+)', time_string)
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))

        with open(file_path, newline='', encoding='utf-8') as file:
            try:
                reader = csv.reader(file, delimiter=' ')
            except:
                print('No such file')
            exp_num = int(df_in.at[0, ns[9]])

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

            start_t = datetime(year=1900, month=1, day=1, hour=hours, minute=minutes, second=seconds)
            delta_time = pd.to_timedelta(delta, unit='s')
            end_time = start_t + delta_time

            df_tdt = df_tdt.loc[df_tdt['Время'].between(start_t, end_time)]

            columns_to_convert = ['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4']
            try:
                for i in columns_to_convert:
                    df_tdt[i] = df_tdt[i].replace('X', np.nan, regex=True)
            except:
                print('Проверьте целостность данных термопар, возможно вы потеряли одну или более термопар')

            df_tdt[columns_to_convert] = df_tdt[columns_to_convert].apply(
                lambda x: x.str.replace(',', '.').astype(float))
            df_tdt[columns_to_convert] = df_tdt[columns_to_convert].apply(pd.to_numeric)

            average_values = df_tdt[columns_to_convert].mean(axis=1).round(1)
            df_tdt['Тср'] = average_values

            def time_difference_in_seconds(time1, time2):
                difference = time1 - time2
                return difference.total_seconds()

            df_tdt['Время, с'] = df_tdt['Время'].apply(lambda x: time_difference_in_seconds(x, df_tdt['Время'].iloc[0]))
            df_tdt['Время, с'] = df_tdt['Время, с'].astype(int)

            # Функция для определения начала устойчивого роста температуры
            def find_heating_start(temp_series, time_series, min_rising_duration=10, offset_before=5):
                rising_duration = 0
                start_idx = 0

                for i in range(1, len(temp_series)):
                    if temp_series.iloc[i] > temp_series.iloc[i - 1]:
                        rising_duration += (time_series.iloc[i] - time_series.iloc[i - 1])
                        if rising_duration >= min_rising_duration:
                            start_time = time_series.iloc[i] - rising_duration - offset_before
                            return max(start_time, 0)
                    else:
                        rising_duration = 0
                return 0

            heating_start = find_heating_start(df_tdt['Тср'], df_tdt['Время, с'])
            df_tdt['Время, с'] = df_tdt['Время, с'] - heating_start

            # Вычисление производной температуры
            df_tdt['dТср/dt'] = np.gradient(df_tdt['Тср'], df_tdt['Время, с'])

            # ===== ЗАГРУЗКА И ОБРАБОТКА КАЛИБРОВОЧНЫХ ДАННЫХ =====
            if calibration_file_path and os.path.exists(calibration_file_path):
                try:
                    df_calib = pd.read_excel(calibration_file_path)

                    # Приводим временные шкалы к одинаковому диапазону
                    df_calib = df_calib[df_calib['Время, с'] <= df_tdt['Время, с'].max()]

                    # Интерполяция калибровочных данных на временную сетку эксперимента
                    calib_deriv = np.interp(df_tdt['Время, с'],
                                            df_calib['Время, с'],
                                            df_calib['def'])

                    # Вычисляем разницу между экспериментальной и калибровочной производными
                    df_tdt['dТср/dt_diff'] = df_tdt['dТср/dt'] - calib_deriv

                except Exception as e:
                    print(f"Ошибка обработки калибровочных данных: {e}")
                    df_tdt['dТср/dt_diff'] = df_tdt['dТср/dt']
            else:
                print("Калибровочный файл не указан или не найден")
                df_tdt['dТср/dt_diff'] = df_tdt['dТср/dt']

            # ===== СОЗДАНИЕ ГРАФИКОВ =====
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

            # График температур (без изменений)
            df_tdt.plot(x='Время, с', y=['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'], ax=ax1)
            ax1.set_ylabel('Температура, град.С')
            ax1.legend(['Термопара 1', 'Термопара 2', 'Термопара 3', 'Термопара 4', 'Тср'])
            ax1.grid(True)

            # График разницы производных (экспериментальная - калибровочная)
            line, = ax2.plot(df_tdt['Время, с'], df_tdt['dТср/dt_diff'], color='purple', linewidth=1)

            # Находим точки пересечения с осью X (где разница производных меняет знак)
            zero_crossings = np.where(np.diff(np.sign(df_tdt['dТср/dt_diff'])))[0]

            # Добавляем начальную и конечную точки
            segments = []
            if len(zero_crossings) > 0:
                segments.append((0, zero_crossings[0]))
                for i in range(len(zero_crossings) - 1):
                    segments.append((zero_crossings[i], zero_crossings[i + 1]))
                segments.append((zero_crossings[-1], len(df_tdt) - 1))
            else:
                segments.append((0, len(df_tdt) - 1))

            # Рассчитываем площади для каждого сегмента
            segment_areas = []
            for start_idx, end_idx in segments:
                x_segment = df_tdt['Время, с'].iloc[start_idx:end_idx + 1]
                y_segment = df_tdt['dТср/dt_diff'].iloc[start_idx:end_idx + 1]
                area = np.trapz(y_segment, x_segment)
                if abs(area) >= 1.5:  # Фильтрация площадей менее 1.5
                    segment_areas.append({
                        'start_time': df_tdt['Время, с'].iloc[start_idx],
                        'end_time': df_tdt['Время, с'].iloc[end_idx],
                        'area': abs(area),
                        'is_positive': y_segment.mean() > 0,
                        'max_y': y_segment.max() if y_segment.mean() > 0 else y_segment.min()
                    })

            # Сортируем сегменты по времени
            segment_areas.sort(key=lambda x: x['start_time'])

            # Рассчитываем суммарные площади
            total_positive = sum([seg['area'] for seg in segment_areas if seg['is_positive']])
            total_negative = sum([seg['area'] for seg in segment_areas if not seg['is_positive']])

            # Оформление графика разницы производных
            for i, segment in enumerate(segment_areas):
                start_idx = df_tdt['Время, с'].searchsorted(segment['start_time'])
                end_idx = df_tdt['Время, с'].searchsorted(segment['end_time'])

                x_segment = df_tdt['Время, с'].iloc[start_idx:end_idx + 1]
                y_segment = df_tdt['dТср/dt_diff'].iloc[start_idx:end_idx + 1]

                color = 'green' if segment['is_positive'] else 'red'
                alpha = 0.3

                ax2.fill_between(
                    x_segment,
                    y_segment,
                    where=(y_segment > 0) if segment['is_positive'] else (y_segment < 0),
                    color=color,
                    alpha=alpha
                )

                # Добавляем аннотацию с площадью
                mid_x = (segment['start_time'] + segment['end_time']) / 2
                y_pos = segment['max_y'] * 1.1

                ax2.text(
                    mid_x,
                    y_pos,
                    f"{segment['area']:.1f}",
                    ha='center',
                    va='center',
                    fontsize=9,
                    bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.7)
                )

                # Линии выноски
                ax2.plot([mid_x, mid_x], [y_segment.mean(), y_pos],
                         color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

            # Легенда с суммарными площадями
            handles = [line]
            labels = [f'Разница производных\nS⁺={total_positive:.1f} (нагрев)\nS⁻={total_negative:.1f} (охлаждение)']

            ax2.legend(handles, labels, loc='upper right')
            ax2.set_xlabel('Время, с (относительно начала нагрева)')
            ax2.set_ylabel('Разница производных, град.С/с')
            ax2.grid(True)

            # Общий заголовок
            plt.suptitle(f'График температур и разницы производных\n(Заявка № {out_num}, Эксперимент №{exp_num})')
            plt.tight_layout()
            # Формируем словари с данными по максимальным и минимальным температурам
            max_value1 = df_tdt['Термопара 1'].max()
            df_in.at[0, ns[35]] = max_value1
            max_value2 = df_tdt['Термопара 2'].max()
            df_in.at[0, ns[37]] = max_value2
            max_value3 = df_tdt['Термопара 3'].max()
            df_in.at[0, ns[39]] = max_value3
            max_value4 = df_tdt['Термопара 4'].max()
            df_in.at[0, ns[41]] = max_value4
            max_value_mean = df_tdt['Тср'].max()
            df_in.at[0, ns[43]] = max_value_mean
            min_value_mean = df_tdt['Тср'].min()
            df_in.at[0, 'start_temp'] = min_value_mean

            # Формируем словари с данными по времени достижения максимальных температур
            time1 = df_tdt.loc[df_tdt['Термопара 1'] == max_value1, 'Время, с'].values[0]
            df_in.at[0, ns[36]] = time1 + heating_start  # Сохраняем исходное время
            time2 = df_tdt.loc[df_tdt['Термопара 2'] == max_value2, 'Время, с'].values[0]
            df_in.at[0, ns[38]] = time2 + heating_start
            time3 = df_tdt.loc[df_tdt['Термопара 3'] == max_value3, 'Время, с'].values[0]
            df_in.at[0, ns[40]] = int(time3) + heating_start
            time4 = df_tdt.loc[df_tdt['Термопара 4'] == max_value4, 'Время, с'].values[0]
            df_in.at[0, ns[42]] = int(time4) + heating_start
            time_mean = df_tdt.loc[df_tdt['Тср'] == max_value_mean, 'Время, с'].values[0]
            df_in.at[0, ns[46]] = int(time_mean) + heating_start
            # Сохранение данных
            df_tdt = df_tdt.drop(["Дата", "Время"], axis=1)
            dd = str(out_num) + '_' + str(exp_num) + '.xlsx'
            out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
            df_tdt.to_excel(out_book)

            # Сохранение графика
            dd1 = str(out_num) + '_' + str(int(exp_num)) + '.jpg'
            out_pic = os.path.abspath(os.path.join('.', 'out', str(out_num), dd1))
            plt.savefig(out_pic)
            plt.close()

            df_out = df_in.copy()
    except Exception as e:
        print(f'Ошибка внутри функции обработки файла термодата: {e}')
        df_out = df_in
    return df_out