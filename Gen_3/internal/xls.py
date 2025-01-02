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
#
# # ------------! РАЗБИРАЕМ книгу результатов испытаний на воспламеняемость ! -----------------
# flam_df_start = pd.read_excel(flam_book)
# flam_df_columns = flam_df_start.columns.tolist()
# flam_df = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id', 'Date_in': 'flam_report_date', 'ID_in': 'ID', 'ext lab': 'flam_lab', 'inventor': 'flam_investigator', 'day inc prod': 'flam_date_of_product_coming', 'dayX': 'flam_date_of_exp', 'link to report': 'flam_report_link', 'type of osn': 'flam_type_of_osn', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux', 'Факт воспламенения': 'flam', 'Время воспламенения': 'flam_time', 'dop inf': 'flam_dop_inf', '№ образца': 'exp_num'})
# flam_df_columns_new = flam_df.columns.tolist()
# amb_df_flam = amb_df_start.rename(columns = {'Дата': 'flam_date_of_exp', 'Температура': 'flam_amb_temp', 'Давление': 'flam_amb_presue', 'Влажность': 'flam_amb_moist', 'Lab': 'flam_lab'})
# flam_df_merged = flam_df.merge(amb_df_flam, how='left', on=["flam_date_of_exp", "flam_lab"])
# flam_df_ser1 = flam_df_merged.loc[flam_df_merged['exp_num'] == 1].copy()
# flam_name_1 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_1', 'Date_in': 'flam_report_date_1', 'ID_in': 'ID', 'ext lab': 'flam_lab_1', 'inventor': 'flam_investigator_1', 'day inc prod': 'flam_date_of_product_coming_1', 'dayX': 'flam_date_of_exp_1', 'link to report': 'flam_report_link_1', 'type of osn': 'flam_type_of_osn_1', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_1', 'Факт воспламенения': 'flam_1', 'Время воспламенения': 'flam_time_1', 'dop inf': 'flam_dop_inf_1', '№ образца': 'exp_num_1'})
# flam_df_ser2 = flam_df_merged.loc[flam_df_merged['exp_num'] == 2].copy()
# flam_name_2 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_2', 'Date_in': 'flam_report_date_2', 'ID_in': 'ID', 'ext lab': 'flam_lab_2', 'inventor': 'flam_investigator_2', 'day inc prod': 'flam_date_of_product_coming_2', 'dayX': 'flam_date_of_exp_2', 'link to report': 'flam_report_link_2', 'type of osn': 'flam_type_of_osn_2', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_2', 'Факт воспламенения': 'flam_2', 'Время воспламенения': 'flam_time_2', 'dop inf': 'flam_dop_inf_2', '№ образца': 'exp_num_2'})
# flam_df_ser3 = flam_df_merged.loc[flam_df_merged['exp_num'] == 3].copy()
# flam_name_3 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_3', 'Date_in': 'flam_report_date_3', 'ID_in': 'ID', 'ext lab': 'flam_lab_3', 'inventor': 'flam_investigator_3', 'day inc prod': 'flam_date_of_product_coming_3', 'dayX': 'flam_date_of_exp_3', 'link to report': 'flam_report_link_3', 'type of osn': 'flam_type_of_osn_3', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_3', 'Факт воспламенения': 'flam_2', 'Время воспламенения': 'flam_time_3', 'dop inf': 'flam_dop_inf_3', '№ образца': 'exp_num_3'})
# flam_df_ser4 = flam_df_merged.loc[flam_df_merged['exp_num'] == 4].copy()
# flam_name_4 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_4', 'Date_in': 'flam_report_date_4', 'ID_in': 'ID', 'ext lab': 'flam_lab_4', 'inventor': 'flam_investigator_4', 'day inc prod': 'flam_date_of_product_coming_4', 'dayX': 'flam_date_of_exp_4', 'link to report': 'flam_report_link_4', 'type of osn': 'flam_type_of_osn_4', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_4', 'Факт воспламенения': 'flam_4', 'Время воспламенения': 'flam_time_4', 'dop inf': 'flam_dop_inf_4', '№ образца': 'exp_num_4'})
# flam_df_ser5 = flam_df_merged.loc[flam_df_merged['exp_num'] == 5].copy()
# flam_name_5 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_5', 'Date_in': 'flam_report_date_5', 'ID_in': 'ID', 'ext lab': 'flam_lab_5', 'inventor': 'flam_investigator_5', 'day inc prod': 'flam_date_of_product_coming_5', 'dayX': 'flam_date_of_exp_5', 'link to report': 'flam_report_link_5', 'type of osn': 'flam_type_of_osn_5', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_5', 'Факт воспламенения': 'flam_5', 'Время воспламенения': 'flam_time_5', 'dop inf': 'flam_dop_inf_5', '№ образца': 'exp_num_5'})
# flam_df_ser6 = flam_df_merged.loc[flam_df_merged['exp_num'] == 6].copy()
# flam_name_6 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_6', 'Date_in': 'flam_report_date_6', 'ID_in': 'ID', 'ext lab': 'flam_lab_6', 'inventor': 'flam_investigator_6', 'day inc prod': 'flam_date_of_product_coming_6', 'dayX': 'flam_date_of_exp_6', 'link to report': 'flam_report_link_6', 'type of osn': 'flam_type_of_osn_6', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_6', 'Факт воспламенения': 'flam_6', 'Время воспламенения': 'flam_time_6', 'dop inf': 'flam_dop_inf_6', '№ образца': 'exp_num_6'})
# flam_df_ser7 = flam_df_merged.loc[flam_df_merged['exp_num'] == 7].copy()
# flam_name_7 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_7', 'Date_in': 'flam_report_date_7', 'ID_in': 'ID', 'ext lab': 'flam_lab_7', 'inventor': 'flam_investigator_7', 'day inc prod': 'flam_date_of_product_coming_7', 'dayX': 'flam_date_of_exp_7', 'link to report': 'flam_report_link_7', 'type of osn': 'flam_type_of_osn_7', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_7', 'Факт воспламенения': 'flam_7', 'Время воспламенения': 'flam_time_7', 'dop inf': 'flam_dop_inf_7', '№ образца': 'exp_num_7'})
# flam_df_ser8 = flam_df_merged.loc[flam_df_merged['exp_num'] == 8].copy()
# flam_name_8 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_8', 'Date_in': 'flam_report_date_8', 'ID_in': 'ID', 'ext lab': 'flam_lab_8', 'inventor': 'flam_investigator_8', 'day inc prod': 'flam_date_of_product_coming_8', 'dayX': 'flam_date_of_exp_8', 'link to report': 'flam_report_link_8', 'type of osn': 'flam_type_of_osn_8', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_8', 'Факт воспламенения': 'flam_8', 'Время воспламенения': 'flam_time_8', 'dop inf': 'flam_dop_inf_8', '№ образца': 'exp_num_8'})
# flam_df_ser9 = flam_df_merged.loc[flam_df_merged['exp_num'] == 9].copy()
# flam_name_9 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_9', 'Date_in': 'flam_report_date_9', 'ID_in': 'ID', 'ext lab': 'flam_lab_9', 'inventor': 'flam_investigator_9', 'day inc prod': 'flam_date_of_product_coming_9', 'dayX': 'flam_date_of_exp_9', 'link to report': 'flam_report_link_9', 'type of osn': 'flam_type_of_osn_9', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_9', 'Факт воспламенения': 'flam_9', 'Время воспламенения': 'flam_time_9', 'dop inf': 'flam_dop_inf_9', '№ образца': 'exp_num_9'})
# flam_df_ser10 = flam_df_merged.loc[flam_df_merged['exp_num'] == 10].copy()
# flam_name_10 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_10', 'Date_in': 'flam_report_date_10', 'ID_in': 'ID', 'ext lab': 'flam_lab_10', 'inventor': 'flam_investigator_10', 'day inc prod': 'flam_date_of_product_coming_10', 'dayX': 'flam_date_of_exp_10', 'link to report': 'flam_report_link_10', 'type of osn': 'flam_type_of_osn_10', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_10', 'Факт воспламенения': 'flam_10', 'Время воспламенения': 'flam_time_10', 'dop inf': 'flam_dop_inf_10', '№ образца': 'exp_num_10'})
# flam_df_ser11 = flam_df_merged.loc[flam_df_merged['exp_num'] == 11].copy()
# flam_name_11 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_11', 'Date_in': 'flam_report_date_11', 'ID_in': 'ID', 'ext lab': 'flam_lab_11', 'inventor': 'flam_investigator_11', 'day inc prod': 'flam_date_of_product_coming_11', 'dayX': 'flam_date_of_exp_11', 'link to report': 'flam_report_link_11', 'type of osn': 'flam_type_of_osn_11', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_11', 'Факт воспламенения': 'flam_11', 'Время воспламенения': 'flam_time_11', 'dop inf': 'flam_dop_inf_11', '№ образца': 'exp_num_11'})
# flam_df_ser12 = flam_df_merged.loc[flam_df_merged['exp_num'] == 12].copy()
# flam_name_12 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_12', 'Date_in': 'flam_report_date_12', 'ID_in': 'ID', 'ext lab': 'flam_lab_12', 'inventor': 'flam_investigator_12', 'day inc prod': 'flam_date_of_product_coming_12', 'dayX': 'flam_date_of_exp_12', 'link to report': 'flam_report_link_12', 'type of osn': 'flam_type_of_osn_12', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_12', 'Факт воспламенения': 'flam_12', 'Время воспламенения': 'flam_time_12', 'dop inf': 'flam_dop_inf_12', '№ образца': 'exp_num_12'})
# flam_df_ser13 = flam_df_merged.loc[flam_df_merged['exp_num'] == 13].copy()
# flam_name_13 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_13', 'Date_in': 'flam_report_date_13', 'ID_in': 'ID', 'ext lab': 'flam_lab_13', 'inventor': 'flam_investigator_13', 'day inc prod': 'flam_date_of_product_coming_13', 'dayX': 'flam_date_of_exp_13', 'link to report': 'flam_report_link_13', 'type of osn': 'flam_type_of_osn_13', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_13', 'Факт воспламенения': 'flam_13', 'Время воспламенения': 'flam_time_13', 'dop inf': 'flam_dop_inf_13', '№ образца': 'exp_num_13'})
# flam_df_ser14 = flam_df_merged.loc[flam_df_merged['exp_num'] == 14].copy()
# flam_name_14 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_14', 'Date_in': 'flam_report_date_14', 'ID_in': 'ID', 'ext lab': 'flam_lab_14', 'inventor': 'flam_investigator_14', 'day inc prod': 'flam_date_of_product_coming_14', 'dayX': 'flam_date_of_exp_14', 'link to report': 'flam_report_link_14', 'type of osn': 'flam_type_of_osn_14', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_14', 'Факт воспламенения': 'flam_14', 'Время воспламенения': 'flam_time_14', 'dop inf': 'flam_dop_inf_14', '№ образца': 'exp_num_14'})
# flam_df_ser15 = flam_df_merged.loc[flam_df_merged['exp_num'] == 15].copy()
# flam_name_15 = flam_df_start.rename(columns = {'ID_Out': 'flam_report_id_15', 'Date_in': 'flam_report_date_15', 'ID_in': 'ID', 'ext lab': 'flam_lab_15', 'inventor': 'flam_investigator_15', 'day inc prod': 'flam_date_of_product_coming_15', 'dayX': 'flam_date_of_exp_15', 'link to report': 'flam_report_link_15', 'type of osn': 'flam_type_of_osn_15', 'Плотность теплового потока, Вт/м2': 'flam_density_of_heat_flux_15', 'Факт воспламенения': 'flam_15', 'Время воспламенения': 'flam_time_15', 'dop inf': 'flam_dop_inf_15', '№ образца': 'exp_num_15'})
# flam_df_2 =  flam_name_1.merge(flam_name_2, how='left', on=["ID"])
# flam_df_3 =  flam_df_2.merge(flam_name_3, how='left', on=["ID"])
# flam_df_4 =  flam_df_3.merge(flam_name_4, how='left', on=["ID"])
# flam_df_gen =  flam_df_4.merge(flam_name_5, how='left', on=["ID"])
#flam_df_6 =  flam_df_5.merge(flam_name_6, how='left', on=["ID"])
#flam_df_gen =  flam_df_6.merge(flam_name_7, how='left', on=["ID"])
# flam_df_8 =  flam_df_7.merge(flam_name_8, how='left', on=["ID"])
# flam_df_9 =  flam_df_8.merge(flam_name_9, how='left', on=["ID"])
# flam_df_10 =  flam_df_9.merge(flam_name_10, how='left', on=["ID"])
# flam_df_11 =  flam_df_10.merge(flam_name_11, how='left', on=["ID"])
# flam_df_12 =  flam_df_11.merge(flam_name_12, how='left', on=["ID"])
# flam_df_13 =  flam_df_12.merge(flam_name_13, how='left', on=["ID"])
# flam_df_14 =  flam_df_13.merge(flam_name_14, how='left', on=["ID"])
# flam_df_gen =  flam_df_14.merge(flam_name_15, how='left', on=["ID"])
# flam_df_gen['critical_density_of_heat_flux'] = np.nan
# flam_df_gen['group_of_flam'] = np.nan
