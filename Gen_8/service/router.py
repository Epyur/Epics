import math
import os
import traceback
import numpy as np
import pandas as pd
from numpy import empty

from .email import email
from .getmail import GetMail
from .saver import *
from .def_lib import *
from .tdt import *
from .comb import *
from .ignition import ptp_indicator
from .indicators import *
from .tg import tg_message


def process_input_value(x, check_list):
    ch_list = check_list
    counter_x = 0
    counter_x += 1
    message = []

    if x == 0:
        message.append("До свидания!")
        exit()
    else:
        try:
            df_start = TakeDfFormExcel(sbd, '№ заявки', [x])
            # Создаем первый датафрейм заявки
            try:
                all_column_index = df_start.columns

                if not os.path.exists(os.path.join('.', 'out', str(x))):
                    # Если директория не существует, создаём её
                    os.makedirs(os.path.join('.', 'out', str(x)))

                else:
                    pass

                # Проверяем, наличие строки записи заявки

                if 0 in df_start['series_num'].values or 101 in df_start['series_num'].values:
                    pass
                else:
                    inc_id = df_start.loc[df_start['series_num'] == 1, 'task_teg'].iloc[0]
                    try:
                        inc_id1 = inc_id.split(',')
                        inc_id_di = int(inc_id1[0])
                    except:
                        inc_id_di = int(inc_id)
                    print(inc_id)
                    # if
                    df_start_2 = TakeDfFormExcel(sbd, 'ID', [inc_id_di])

                    df_start_2.at[0, 'ID'] = int(x)
                    df_start = pd.concat([df_start_2, df_start], ignore_index=True)


                if isinstance(df_start, pd.DataFrame): # проверяем, что получен действительно датафрейм
                    pass
                if df_start.empty: # проверяем, что датафрейм не пустой
                    message.append('Записи не найдены!')
                    exit()
                else:
                    pass
            except Exception as e:
                message.append(f"Ошибка 0: {(x, e)}")
            # меняем формат даты
            for col in df_start.columns:
                if df_start[col].isna().any():
                    df_start[col] = df_start[col].astype('object')
            date_columns = ['date_of_end', 'sampels_in_date', 'exp_date',
                            'flam_date_material_in', 'flam_exp_date']
            df_start = convert_date_format(df_start, date_columns)

            # проверяем, есть ли в ДФ испытания без заявки, если да, то выделяем строку заявки и строку испытания. Если нет,
            # то идем дальше
            try:
                if 101 in df_start['series_num'].values:
                    column_list = all_column_index.tolist()
                    print(column_list)
                    old_row_remove = ['amb_temp',	'amb_pres',	'amb_moist', 'report_date',	'inventor',	'sampels_in_date',	'exp_date',
                                   'tp1_smog',	'time_of_tp1',	'tp2_smog',	'time_of_tp2',	'tp3_smog',	'time_of_tp3', 'tp4_smog',
                                   'time_of_tp4', 'temp_of_smog', 'temp_of_smog_group',	'temp_of_smog_compare',	'time_of_max_temp',
                                   'mean_len_exp',	'mean_len_group', 'mean_len_compare', 'mass_before', 'mass_after', 'mass_loss',
                                   'mass_loss_group', 'mass_loss_group_compare', 'combustion_time',	'burning_drops', 'substrate',
                                   'mounting_method', 'start_time',	'photo_before',	'photo_after', 'additional_inf', 'link_to_file',
                                   'flam_rep_date',	'flam_inventor', 'flam_date_material_in', 'flam_exp_date',	'flam_report',
                                   'flam_subst', 'flam_fixation', 'flam_flow_density', 'flam_ignition', 'flam_time',
                                   'flam_additional_inf']
                    new_row_remove = ['place', 'budget', 'expense_item', 'matching_agent', 'matching_agent_mail']
                    df_gen = split_row(df_start, column_list, old_row_remove, new_row_remove)

                else:
                    df_gen = df_start
            except Exception as e:
                print(f'Ошибка 1: {(x, e)}')
                df_gen = df_start
                df_gen = df_gen.replace('NaN', np.nan)

            # print(df_star)
            # проверяем ЕКН и информацию по материалу
            try:
                print(df_gen.at[0, 'ekn'])
                if math.isnan(df_gen.at[0, 'ekn']):
                    mat_name = df_gen.at[0, 'product_name']
                    mat_name_list = mat_name.split(',')
                    # print(mat_name)
                    ekn = int(mat_name_list[-1])
                    # print(ekn)
                    df_gen.at[0, 'ekn'] = ekn
                else:
                    ekn = int(df_gen.loc[df_gen['series_num'] == 0, 'ekn'].iloc[0])
                # print(ekn)
                ekn_column_list = ['product_name', 'color', 'sto', 'short_discr',
                                   'producer', 'thickness', 'comb_indicator', 'flam_indicator',
                                   'prop_indicator']
                df_plus_ekn = DfFiller(ekn_book, df_gen, 'ekn', ekn,
                                       'series_num', 0, ekn_column_list, x)
                df_gen = df_plus_ekn

            except Exception as e:
                message.append(f'Ошибка 2: ЕКН указан не верно, либо не введен ({(x, e)})')
                print(f'Ошибка 2: ЕКН указан не верно, либо не введен ({(x, e)})')

            # собираем информацию о заказчике
            try:
                cust_column_list = ['company_name',	'requesits', 'name_of_cust', 'tel', 'sbe', 'ind']
                cust_mail = df_gen.loc[df_gen['series_num'] == 0, 'cust_mail'].iloc[0]
                df_plus_ekn_cust = DfFiller(cus_book, df_gen, 'cust_mail', cust_mail,
                                       'series_num', 0, cust_column_list, x)
                df_gen = df_plus_ekn_cust

            except Exception as e:
                print(f'Ошибка 3: информация о заказчике не найдена ({(x, e)})')

            # на всякий случай вытаскиваем датафрейм со строкой заявки
            df_inc = df_gen.iloc[[0]].copy()

            # print(df_inc)
            try:
                columns_to_fill = ['ekn', 'product_name', 'color', 'sto', 'short_discr',
                                   'producer', 'thickness', 'comb_indicator', 'flam_indicator',
                                   'prop_indicator', 'idetnity', 'cust_mail', 'name_of_cust', 'date_in',
                                   'requesits', 'tel', 'sbe', 'company_name', 'ind']
                df_gen = SpreadAndFill(df_gen, columns_to_fill)
                try:
                    df_gen['ekn'] = df_gen['ekn'].astype('int')
                except:
                    pass
                try:
                    df_gen['ID'] = df_gen['ID'].astype('int')
                except:
                    pass
                try:
                    df_gen['inc_ID'] = df_gen['inc_ID'].astype('int')
                except:
                    pass
                try:
                    df_gen['series_num'] = df_gen['series_num'].astype('int')
                except:
                    pass
            except:
                pass
            # print(list(df_gen.columns))
            # print(df_gen)
            list_to_fill_amb = ['place', 'amb_temp',	'amb_pres',	'amb_moist', 'inventor', 'sampels_in_date',	'substrate',
                                'mounting_method','exp_date', 'flam_inventor', 
                                'flam_date_material_in', 'flam_exp_date', 'flam_report', 'flam_subst', 'flam_fixation']
            fixated_column_list = ['inc_ID', 'ID', 'series_num', 'report_date', 'flam_rep_date']
            try:

                if not df_gen['mass_before'].isna().all():
                    comb_df = df_gen[df_gen['mass_before'].notna()]
                    comb_df = comb_df.reset_index(drop=True, level=0)
                    try:
                        comb_df = merge_duplicate_rows(comb_df, ['series_num'], fixated_column_list)
                    except:
                        print('Дублирующие записи отсутствуют (горючесть)')                    
                    comb_df = SpreadAndFill(comb_df, list_to_fill_amb)
                    comb_df_list = [comb_df.iloc[i:i+1].reset_index(drop=True, level=0) for i in range(len(comb_df))]
                    print(comb_df_list)
                    comb_df_list_2 = []
                    # print(comb_df)
                    try:
                        mail_client = GetMail(folder='Comb', search='UNSEEN')
                        # Получение и обработка писем
                        messages = mail_client.process_messages()
                    except:
                        pass
                    try:
                        try:
                            for exp_frame in comb_df_list:
                                df_temp = dataframe_tdt(exp_frame, 900, x)
                                comb_df_list_2.append(df_temp)

                            comb_df = pd.concat(comb_df_list_2)
                            comb_df = comb_df.reset_index(drop=True, level=0)
                            # print(comb_df)
                        except Exception as e:
                            print(f'Ошибка 4.1, возможно нет файла термодата для обработки: {(x, e)}')
                            traceback.print_exc()
                            if not comb_df['temp_of_smog'].isna().all():
                                pass
                            else:
                                comb_df = MeanValue(comb_df,  ['tp1_smog', 'tp2_smog', 'tp3_smog', 'tp4_smog'], 'temp_of_smog')

                    except Exception as e:
                        print(f'Ошибка 4.2: Хз, что здесь могло произойти, но вдруг ({(x, e)})')
                    try:
                        comb_df = MeanValue(comb_df, ['Comb_lenth_1', 'Comb_lenth_2', 'Comb_lenth_3', 'Comb_lenth_4'], 'mean_len_exp')
                    except Exception as e:
                        print(f'Ошибка 4.3: Проверьте значения повреждений по длине ({(x, e)})')

                    # рассчитываем потерю массы
                    try:
                        comb_df['mass_loss'] = abs((comb_df['mass_after'] - comb_df['mass_before']) * 100 / comb_df['mass_before'])
                        comb_df['mass_loss'] = comb_df['mass_loss'].round(2)
                    except Exception as e:
                        print(f'Ошибка 4.4: Проверьте значение введенных масс, особенно массы до эксперимента ({(x, e)})')

                    # we are making new dataframe for the sum row and fill it with basic data
                    try:
                        df_com_sum = pd.DataFrame(columns=all_column_index)
                        df_com_sum.at[0, 'series_num'] = 102
                        df_com_sum.at[0, 'aim_indicator'] = 'Группа горючести'
                        df_com_sum.at[0, 'ID'] = x
                        list_for_mean = ['temp_of_smog', 'mean_len_exp', 'mass_loss', 'combustion_time']
                        for i_t in list_for_mean:
                            i_t_m = comb_df[i_t].mean().round(2)
                            df_com_sum.at[0, i_t] = i_t_m
                        if 'Да' in comb_df['burning_drops'].values:
                            df_com_sum.at[0, 'burning_drops'] = 'Да'
                        else:
                            df_com_sum.at[0, 'burning_drops'] = 'Нет'
                        df_com_sum.at[0, 'ind'] = df_inc.at[0, 'ind']

                    except Exception as e:
                        print(f'Ошибка 4.5: не получилось создать и заполнить новый фрейм для итоговых результатов испытаний '
                              f'на горючесть ({(x, e)})')

                    # add new df to comb_df
                    try:
                        comb_df = pd.concat([comb_df, df_com_sum], ignore_index=True)
                        # print(comb_df)
                    except Exception as e:
                        print(f'Ошибка 4.6: Ошибка объединения фреймов ({(x, e)})')

                    # start to check a comb indicators and a matching
                    try:
                        comb_indicator = comb_df.at[0, 'comb_indicator']
                        for i_t_v in range(0,len(comb_df)):
                            i_t_v_g = comb_df.at[i_t_v, 'temp_of_smog']
                            comb_df.at[i_t_v, 'temp_of_smog_group'] = smog_indicator(i_t_v_g)
                            i_t_v_l = comb_df.at[i_t_v, 'mean_len_exp']
                            comb_df.at[i_t_v, 'mean_len_group'] = length_indicator(i_t_v_l)
                            i_t_v_m = comb_df.at[i_t_v, 'mass_loss']
                            comb_df.at[i_t_v, 'mass_loss_group'] = mass_indicator(i_t_v_m)
                            i_t_v_c = comb_df.at[i_t_v, 'combustion_time']
                            comb_df.at[i_t_v, 'combustion_time_group'] = time_indicator(i_t_v_c)
                            i_t_v_d = comb_df.at[i_t_v, 'burning_drops']
                            comb_df.at[i_t_v, 'burning_drops_group'] = burning_drops_group(i_t_v_d)
                    except:
                        print(f'Ошибка 4.7: {(x, e)}')

                    # собираем общую оценку
                    try:
                        comb_indicator_list = ['temp_of_smog_group', 'mean_len_group', 'mass_loss_group', 'combustion_time_group',
                                               'burning_drops_group']
                        comb_indicator_l = []
                        for index_f in range(0,len(comb_df)):
                            for i_c in comb_indicator_list:
                                i_c_g = comb_df.at[index_f, i_c]
                                comb_indicator_l.append(i_c_g)
                            max_i_c_g = FindeWorsest('Г', comb_indicator_l)
                            comb_df.at[index_f, 'gen_indicator'] = max_i_c_g
                            comb_indicator_l = []
                    except Exception as e:
                        print(f'Ошибка 4.8: {(x, e)}')

                    # matching
                    try:
                        match_list = ['temp_of_smog_group', 'mean_len_group', 'mass_loss_group', 'combustion_time_group',
                                               'burning_drops_group', 'gen_indicator']
                        match_list_aim = ['temp_of_smog_compare', 'mean_len_compare', 'mass_loss_group_compare',
                                          'combustion_time_group_compare', 'burning_drops_group_compare', 'matching']
                        for index_f in range(0,len(comb_df)):
                            for i_m in range(len(match_list)):
                                i_m_m = match_list[i_m]
                                i_m_a = match_list_aim[i_m]
                                i_m_v = comb_df.at[index_f, i_m_m]
                                comb_df.at[index_f, i_m_a] = group_compare('Г', comb_indicator, i_m_v)
                    except Exception as e:
                        print(f'Ошибка 4.9: {(x, e)}')

                    # df_gen = pd.concat([df_inc, comb_df], ignore_index=True)

                    try:
                        comb_df_d = comb_df.copy()
                        float_list = ['thickness', 'start_temp', 'tp1_smog',  'time_of_tp1', 'tp2_smog',  'time_of_tp2', 'tp3_smog',
                                      'time_of_tp3', 'tp4_smog',  'time_of_tp4', 'temp_of_smog']
                        for it_d in range(0, len(comb_df_d)):
                            it_d_v = round(float(comb_df_d.at[it_d, 'mass_loss']), 1)
                            comb_df_d.at[it_d, 'mass_loss'] = it_d_v

                        # for floa in float_list:
                        #     comb_df_d[floa] = comb_df_d[floa].astype('float')
                        print(comb_df_d.at[0, 'photo_before'])
                        report_to_word(comb_df_d, doc_templ, x, 'g')

                    except Exception as e:
                        print(f'Ошибка 4.10: {(x, e)}')

                    try:
                        ident = comb_df_d.at[0, 'idetnity']
                        matname = comb_df_d.at[0, 'product_name']
                        theme = f'{ident}|{matname} (LPIZAYAVKINAPRO-{x})'
                        email_text = (f'Настоящим сообщаем, что заявка на проведение испытаний материала {matname} c '
                                      f'идентификатором "{ident}" выполнена в отношении показателя "Группа горючести".\n'
                                      f'Установленная группа горючести: {max_i_c_g}')
                        file_path_to_email = os.path.abspath(os.path.join('.', 'out', str(x), str(x) + "g.docx"))
                        file_name = str(x) + "g.docx"
                        if 'a1' in ch_list:
                            email(theme, email_text, file_path_to_email, file_name, 'shoya.vs@tn.ru')
                        if 'a2' in ch_list:
                            tg_text = theme + '\n\n' + email_text
                            tg_message(tg_text, '10', file_path_to_email)
                        if 'a3' in ch_list:
                            email_text = email_text + '\n\n\n\n\n\n end point'
                            email(theme, email_text, file_path_to_email, file_name, 'lpi@tracker.tn.ru')
                    except Exception as e:
                        print(f'почта не отправлена: {e}')


                else:
                    message.append('Результаты испытания на группу горючести отсутствуют в СБД.')
                    print('Nfrjq pfgbcb ytn')



            except Exception as e:
                message.append(f'Ошибка 4. Ошибка при формировании таблицы результатов испытаний на горючесть: {x, e}.')
            
            # print(df_gen)


            # обрабатываем воспламеняемость
            if not df_gen['flam_ignition'].isna().all():
                flam_df = df_gen[df_gen['flam_ignition'].notna()]
                flam_df = flam_df.reset_index(drop=True, level=0)
                # print(flam_df)
                try:                    
                    flam_df = merge_duplicate_rows(flam_df, ['series_num'], fixated_column_list)
                except:
                    print('Дублирующие записи отсутствуют')
                try:
                    flam_df = SpreadAndFill(flam_df, list_to_fill_amb)
                except Exception as e:
                    print(f'Ошибка заполнения условий окружающей среды (воспламеняемость): {e}')
                # comb_df_list = [comb_df.iloc[i:i+1].reset_index(drop=True, level=0) for i in range(len(comb_df))]
                # print('мЫ сюда вошли')
                try:
                    # создаем пустой дф для итоговой строки воспламеняемости

                    try:
                        df_flam_sum = pd.DataFrame(columns=all_column_index)
                        df_flam_sum.at[0, 'series_num'] = 103
                        df_flam_sum.at[0, 'aim_indicator'] = 'Группа воспламеняемости'
                        df_flam_sum.at[0, 'ID'] = x
                        min_value_flam = df_gen.loc[df_gen['flam_ignition'] == 'Да', 'flam_flow_density'].min()
                        df_flam_sum.at[0, 'flam_flow_density'] = min_value_flam
                        df_flam_sum.at[0, 'ind'] = df_inc.at[0, 'ind']
                    except Exception as e:
                        print(f'Ошибка 5.1: {(x, e)}')

                    try:
                        flam_indicator = df_gen.at[0, 'flam_indicator']
                        flam_indicator_real = ptp_indicator(min_value_flam)
                        df_flam_sum.at[0, 'flam_group'] = flam_indicator_real
                        df_flam_sum.at[0, 'flam_group_comprasion'] = group_compare('В', flam_indicator, flam_indicator_real)
                    except Exception as e:
                        print(f'Ошибка 5.2: {(x, e)}')

                    df_flam = pd.concat([flam_df, df_flam_sum], ignore_index=True)
                    try:
                        flam_df_d = df_flam.copy()
                        # flam_df_d['thickness'] = flam_df_d['thickness'].astype('float')
                        flam_df_d['flam_flow_density'] = flam_df_d['flam_flow_density'].astype('int')
                        int_list = ['flam_flow_density', 'flam_time']
                        for i in range(0, len(flam_df_d)):
                            try:
                                flam_df_d.at[i, 'flam_time'] = int(flam_df_d.at[i, 'flam_time'])
                            except:
                                pass

                        report_to_word(flam_df_d, doc_templ_v, x, 'v')

                    except Exception as e:
                        print(f'Ошибка 5.3: {(x, e)}')

                    try:
                        ident = flam_df_d.at[0, 'idetnity']
                        matname = flam_df_d.at[0, 'product_name']
                        theme = f'{ident}|{matname} (LPIZAYAVKINAPRO-{x})'
                        email_text = (f'Настоящим сообщаем, что заявка на проведение испытаний материала {matname} c '
                                      f'идентификатором "{ident}" выполнена в отношении показателя "Группа воспламеняемости".\n'
                                      f'Установленная критическая плотность теплового потока (кВт/м\u00b2): {int(min_value_flam)}\n'
                                      f'Установленная группа воспламеняемости: {flam_indicator_real}')
                        file_path_to_email = os.path.abspath(os.path.join('.', 'out', str(x), str(x) + "v"+".docx"))
                        file_name = str(x) + "v.docx"
                        if 'a4' in ch_list:
                            email(theme, email_text, file_path_to_email, file_name, 'shoya.vs@tn.ru')
                        if 'a5' in ch_list:
                            tg_text = theme + '\n\n' + email_text
                            tg_message(tg_text, '12', file_path_to_email)
                        if 'a3' in ch_list:
                            email_text = email_text + '\n\n\n\n\n\n end point'
                            email(theme, email_text, file_path_to_email, file_name, 'lpi@tracker.tn.ru')
                    except Exception as e:
                        print(f'почта не отправлена: {e}')
                except Exception as e:
                    message.append(f'Ошибка 5. Ошибка при формировании таблицы результатов испытаний на воспламеняемость: {e}.')


            else:
                print('Результаты оценки воспламеняемости отсутствуют')
            
            df_gen = df_inc.copy()

            try:
                df_gen = pd.concat([df_gen, comb_df], ignore_index=True)
            except Exception as e:
                print('Нет данных горючести')
                             
            try:
                df_gen = pd.concat([df_gen, df_flam], ignore_index=True)                
            except Exception as e:
                print('Нет данных воспламеняемости')


            
            # print('We are there')

            try:
                df_gen = DictTitlesRename(df_gen, in_title, 'val', 'val2')
                ds = report_to_excel(df_gen, x)

            except Exception as e:
                print(f'ошибка записи файла: {e}')
        except Exception as e:
            print(f'Ошибка Ошибка {e}')
        return message

