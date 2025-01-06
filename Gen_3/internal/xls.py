from datetime import datetime as dt
import pandas as pd
import numpy as np
from Gen_3.excel.routes import *

# ------------! РАЗБИРАЕМ книгу входящих заявок ! -----------------
inc_df_start = pd.read_excel(inc_book)
inc_df_columns = inc_df_start.columns.tolist()
inc_df = inc_df_start.rename(columns={'№ заявки': 'ID', 'ID заявки': 'Inc_ID', 'Дата поступления заявки': 'Date_in', 'e-mail заказчика': 'cust_mail', 'Цель испытания': 'inv_aim', 'Форма подтверждения соответствия': 'form', 'Приоритетность заявки': 'priority', 'Оцениваемая характеристика': 'cvality', 'Провести испытания во внешней лаборатории': 'ext_lab', 'Наименование внешней лаборатории': 'ext_lab_name', 'ЕКН материала (системы)': 'ekn', 'Наименование материала (при отсутствии ЕКН)': 'product_name', 'Идентификационные признаки образца': 'identity', 'Описание материала, для помещения в протокол': 'description', 'Тип материала (для отдельных групп методов)': 'product_type', 'Количество образцов передаваемых на испытания': 'number_of_prod', 'Фактическая толщина передаваемого образца': 'thickness', 'Целевой показатель (для НИОКР)': 'aim_cvality', 'Ссылки на приложенные файлы': 'link', 'Бюджет': 'budjet', 'Статья расходов': 'title_of_budget', 'ФИО согласующего': 'general_cast', 'Электронная почта согласующего': 'mail_of_general_cast'})
inc_df_columns_new = inc_df.columns.tolist()

# ------------! РАЗБИРАЕМ книгу условий в лаборатории ! -----------------
amb_df_start = pd.read_excel(amb_book)
amb_df_columns = amb_df_start.columns.tolist()
amb_df = amb_df_start.rename(columns = {'Дата': 'date_of_exp', 'Температура': 'amb_temp', 'Давление': 'amb_presue', 'Влажность': 'amb_moist', 'Lab': 'lab'})
amb_df_columns_new = amb_df.columns.tolist()

# ------------! РАЗБИРАЕМ книгу заказчиков ! -----------------
cust_df_start = pd.read_excel(cus_book)
cust_df_columns = cust_df_start.columns.tolist()
cust_df = cust_df_start.rename(columns = {'Наименование организации': 'cust_org', 'Реквизиты организации': 'cust_org_req', 'ФИО представителя': 'cust_name', 'Электронная почта представителя': 'cust_mail', 'Телефон представителя': 'cust_tel', 'СБЕ': 'SBE'})
cust_df_columns_new = cust_df.columns.tolist()
# print(cust_df_columns_new)

# ------------! РАЗБИРАЕМ книгу результатов испытаний на горючесть ! -----------------
def combustion():
    comb_df_start = pd.read_excel(comb_book)
    comb_df_columns = comb_df_start.columns.tolist()
    comb_df = comb_df_start.rename(columns = {'ID записи протокола': 'report_id', 'Дата протокола': 'report_date', '№ записи заявки на испытания': 'ID', 'Лаборатория': 'lab', 'Испытатель': 'investigator', 'Дата поступления образцов': 'date_of_product_coming', 'Дата проведения испытаний': 'date_of_exp', 'Ссылка на файл протокола полученного во внешней лаборатории': 'ext_lab_report', 'Температура дымовых газов': 'temp_of_smog', 'Время достижения максимальной температуры, с': 'time_of_max_temp', 'Длина повреждения образца 1 образца': 'len_1', 'Длина повреждений 2 образца': 'len_2', 'Длина повреждений 3 образца': 'len_3', 'Длина повреждений 4 образца': 'len_4', 'Масса образцов до испытания': 'mass_before', 'Масса образцов после испытания': 'mass_after', 'Время самостоятельного горения': 'combustion_time', 'Падение горящих капель расплава': 'flame_bubles', 'Тип основания под образец': 'type_of_osn', 'Способ крепления образца': 'fixation_type', 'Дополнительная информация': 'additional_inf', 'Фото образцов до испытания': 'foto_before', 'Фото образцов после испытания': 'foto_after', 'График температуры': 'grafic_of_temp', 'Номер серии': 'sery'})
    comb_df_columns_new = comb_df.columns.tolist()
    comb_df_merged = comb_df.merge(amb_df, how='left', on=["date_of_exp", "lab"])
    comb_df_merged['product_condition_time'] = np.nan
    comb_df_merged['middle_len'] = np.nan
    comb_df_merged['mass_los'] = np.nan
    comb_df_merged['group_by_smog_temp'] = np.nan
    comb_df_merged['group_by_len'] = np.nan
    comb_df_merged['group_by_mass_los'] = np.nan
    comb_df_merged['group_by_combustion'] = np.nan
    comb_df_merged['group_by_buble'] = np.nan
    comb_df_merged['match'] = np.nan
    comb_df_columns_new2 = comb_df_merged.columns.tolist()
    comb_df_ser1 = comb_df_merged.loc[comb_df_merged['sery'] == 1].copy()
    comb_df_shortened = comb_df_merged.drop(
        ['report_id', 'report_date', 'lab', 'investigator', 'date_of_product_coming', 'date_of_exp', 'ext_lab_report', 'type_of_osn', 'fixation_type',
         'amb_temp', 'amb_presue', 'amb_moist', 'product_condition_time'], axis=1)
    comb_df_ser2 = comb_df_shortened.loc[comb_df_shortened['sery'] == 2].copy()
    comb_df_ser3 = comb_df_shortened.loc[comb_df_shortened['sery'] == 3].copy()
    comb_df_2 =  comb_df_ser1.merge(comb_df_ser2, how='left', on=["ID"])
    comb_df_gen = comb_df_2.merge(comb_df_ser3, how='left', on=["ID"])
    comb_df_gen['gen_smog_temp'] = np.nan
    comb_df_gen['gen_middle_len'] = np.nan
    comb_df_gen['gen_middle_mass_los'] = np.nan
    comb_df_gen['gen_combustion_time'] = np.nan
    comb_df_gen['gen_babble'] = np.nan
    comb_df_gen['gen_group_by_smog_temp'] = np.nan
    comb_df_gen['gen_group_by_len'] = np.nan
    comb_df_gen['gen_group_by_mass_los'] = np.nan
    comb_df_gen['gen_group_by_combustion'] = np.nan
    comb_df_gen['gen_group_by_buble'] = np.nan
    comb_df_gen['gen_comb_group'] = np.nan
    comb_df_gen['gen_match'] = np.nan
    return comb_df_gen


# # ------------! РАЗБИРАЕМ книгу результатов испытаний на воспламеняемость ! -----------------
def flamability():
    flam_df_start = pd.read_excel(flam_book)
    flam_df_columns = flam_df_start.columns.tolist()
    flam_df = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id', 'Date_in': 'flam_report_date', 'ID_in': 'ID', 'ext lab': 'flam_lab', 'inventor': 'flam_investigator', 'day inc prod': 'flam_date_of_product_coming', 'dayX': 'flam_date_of_exp', 'link to report': 'flam_report_link', 'type of osn': 'flam_type_of_osn', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux', 'Факт воспламенения': 'flam', 'Время воспламенения': 'flam_time', 'dop inf': 'flam_dop_inf', '№ образца': 'exp_num'})
    flam_df_columns_new = flam_df.columns.tolist()
    amb_df_flam = amb_df_start.rename(columns = {'Дата': 'flam_date_of_exp', 'Температура': 'flam_amb_temp', 'Давление': 'flam_amb_presue', 'Влажность': 'flam_amb_moist', 'Lab': 'flam_lab'})
    flam_df_merged = flam_df.merge(amb_df_flam, how='left', on=["flam_date_of_exp", "flam_lab"])
    ser1 = flam_df_merged.loc[flam_df_merged['exp_num'] == 1].copy().set_index('ID')
    flam_df_shortened = flam_df_merged.drop(['flam_report_id', 'flam_report_date', 'flam_lab', 'flam_investigator', 'flam_date_of_product_coming', 'flam_date_of_exp', 'flam_report_link', 'flam_amb_temp', 'flam_amb_presue', 'flam_amb_moist', 'flam_type_of_osn'], axis=1)
    ser2 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 2].copy().set_index('ID')
    ser3 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 3].copy().set_index('ID')
    ser4 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 4].copy().set_index('ID')
    ser5 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 5].copy().set_index('ID')
    ser6 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 6].copy().set_index('ID')
    ser7 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 7].copy().set_index('ID')
    ser8 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 8].copy().set_index('ID')
    ser9 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 9].copy().set_index('ID')
    ser10 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 10].copy().set_index('ID')
    ser11 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 11].copy().set_index('ID')
    ser12 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 12].copy().set_index('ID')
    ser13 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 13].copy().set_index('ID')
    ser14 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 14].copy().set_index('ID')
    ser15 = flam_df_shortened.loc[flam_df_merged['exp_num'] == 15].copy().set_index('ID')
    dfs = [ser2, ser3, ser4, ser5, ser6, ser7, ser8, ser9, ser10, ser11, ser12, ser13, ser14, ser15]
    names = ["ser2_", "ser3_", "ser4_", "ser5_", "ser6_", "ser7_", "ser8_", "ser9_", "ser10_", "ser11_", "ser12_", "ser13_", "ser14_", "ser15_"]

    flam_df_gen = pd.concat([ser1, ser2, ser3, ser4, ser5, ser6, ser7, ser8, ser9, ser10, ser11, ser12, ser13, ser14, ser15], axis=1).reset_index()


    flam_df_gen['critical_density_of_heat_flux'] = np.nan
    flam_df_gen['group_of_flam'] = np.nan
    flam_df_columns_new2 = ser1.columns.tolist()
    return flam_df_gen

c_t = '01.01.2025'
f_d=dt.strptime(c_t, '%d.%m.%Y')