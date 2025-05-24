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


def process_input_value(x, check_list, chat_id, message_thread_id):
    ch_list = check_list
    counter_x = 0
    counter_x += 1
    message = []
    try:
        folder_list = ['Comb', 'Flam']
        for i in folder_list:
            mail_client = GetMail(folder=i, search='UNSEEN')
            # Получение и обработка писем
            messages = mail_client.process_messages()
            mail_client.save_to_excel(sbd)
    except:
        pass

    if x == 0:
        message.append("До свидания!")
        exit()
    else:
        try:
            df_start = TakeDfFormExcel(sbd, ns[8], [x])
            # Создаем первый датафрейм заявки
            try:
                all_column_index = df_start.columns

                if not os.path.exists(os.path.join('.', 'out', str(x))):
                    # Если директория не существует, создаём её
                    os.makedirs(os.path.join('.', 'out', str(x)))

                else:
                    pass

                # Проверяем, наличие строки записи заявки

                if 0 in df_start[ns[9]].values or 101 in df_start[ns[9]].values:
                    pass
                else:
                    inc_id = df_start.loc[df_start[ns[9]] == 1, ns[5]].iloc[0]
                    try:
                        inc_id1 = inc_id.split(',')
                        inc_id_di = int(inc_id1[0])
                    except:
                        inc_id_di = int(inc_id)

                    # if
                    df_start_2 = TakeDfFormExcel(sbd, ns[7], [inc_id_di])

                    df_start_2.at[0, ns[8]] = int(x)
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
            date_columns = [ns[4], ns[32], ns[33], ns[76], ns[77]]
            df_start = convert_date_format(df_start, date_columns)

            # проверяем, есть ли в ДФ испытания без заявки, если да, то выделяем строку заявки и строку испытания. Если нет,
            # то идем дальше
            try:
                if 101 in df_start[ns[9]].values:
                    column_list = all_column_index.tolist()
                    print(column_list)
                    old_row_remove = [ns[27], ns[28], ns[29], ns[30], ns[31], ns[32], ns[33],
                                   ns[35], ns[36], ns[37], ns[38], ns[39], ns[40], ns[41], ns[42], ns[43], ns[44], ns[45], ns[46],
                                   ns[51], ns[52], ns[53], ns[54], ns[55], ns[56], ns[57], ns[58], ns[59], ns[62], ns[67],
                                   ns[68], ns[69], ns[70], ns[71], ns[72], ns[73], ns[74], ns[75], ns[76], ns[77], ns[78],
                                   ns[79], ns[80], ns[81], ns[82], ns[83], ns[86]]
                    new_row_remove = [ns[12], ns[89], ns[90], ns[91], ns[92]]
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
                print(df_gen.at[0, ns[14]])
                try:
                    if math.isnan(df_gen.at[0, ns[15]]):
                        mat_name = df_gen.at[0, ns[14]]
                        mat_name_list = mat_name.split(',')# print(mat_name)
                        ekn = int(mat_name_list[-1])
                        # print(ekn)
                        df_gen.at[0, ns[14]] = ekn
                except:
                    ekn = int(df_gen.loc[df_gen[ns[9]] == 0, ns[14]].iloc[0])

                # print(ekn)
                ekn_column_list = [ns[15], ns[16], ns[17], ns[18], ns[19], ns[22], ns[23], ns[24], ns[25]]
                df_plus_ekn = DfFiller(ekn_book, df_gen, ns[14], ekn, ns[9], 0, ekn_column_list, x)
                df_gen = df_plus_ekn

            except Exception as e:
                message.append(f'Ошибка 2: ЕКН указан не верно, либо не введен ({(x, e)})')
                print(f'Ошибка 2: ЕКН указан не верно, либо не введен ({(x, e)})')

            # собираем информацию о заказчике
            try:
                cust_column_list = [ns[93],	ns[94], ns[11], ns[95], ns[96], ns[97]]
                cust_mail = df_gen.loc[df_gen[ns[9]] == 0, ns[10]].iloc[0]
                df_plus_ekn_cust = DfFiller(cus_book, df_gen, ns[10], cust_mail,
                                       ns[9], 0, cust_column_list, x)
                df_gen = df_plus_ekn_cust

            except Exception as e:
                print(f'Ошибка 3: информация о заказчике не найдена ({(x, e)})')

            # на всякий случай вытаскиваем датафрейм со строкой заявки
            df_inc = df_gen.iloc[[0]].copy()

            # print(df_inc)
            try:
                columns_to_fill = [ns[14], ns[15], ns[16], ns[17], ns[18], ns[19], ns[22], ns[23], ns[24],
                                   ns[25], ns[13], ns[10], ns[11], ns[3], ns[94], ns[95], ns[96], ns[93], ns[97]]
                df_gen = SpreadAndFill(df_gen, columns_to_fill)
                try:
                    df_gen[ns[14]] = df_gen[ns[14]].astype('int')
                except:
                    pass
                try:
                    df_gen[ns[8]] = df_gen[ns[8]].astype('int')
                except:
                    pass
                try:
                    df_gen[ns[7]] = df_gen[ns[7]].astype('int')
                except:
                    pass
                try:
                    df_gen[ns[9]] = df_gen[ns[9]].astype('int')
                except:
                    pass
            except:
                pass
            # print(list(df_gen.columns))
            # print(df_gen)
            list_to_fill_amb = [ns[12], ns[27], ns[28], ns[29], ns[31], ns[32], ns[67],
                                ns[68], ns[33], ns[75], ns[76], ns[77], ns[78], ns[79], ns[80]]
            fixated_column_list = [ns[7], ns[8], ns[9], ns[30], ns[74]]
            try:
                print('we are go in ')
                if not df_gen[ns[54]].isna().all():
                    print('tre there')
                    comb_df = df_gen[df_gen[ns[54]].notna()]
                    comb_df = comb_df.reset_index(drop=True, level=0)
                    try:
                        comb_df = merge_duplicate_rows(comb_df, [ns[9]], fixated_column_list)
                    except:
                        print('Дублирующие записи отсутствуют (горючесть)')
                    print('we are go on')
                    comb_df = SpreadAndFill(comb_df, list_to_fill_amb)
                    comb_df_list = [comb_df.iloc[i:i+1].reset_index(drop=True, level=0) for i in range(len(comb_df))]
                    print(comb_df_list)
                    comb_df_list_2 = []
                    # print(comb_df)

                    try:
                        try:
                            for exp_frame in comb_df_list:
                                df_temp = dataframe_tdt(exp_frame, 700, x)
                                comb_df_list_2.append(df_temp)

                            comb_df = pd.concat(comb_df_list_2)
                            comb_df = comb_df.reset_index(drop=True, level=0)
                            # print(comb_df)
                        except Exception as e:
                            print(f'Ошибка 4.1, возможно нет файла термодата для обработки: {(x, e)}')
                            traceback.print_exc()
                            if not comb_df[ns[43]].isna().all():
                                pass
                            else:
                                comb_df = MeanValue(comb_df,  [ns[35], ns[37], ns[39], ns[41]], ns[43])

                    except Exception as e:
                        print(f'Ошибка 4.2: Хз, что здесь могло произойти, но вдруг ({(x, e)})')
                    try:
                        comb_df = MeanValue(comb_df, [ns[47], ns[48], ns[49], ns[50]], ns[51])
                    except Exception as e:
                        print(f'Ошибка 4.3: Проверьте значения повреждений по длине ({(x, e)})')

                    # рассчитываем потерю массы
                    try:
                        comb_df[ns[56]] = abs((comb_df[ns[55]] - comb_df[ns[54]]) * 100 / comb_df[ns[54]])
                        comb_df[ns[56]] = comb_df[ns[56]].round(2)
                    except Exception as e:
                        print(f'Ошибка 4.4: Проверьте значение введенных масс, особенно массы до эксперимента ({(x, e)})')

                    # we are making new dataframe for the sum row and fill it with basic data
                    try:
                        df_com_sum = pd.DataFrame(columns=all_column_index)
                        df_com_sum.at[0, ns[9]] = 102
                        df_com_sum.at[0, ns[1]] = 'Группа горючести'
                        df_com_sum.at[0, ns[8]] = x
                        list_for_mean = [ns[43], ns[51], ns[56], ns[59]]
                        for i_t in list_for_mean:
                            i_t_m = comb_df[i_t].mean().round(2)
                            df_com_sum.at[0, i_t] = i_t_m
                        if 'Да' in comb_df[ns[62]].values:
                            df_com_sum.at[0, ns[62]] = 'Да'
                        else:
                            df_com_sum.at[0, ns[62]] = 'Нет'
                        df_com_sum.at[0, ns[97]] = df_inc.at[0, ns[97]]


                    except Exception as e:
                        print(f'Ошибка 4.5: не получилось создать и заполнить новый фрейм для итоговых результатов испытаний '
                              f'на горючесть ({(x, e)})')

                    # add new df to comb_df
                    try:
                        comb_df = pd.concat([comb_df, df_com_sum], ignore_index=True)
                        print(comb_df)
                    except Exception as e:
                        print(f'Ошибка 4.6: Ошибка объединения фреймов ({(x, e)})')

                    # start to check a comb indicators and a matching
                    try:
                        comb_indicator = comb_df.at[0, ns[23]]
                        for i_t_v in range(0,len(comb_df)):
                            i_t_v_g = comb_df.at[i_t_v, ns[43]]
                            comb_df.at[i_t_v, ns[44]] = smog_indicator(i_t_v_g)
                            i_t_v_l = comb_df.at[i_t_v, ns[51]]
                            comb_df.at[i_t_v, ns[52]] = length_indicator(i_t_v_l)
                            i_t_v_m = comb_df.at[i_t_v, ns[56]]
                            comb_df.at[i_t_v, ns[57]] = mass_indicator(i_t_v_m)
                            i_t_v_c = comb_df.at[i_t_v, ns[59]]
                            comb_df.at[i_t_v, ns[60]] = time_indicator(i_t_v_c)
                            i_t_v_d = comb_df.at[i_t_v, ns[62]]
                            comb_df.at[i_t_v, ns[63]] = burning_drops_group(i_t_v_d)
                    except:
                        print(f'Ошибка 4.7: {(x, e)}')

                    # собираем общую оценку
                    try:
                        comb_indicator_list = [ns[44], ns[52], ns[57], ns[60],
                                               ns[63]]
                        comb_indicator_l = []
                        for index_f in range(0,len(comb_df)):
                            for i_c in comb_indicator_list:
                                i_c_g = comb_df.at[index_f, i_c]
                                comb_indicator_l.append(i_c_g)
                            max_i_c_g = FindeWorsest('Г', comb_indicator_l)
                            comb_df.at[index_f, ns[65]] = max_i_c_g
                            comb_indicator_l = []
                    except Exception as e:
                        print(f'Ошибка 4.8: {(x, e)}')

                    # matching
                    try:
                        match_list = [ns[44], ns[52], ns[57], ns[60], ns[63], ns[65]]
                        match_list_aim = [ns[45], ns[53], ns[58], ns[61], ns[64], ns[66]]
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
                        float_list = [ns[22], ns[69], ns[35], ns[36], ns[37], ns[38], ns[39],	ns[40], ns[41], ns[42], ns[43]]
                        for it_d in range(0, len(comb_df_d)):
                            it_d_v = round(float(comb_df_d.at[it_d, ns[56]]), 1)
                            comb_df_d.at[it_d, ns[56]] = it_d_v

                        # for floa in float_list:
                        #     comb_df_d[floa] = comb_df_d[floa].astype('float')
                        print(comb_df_d.at[0, ns[70]])
                        report_to_word(comb_df_d, doc_templ, x, 'g')

                    except Exception as e:
                        print(f'Ошибка 4.10: {(x, e)}')

                    try:
                        ident = comb_df_d.at[0, ns[13]]
                        matname = comb_df_d.at[0, ns[15]]
                        theme = f'{ident}|{matname} (LPIZAYAVKINAPRO-{x})'
                        email_text = (f'Настоящим сообщаем, что заявка на проведение испытаний материала {matname} c '
                                      f'идентификатором "{ident}" выполнена в отношении показателя "Группа горючести".\n'
                                      f'Установленная группа горючести: {max_i_c_g}')
                        file_path_to_email = os.path.abspath(os.path.join('.', 'out', str(x), str(x) + "g.docx"))
                        file_name = str(x) + "g.docx"
                        if 'a1' in ch_list:
                            email(theme, email_text, file_path_to_email, file_name, 'shoya.vs@tn.ru')
                        if 'a6' in ch_list:
                            tg_text = theme + '\n\n' + email_text
                            tg_message(tg_text, topic_id=message_thread_id, file_path=file_path_to_email, chat_id=chat_id)
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
            if not df_gen[ns[82]].isna().all():
                flam_df = df_gen[df_gen[ns[82]].notna()]
                flam_df = flam_df.reset_index(drop=True, level=0)
                # print(flam_df)
                try:                    
                    flam_df = merge_duplicate_rows(flam_df, [ns[9]], fixated_column_list)
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
                        df_flam_sum.at[0, ns[9]] = 103
                        df_flam_sum.at[0, ns[1]] = 'Группа воспламеняемости'
                        df_flam_sum.at[0, ns[8]] = x
                        min_value_flam = df_gen.loc[df_gen[ns[82]] == 'Да', ns[81]].min()
                        df_flam_sum.at[0, ns[81]] = min_value_flam
                        df_flam_sum.at[0, ns[97]] = df_inc.at[0, ns[97]]
                    except Exception as e:
                        print(f'Ошибка 5.1: {(x, e)}')

                    try:
                        flam_indicator = df_gen.at[0, ns[24]]
                        flam_indicator_real = ptp_indicator(min_value_flam)
                        df_flam_sum.at[0, ns[84]] = flam_indicator_real
                        df_flam_sum.at[0, ns[85]] = group_compare('В', flam_indicator, flam_indicator_real)
                    except Exception as e:
                        print(f'Ошибка 5.2: {(x, e)}')

                    df_flam = pd.concat([flam_df, df_flam_sum], ignore_index=True)
                    try:
                        flam_df_d = df_flam.copy()
                        # flam_df_d[ns[22]] = flam_df_d[ns[22]].astype('float')
                        flam_df_d[ns[81]] = flam_df_d[ns[81]].astype('int')
                        int_list = [ns[81], ns[83]]
                        for i in range(0, len(flam_df_d)):
                            try:
                                flam_df_d.at[i, ns[83]] = int(flam_df_d.at[i, ns[83]])
                            except:
                                pass

                        report_to_word(flam_df_d, doc_templ_v, x, 'v')

                    except Exception as e:
                        print(f'Ошибка 5.3: {(x, e)}')

                    try:
                        ident = flam_df_d.at[0, ns[13]]
                        matname = flam_df_d.at[0, ns[15]]
                        theme = f'{ident}|{matname} (LPIZAYAVKINAPRO-{x})'
                        email_text = (f'Настоящим сообщаем, что заявка на проведение испытаний материала {matname} c '
                                      f'идентификатором "{ident}" выполнена в отношении показателя "Группа воспламеняемости".\n'
                                      f'Установленная критическая плотность теплового потока (кВт/м\u00b2): {int(min_value_flam)}\n'
                                      f'Установленная группа воспламеняемости: {flam_indicator_real}')
                        file_path_to_email_v = os.path.abspath(os.path.join('.', 'out', str(x), str(x) + "v"+".docx"))
                        file_name = str(x) + "v.docx"
                        if 'a4' in ch_list:
                            email(theme, email_text, file_path_to_email_v, file_name, 'shoya.vs@tn.ru')
                        if 'a7' in ch_list:
                            tg_text = theme + '\n\n' + email_text
                            tg_message(tg_text, topic_id=message_thread_id, file_path=file_path_to_email_v, chat_id=chat_id)
                        if 'a5' in ch_list:
                            tg_text = theme + '\n\n' + email_text
                            tg_message(tg_text, '12', file_path_to_email_v)
                        if 'a3' in ch_list:
                            email_text = email_text + '\n\n\n\n\n\n end point'
                            email(theme, email_text, file_path_to_email_v, file_name, 'lpi@tracker.tn.ru')
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

