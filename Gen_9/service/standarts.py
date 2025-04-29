import pandas as pd


from Gen_9.service.rout_map import ns


class GOST30244:
    def __init__(self, data, smog_temp=ns[43], list_of_length_columns=None, length_of_distraction=ns[51],
                 mass_before=ns[54], mass_after=ns[55], mass_loss=ns[56], combustion_time=ns[59], burning_drops=ns[62]):

        if list_of_length_columns is None:
            list_of_length_columns = [ns[47], ns[48], ns[49], ns[50]]
        self.data = data
        self.summary_group = None
        self.mass_loss_calculated = None
        self.smog_temp = smog_temp
        self.list_of_length_columns = list_of_length_columns
        self.length_of_distraction = length_of_distraction
        self.mass_before = mass_before
        self.mass_after = mass_after
        self.mass_loss = mass_loss
        self.combustion_time = combustion_time
        self.burning_drops = burning_drops
        self.column_to_compare = None
        self.index = None

    def group_by_smog(self, index):
        self.index = index
        try:
            if self.data.at[self.index, self.smog_temp] <= 135:
                return "Г1"
            elif self.data.at[self.index, self.smog_temp] <= 235:
                return "Г2"
            elif self.data[self.index, self.smog_temp].iloc[0] <= 450:
                return "Г3"
            else:
                return "Г4"
        except Exception as e:
            raise ValueError(f"Ошибка при определении группы по дымообразованию: {str(e)}")

    def calc_mean_length(self, index):
        self.index = index
        try:
            # Получаем значения из датафрейма по указанным колонкам
            length_values = [self.data[col].iloc[index] for col in self.list_of_length_columns]
            return round(sum(length_values) / len(length_values), 2)
        except Exception as e:
            raise ValueError(f"Ошибка при расчете средней длины: {str(e)}")

    def group_by_length(self, index):
        self.index = index
        try:
            length = self.data.at[self.index, self.length_of_distraction] if self.length_of_distraction is not None else self.calc_mean_length
            if length <= 65:
                return "Г1"
            elif length <= 85:
                return "Г2"
            else:
                return "Г3"
        except Exception as e:
            raise ValueError(f"Ошибка при определении группы по длине: {str(e)}")

    def calc_mass_loss(self, index):
        self.index = index
        try:
            return round(((1 - self.data.at[self.index, self.mass_after] / self.data.at[self.index, self.mass_before]) * 100), 2)
        except Exception as e:
            raise ValueError(f"Ошибка при расчете потери массы: {str(e)}")

    def group_by_mass_loss(self, index):
        self.index = index
        try:
            loss = self.data.at[self.index, self.mass_loss] if self.mass_loss is not None else self.calc_mass_loss
            if loss <= 20:
                return "Г1"
            elif loss <= 50:
                return "Г2"
            else:
                return "Г3"
        except Exception as e:
            raise ValueError(f"Ошибка при определении группы по потере массы: {str(e)}")

    def group_by_combustion_time(self, index):
        self.index = index
        try:
            time = self.data.at[self.index, self.combustion_time]
            if time == 0:
                return "Г1"
            elif time <= 30:
                return "Г2"
            elif time <= 300:
                return "Г3"
            else:
                return "Г4"
        except Exception as e:
            raise ValueError(f"Ошибка при определении группы по времени горения: {str(e)}")

    def group_by_drops(self, index):
        self.index = index
        try:
            drops = self.data.at[self.index, self.burning_drops]
            if drops == 'Нет':
                return "Г1"
            elif drops == 'Да':
                return "Г4"
            else:
                raise ValueError("Некорректное значение для капель")
        except Exception as e:
            raise ValueError(f"Ошибка при определении группы по каплям: {str(e)}")

    @property
    def summary_group(self):
        try:
            for x in range(0, len(self.data)):
                groups = [
                    self.group_by_smog(x),
                    self.group_by_length(x),
                    self.group_by_mass_loss(x),
                    self.group_by_combustion_time(x),
                    self.group_by_drops(x)
                ]
                # Определяем порядок групп для корректного сравнения
                group_order = {"Г1": 1, "Г2": 2, "Г3": 3, "Г4": 4}

                return max(groups, key=lambda x: group_order[x])
            return None
        except Exception as msg:
            raise ValueError(f"Ошибка при определении итоговой группы: {str(msg)}")

    def compare_columns(self, column_to_compare: str, index):
        self.column_to_compare = column_to_compare
        self.index = index
        try:
            # Получаем конкретные значения для сравнения
            ref_value = self.data.at[self.index, ns[23]]
            comp_value = self.data.at[self.index, self.column_to_compare]

            if ref_value < comp_value:
                return 'Не соответствует'
            else:
                return 'Соответствует'
        except Exception as msg:
            raise ValueError(f"Ошибка при сравнении столбцов: {str(msg)}")

    def update_dataframe(self):
        try:
            for i in [44, 51, 52, 56, 57, 60, 63, 65, 45, 53, 58, 61, 64, 66]:
                self.data[ns[i]] = self.data[ns[i]].astype(str)
            for x in range(0, len(self.data)):
                # Обновляем датафрейм новыми значениями
                self.data.at[x, ns[44]] = self.group_by_smog(x)
                self.data.at[x, ns[51]] = self.calc_mean_length(x)
                self.data.at[x, ns[52]] = self.group_by_length(x)
                self.data.at[x, ns[56]] = self.calc_mass_loss(x)
                self.data.at[x, ns[57]] = self.group_by_mass_loss(x)
                self.data.at[x, ns[60]] = self.group_by_combustion_time(x)
                self.data.at[x, ns[63]] = self.group_by_drops(x)
                self.data.at[x, ns[65]] = self.summary_group
                self.data.at[x, ns[45]] = self.compare_columns(ns[44], x)
                self.data.at[x, ns[53]] = self.compare_columns(ns[52], x)
                self.data.at[x, ns[58]] = self.compare_columns(ns[57], x)
                self.data.at[x, ns[61]] = self.compare_columns(ns[60], x)
                self.data.at[x, ns[64]] = self.compare_columns(ns[63], x)
                self.data.at[x, ns[66]] = self.compare_columns(ns[65], x)
            return self.data
        except Exception as e:
            raise ValueError(f"Ошибка при обновлении датафрейма: {str(e)}")

    def display_results(self):
        try:
            # Создаем словарь с результатами
            results = {
                'Группа по дымообразованию': self.group_by_smog,
                'Средняя длина оплавления': self.calc_mean_length,
                'Группа по длине': self.group_by_length,
                'Расчетная потеря массы': self.calc_mass_loss,
                'Группа по потере массы': self.group_by_mass_loss,
                'Группа по времени горения': self.group_by_combustion_time,
                'Группа по каплям': self.group_by_drops,
                'Итоговая группа': self.summary_group
            }
            return pd.DataFrame([results])
        except Exception as e:
            raise ValueError(f"Ошибка при отображении результатов: {str(e)}")

    @summary_group.setter
    def summary_group(self, value):
        self._summary_group = value


class GOST30402:

    def __init__(self, data, kptp=ns[81]):
        self.data = data
        self.kptp = kptp
        self.index = None


    def flam_group(self,
                   index=None):
        if index is None:
            index = self.data[self.data[ns[9]] == 103].index[0]
        self.index = index
        try:

            kptp_s = self.data.at[self.index, self.kptp]
            if kptp_s <= 30:
                r = "В2"
            if kptp_s <= 15:
                r = "В3"
            if kptp_s > 30:
                r = "В1"
            return r
        except Exception as msg:
            return msg
    @property
    def compare_columns(self):
        self.column_to_compare = ns[84]
        self.index = self.data[self.data[ns[9]] == 103].index[0]
        try:
            # Получаем конкретные значения для сравнения
            ref_value = self.data.at[self.index, ns[24]]
            comp_value = self.data.at[self.index, self.column_to_compare]

            if ref_value < comp_value:
                return 'Не соответствует'
            else:
                return 'Соответствует'
        except Exception as msg:
            raise ValueError(f"Ошибка при сравнении столбцов: {str(msg)}")

    def update_dataframe(self):
        self.index = self.data[self.data[ns[9]] == 103].index[0]
        try:
            self.data[ns[84]] = self.data[ns[84]].astype(str)
            self.data[ns[85]] = self.data[ns[85]].astype(str)
            self.data.at[self.index, ns[84]] = self.flam_group()
            self.data.at[self.index, ns[85]] = self.compare_columns
            return self.data
        except Exception as e:
            raise ValueError(f"Ошибка при обновлении датафрейма: {str(e)}")




