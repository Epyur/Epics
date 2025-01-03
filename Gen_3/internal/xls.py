import xlrd
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
    comb_df_merged['group_by_buble'] = np.nan
    comb_df_ser1 = comb_df_merged.loc[comb_df_merged['sery'] == 1].copy()
    comb_df_ser2 = comb_df_merged.loc[comb_df_merged['sery'] == 2].copy()
    comb_df_ser3 = comb_df_merged.loc[comb_df_merged['sery'] == 3].copy()
    comb_df_2 =  comb_df_ser1.merge(comb_df_ser2, how='left', on=["ID"])
    comb_df_gen = comb_df_2.merge(comb_df_ser3, how='left', on=["ID"])
    comb_df_gen['gen_middle_len'] = np.nan
    comb_df_gen['middle_mass_los'] = np.nan
    comb_df_gen['gen_group_by_smog_temp'] = np.nan
    comb_df_gen['gen_group_by_len'] = np.nan
    comb_df_gen['gen_group_by_mass_los'] = np.nan
    comb_df_gen['gen_group_by_buble'] = np.nan
    return comb_df_gen


# # ------------! РАЗБИРАЕМ книгу результатов испытаний на воспламеняемость ! -----------------
def flamability():

    flam_df_start = pd.read_excel(flam_book)
    flam_df = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id', 'Date_in': 'flam_report_date', 'ID_in': 'ID', 'ext lab': 'flam_lab', 'inventor': 'flam_investigator', 'day inc prod': 'flam_date_of_product_coming', 'dayX': 'flam_date_of_exp', 'link to report': 'flam_report_link', 'type of osn': 'flam_type_of_osn', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux', 'Факт воспламенения': 'flam', 'Время воспламенения': 'flam_time', 'dop inf': 'flam_dop_inf', '№ образца': 'exp_num'})

    amb_df_flam = amb_df_start.rename(columns = {'Дата': 'flam_date_of_exp', 'Температура': 'flam_amb_temp', 'Давление': 'flam_amb_presue', 'Влажность': 'flam_amb_moist', 'Lab': 'flam_lab'})
    flam_df_1 = flam_df.groupby('ID')[['flam_report_id', 'flam_report_date', 'flam_lab', 'flam_investigator', 'flam_date_of_product_coming', 'flam_date_of_exp', 'flam_report_link', 'flam_type_of_osn', 'flam_density_of_heat_flux', 'flam', 'flam_time', 'flam_dop_inf', 'exp_num']].apply(lambda x: pd.DataFrame(x.values)).unstack().reset_index()
    flam_df_2 = flam_df_1.columns.droplevel()
    flam_df_3 = flam_df_2.columns['ID', 'flam_report_id', 'flam_report_date', 'flam_lab', 'flam_investigator', 'flam_date_of_product_coming', 'flam_date_of_exp', 'flam_report_link', 'flam_type_of_osn', 'exp_num_1', 'flam_density_of_heat_flux_1', 'flam_1', 'flam_time_1', 'flam_dop_inf_1',
                                   'flam_report_id_2', 'flam_report_date_2', 'flam_lab_2', 'flam_investigator_2', 'flam_date_of_product_coming_2', 'flam_date_of_exp_2', 'flam_report_link_2', 'flam_type_of_osn_2', 'exp_num_2', 'flam_density_of_heat_flux_2', 'flam_2', 'flam_time_2', 'flam_dop_inf_2',
                                   'flam_report_id_3', 'flam_report_date_3', 'flam_lab_3', 'flam_investigator_3', 'flam_date_of_product_coming_3', 'flam_date_of_exp_3', 'flam_report_link_3', 'flam_type_of_osn_3', 'exp_num_3', 'flam_density_of_heat_flux_3', 'flam_3', 'flam_time_3', 'flam_dop_inf_3',
                                   'flam_report_id_4', 'flam_report_date_4', 'flam_lab_4', 'flam_investigator_4', 'flam_date_of_product_coming_4', 'flam_date_of_exp_4', 'flam_report_link_4', 'flam_type_of_osn_4', 'exp_num_4', 'flam_density_of_heat_flux_4', 'flam_4', 'flam_time_4', 'flam_dop_inf_4',
                                   'flam_report_id_5', 'flam_report_date_5', 'flam_lab_5', 'flam_investigator_5', 'flam_date_of_product_coming_5', 'flam_date_of_exp_5', 'flam_report_link_5', 'flam_type_of_osn_5', 'exp_num_5', 'flam_density_of_heat_flux_5', 'flam_5', 'flam_time_5', 'flam_dop_inf_5',
                                   'flam_report_id_6', 'flam_report_date_6', 'flam_lab_6', 'flam_investigator_6', 'flam_date_of_product_coming_6', 'flam_date_of_exp_6', 'flam_report_link_6', 'flam_type_of_osn_6', 'exp_num_6', 'flam_density_of_heat_flux_6', 'flam_6', 'flam_time_6', 'flam_dop_inf_6',
                                   'flam_report_id_7', 'flam_report_date_7', 'flam_lab_7', 'flam_investigator_7', 'flam_date_of_product_coming_7', 'flam_date_of_exp_7', 'flam_report_link_7', 'flam_type_of_osn_7', 'exp_num_7', 'flam_density_of_heat_flux_7', 'flam_7', 'flam_time_7', 'flam_dop_inf_7',
                                   'flam_report_id_8', 'flam_report_date_8', 'flam_lab_8', 'flam_investigator_8', 'flam_date_of_product_coming_8', 'flam_date_of_exp_8', 'flam_report_link_8', 'flam_type_of_osn_8', 'exp_num_8', 'flam_density_of_heat_flux_8', 'flam_8', 'flam_time_8', 'flam_dop_inf_8',
                                   'flam_report_id_9', 'flam_report_date_9', 'flam_lab_9', 'flam_investigator_9', 'flam_date_of_product_coming_9', 'flam_date_of_exp_9', 'flam_report_link-9', 'flam_type_of_osn_9', 'exp_num_9', 'flam_density_of_heat_flux_9', 'flam_9', 'flam_time_9', 'flam_dop_inf_9',
                                   'flam_report_id_10', 'flam_report_date_10', 'flam_lab_10', 'flam_investigator_10', 'flam_date_of_product_coming_10', 'flam_date_of_exp_10', 'flam_report_link_10', 'flam_type_of_osn_10', 'exp_num_10', 'flam_density_of_heat_flux_10', 'flam_10', 'flam_time_10', 'flam_dop_inf_10',
                                   'flam_report_id_11', 'flam_report_date_11', 'flam_lab_11', 'flam_investigator_11', 'flam_date_of_product_coming_11', 'flam_date_of_exp_11', 'flam_report_link_11', 'flam_type_of_osn_11', 'exp_num_11', 'flam_density_of_heat_flux_11', 'flam_11', 'flam_time_11', 'flam_dop_inf_11',
                                   'flam_report_id_12', 'flam_report_date_12', 'flam_lab_12', 'flam_investigator_12', 'flam_date_of_product_coming_12', 'flam_date_of_exp_12', 'flam_report_link_12', 'flam_type_of_osn_12', 'exp_num_12', 'flam_density_of_heat_flux_12', 'flam_12', 'flam_time_12', 'flam_dop_inf_12',
                                   'flam_report_id_13', 'flam_report_date_13', 'flam_lab_13', 'flam_investigator_13', 'flam_date_of_product_coming_13', 'flam_date_of_exp_13', 'flam_report_link_13', 'flam_type_of_osn_13', 'exp_num_13', 'flam_density_of_heat_flux_13', 'flam_13', 'flam_time_13', 'flam_dop_inf_13',
                                   'flam_report_id_14', 'flam_report_date_14', 'flam_lab_14', 'flam_investigator_14', 'flam_date_of_product_coming_14', 'flam_date_of_exp_14', 'flam_report_link_14', 'flam_type_of_osn_14', 'exp_num_14', 'flam_density_of_heat_flux_14', 'flam_14', 'flam_time_14', 'flam_dop_inf_14',
                                   'flam_report_id_15', 'flam_report_date-15', 'flam_lab_15', 'flam_investigator_15', 'flam_date_of_product_coming_15', 'flam_date_of_exp_15', 'flam_report_link_15', 'flam_type_of_osn_15', 'exp_num_15', 'flam_density_of_heat_flux_15', 'flam_15', 'flam_time_15', 'flam_dop_inf_15']
    flam_df_shortened = flam_df_3.drop(['flam_report_id_2', 'flam_report_date_2', 'flam_lab_2', 'flam_investigator_2', 'flam_date_of_product_coming_2', 'flam_date_of_exp_2', 'flam_report_link_2', 'flam_type_of_osn_2',
                                     'flam_report_id_3', 'flam_report_date_3', 'flam_lab_3', 'flam_investigator_3', 'flam_date_of_product_coming_3', 'flam_date_of_exp_3', 'flam_report_link_3', 'flam_type_of_osn_3',
                                     'flam_report_id_4', 'flam_report_date_4', 'flam_lab_4', 'flam_investigator_4', 'flam_date_of_product_coming_4', 'flam_date_of_exp_4', 'flam_report_link_4', 'flam_type_of_osn_4',
                                     'flam_report_id_5', 'flam_report_date_5', 'flam_lab_5', 'flam_investigator_5', 'flam_date_of_product_coming_5', 'flam_date_of_exp_5', 'flam_report_link_5', 'flam_type_of_osn_5',
                                     'flam_report_id_6', 'flam_report_date_6', 'flam_lab_6', 'flam_investigator_6', 'flam_date_of_product_coming_6', 'flam_date_of_exp_6', 'flam_report_link_6', 'flam_type_of_osn_6',
                                     'flam_report_id_7', 'flam_report_date_7', 'flam_lab_7', 'flam_investigator_7', 'flam_date_of_product_coming_7', 'flam_date_of_exp_7', 'flam_report_link_7', 'flam_type_of_osn_7',
                                     'flam_report_id_8', 'flam_report_date_8', 'flam_lab_8', 'flam_investigator_8', 'flam_date_of_product_coming_8', 'flam_date_of_exp_8', 'flam_report_link_8', 'flam_type_of_osn_8',
                                     'flam_report_id_9', 'flam_report_date_9', 'flam_lab_9', 'flam_investigator_9', 'flam_date_of_product_coming_9', 'flam_date_of_exp_9', 'flam_report_link-9', 'flam_type_of_osn_9',
                                     'flam_report_id_10', 'flam_report_date_10', 'flam_lab_10', 'flam_investigator_10', 'flam_date_of_product_coming_10', 'flam_date_of_exp_10', 'flam_report_link_10', 'flam_type_of_osn_10',
                                     'flam_report_id_11', 'flam_report_date_11', 'flam_lab_11', 'flam_investigator_11', 'flam_date_of_product_coming_11', 'flam_date_of_exp_11', 'flam_report_link_11', 'flam_type_of_osn_11',
                                     'flam_report_id_12', 'flam_report_date_12', 'flam_lab_12', 'flam_investigator_12', 'flam_date_of_product_coming_12', 'flam_date_of_exp_12', 'flam_report_link_12', 'flam_type_of_osn_12',
                                     'flam_report_id_13', 'flam_report_date_13', 'flam_lab_13', 'flam_investigator_13', 'flam_date_of_product_coming_13', 'flam_date_of_exp_13', 'flam_report_link_13', 'flam_type_of_osn_13',
                                     'flam_report_id_14', 'flam_report_date_14', 'flam_lab_14', 'flam_investigator_14', 'flam_date_of_product_coming_14', 'flam_date_of_exp_14', 'flam_report_link_14', 'flam_type_of_osn_14',
                                     'flam_report_id_15', 'flam_report_date-15', 'flam_lab_15', 'flam_investigator_15', 'flam_date_of_product_coming_15', 'flam_date_of_exp_15', 'flam_report_link_15', 'flam_type_of_osn_15'], axis=1)
    flam_df_merged = flam_df_shortened.merge(amb_df_flam, how='left', on=["flam_date_of_exp", "flam_lab"])
    flam_df_columns = flam_df_start.columns.tolist()
    return flam_df_columns
