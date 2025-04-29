import os
from pathlib import Path

import pandas as pd
import numpy as np
from .rout_map import ekn_book, ns


class FrameOfData:
    def __init__(self, excel_file=None, data=None, source_of_titles: pd.DataFrame = None, key=None, val=None):
        self.string_columns = None
        self.date_columns = None
        self.excel_file = excel_file
        self.data = data
        self.source_of_titles = source_of_titles
        self.key = key
        self.val = val
        self.df = None
        self.series_1 = None
        self.title_dict = None
        self.df_a = None
        self.columns = None

        # Проверка существования файла
        if excel_file and not Path(excel_file).exists():
            raise FileNotFoundError(f"Файл {excel_file} не найден")

    def convert_date_format(self, columns):
        self.columns = columns

        for col in self.columns:
            try:
                if pd.api.types.is_datetime64_dtype(self.data[col]):
                    self.data[col] = self.data[col].dt.strftime('%d.%m.%Y')
                elif self.data[col].dtype == 'object':
                    self.data[col] = pd.to_datetime(self.data[col], errors='coerce').dt.strftime('%d.%m.%Y')
            except Exception as e:
                print(f"Ошибка при преобразовании столбца {col}: {e}")
        return self.data

    def update_dataframe(self, date_columns=None, string_columns=None):
        self.date_columns = date_columns
        if self.date_columns is None:
            self.date_columns = [ns[x] for x in [32, 33, 76, 77]]

        self.string_columns = string_columns
        if self.string_columns is None:
            self.string_columns = [ns[x] for x in [11, 93, 94, 95, 96, 97, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26]]

        try:
            # Преобразование дат
            if self.date_columns:
                self.convert_date_format(self.date_columns)
            for col in self.string_columns:
                self.data[col] = self.data[col].astype(str)

            return self.data
        except Exception as e:
            print(f"Ошибка при обновлении DataFrame: {e}")
            return self.data

    def load_data(self, excel_file=None):
        if excel_file:
            self.excel_file = excel_file
        try:
            self.data = pd.read_excel(self.excel_file)
            return self.data
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return None

    def rename_df(self, key=None, val=None):
        if key is None or val is None:
            raise ValueError("Необходимо указать Исходные и Целевые значения для переименования")

        try:
            self.df = self.source_of_titles.set_index(key)
            self.series_1 = self.df[val]
            self.title_dict = self.series_1.to_dict()
            self.df_a = self.data.rename(columns=self.title_dict)
            return self.df_a
        except KeyError as e:
            print(f"Ошибка: {e}. Проверьте правильность Исходных и Целевых значений наименований колонок")
            return None

    # Дополнительные методы
    def describe_data(self):
        return self.data.describe()

    def clean_data(self):
        self.data.dropna(inplace=True)  # Удаление строк с пропусками
        self.data.drop_duplicates(inplace=True)  # Удаление дубликатов
        return self.data

    def save_data(self, output_file):
        try:
            self.df_a.to_excel(output_file, index=False)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def get_column_types(self):
        return self.data.dtypes

    def get_missing_values(self):
        return self.data.isnull().sum()

    def filter_rows(self, condition_func, create_new=True):
        """
        Метод для фильтрации строк по заданному условию

        Параметры:
        - condition_func: функция, принимающая строку DataFrame и возвращающая bool
        - create_new: если True, создает новый DataFrame, иначе фильтрует текущий

        Возвращает:
        - отфильтрованный DataFrame
        """
        try:
            if create_new:
                filtered_df = self.data[self.data.apply(condition_func, axis=1)]
                return filtered_df
            else:
                self.data = self.data[self.data.apply(condition_func, axis=1)]
                return self.data
        except Exception as e:
            print(f"Ошибка при фильтрации данных: {e}")
            return None


class Materials:
    def __init__(self, data, ekn=None):
        self.ekn = ekn
        self.data = data
        self.prop_group = None
        self.ekns = None
        self.lusya = None
        self.name = None
        self.sto = None
        self.thickness = None
        self.producer_name = None
        self.description = None
        self.comb_group = None
        self.flam_group = None



    def get_ekn(self, mat_name):
        filtered = self.data[self.data['product_name'].str.contains(mat_name, case=False, na=False)]
        self.ekns = filtered['ekn']
        return self.ekns

    def ask_lusie(self, word):
        self.lusya = self.data.loc[self.data['ekn'] == self.ekn, word].iloc[0]
        return self.lusya

    @property
    def get_name(self):
        try:
            self.name = self.ask_lusie('product_name')
            return self.name
        except:
            return 'no data'

    @property
    def get_sto(self):
        try:
            self.sto = self.ask_lusie('sto')
            return self.sto
        except:
            return 'no data'

    @property
    def get_thickness(self):
        try:
            self.thickness = self.ask_lusie('thickness')
            if self.thickness > 10:
                return int(self.thickness)
            else:
                return float(self.thickness)
        except:
            return np.nan

    @property
    def get_producer_name(self):
        try:
            self.producer_name = self.ask_lusie('producer')
            return self.producer_name
        except:
            return 'no data'

    @property
    def get_description(self):
        try:
            self.description = self.ask_lusie('short_discr')
            return self.description
        except:
            return 'no data'

    @property
    def get_comb_group(self):
        try:
            self.comb_group = self.ask_lusie('comb_indicator')
            return self.comb_group
        except:
            return 'no data'

    @property
    def get_flam_group(self):
        try:
            self.flam_group = self.ask_lusie('flam_indicator')
            return self.flam_group
        except:
            return 'no data'

    @property
    def get_prop_group(self):
        try:
            self.prop_group = self.ask_lusie('prop_indicator')
            return self.prop_group
        except:
            return 'no data'

class PhotoFinder:
    def __init__(self, base_dir):
        self.current_directory = os.getcwd()
        self.base_dir = base_dir
        self.search_part = None
        self.found_files = []

    def find_files_by_name_part(self, file_num):
        self.search_part = str(file_num)
        directory = os.path.join(self.current_directory, self.base_dir)

        for root, dirs, files in os.walk(directory):
            for file in files:
                if self.search_part in file:
                    self.found_files.append(os.path.join(root, file))

        return self.found_files

    def get_file_path(self, file_num):
        self.found_files = self.find_files_by_name_part(file_num)

        if not self.found_files:
            return None
        else:
            return self.found_files[0]

