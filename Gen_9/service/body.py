import math

from Gen_9.service.consumer import ConsumerInfo
from Gen_9.service.core import *
from Gen_9.service.def_lib import TakeRequest
from Gen_9.service.rout_map import *
from Gen_9.service.saver import ReportGenerator
from Gen_9.service.standarts import GOST30244, GOST30402

materials_data = FrameOfData().load_data(ekn_book)
consumer_data = FrameOfData().load_data(cus_book)
title_data = FrameOfData().load_data(in_title)

start_work_data = FrameOfData(excel_file=sbd, source_of_titles=title_data)
start_work_data.load_data()
work_data = start_work_data.rename_df(key='key', val='val') # rename the dataframe from excel

filtered_work_data = TakeRequest(work_data, ns[8], [107], title_data) # make base frame with inc number
column_list = list(filtered_work_data)
w_d = FrameOfData(data=filtered_work_data)
filtered_work_data = w_d.update_dataframe()
saver = ReportGenerator(107)

# now we are trying to find information about consumer request and fill target frame
target_columns = [ns[3], ns[10], ns[12], ns[13], ns[14], ns[15], ns[22], ns[23], ns[24], ns[25]]
try:
    teg_list = filtered_work_data.at[0, ns[5]].split(',') # take tegs from excel
    inc_id = int(teg_list[0])
    inc_frame = TakeRequest(work_data, ns[7], [inc_id], title_data)

    # transferring data from inc frame to work frame

    for item in target_columns:
        filtered_work_data[item] = inc_frame.at[0, item]
except:
    for item in target_columns:
        filtered_work_data[item] = filtered_work_data.at[0, item]


#now we will try to find information about consumer and material
try:
    for item in range(0, len(filtered_work_data)):
        cons_email = filtered_work_data.at[item, ns[10]]
        consumer_info = ConsumerInfo(consumer_data, cons_email)
        filtered_work_data.at[item, ns[11]] = consumer_info.cons_name
        filtered_work_data.at[item, ns[93]] = consumer_info.cons_place_of_work
        filtered_work_data.at[item, ns[95]] = consumer_info.cons_tel
        filtered_work_data.at[item, ns[94]] = consumer_info.cons_co_requesits
        filtered_work_data.at[item, ns[96]] = consumer_info.cons_sbe
        filtered_work_data.at[item, ns[97]] = consumer_info.cons_ind
except: pass

try:
    ekn = int(filtered_work_data.at[0, ns[14]])
    print(ekn)
    try:
        if math.isnan(ekn):
            mat_name_ekn = filtered_work_data.at[0, ns[15]].split(',')
            ekn = int(mat_name_ekn[-1])
        else: pass
    except: pass


    try:
        if math.isnan(ekn): pass
        else:
            for item in range(0, len(filtered_work_data)):
                material_info = Materials(materials_data, ekn)
                filtered_work_data.at[item, ns[15]] = material_info.get_name
                # filtered_work_data.at[item, ns[16]] = material_info.get_color
                filtered_work_data.at[item, ns[17]] = material_info.get_sto
                filtered_work_data.at[item, ns[18]] = material_info.get_description
                filtered_work_data.at[item, ns[19]] = material_info.get_producer_name
                filtered_work_data.at[item, ns[22]] = material_info.get_thickness
                filtered_work_data.at[item, ns[23]] = material_info.get_comb_group
                filtered_work_data.at[item, ns[24]] = material_info.get_flam_group
                filtered_work_data.at[item, ns[25]] = material_info.get_prop_group

    except: pass
except: pass

# now we are trying to split frame by methods
# first we will try to get a df of GOST30244 results

try:
    gost_30244_res = TakeRequest(filtered_work_data, ns[1], ['Группа горючести'])
    if not gost_30244_res.empty:
        # now we will create new row in df and fill it with basic info
        try:
            gost_30244_res = gost_30244_res.set_index(ns[0]).reset_index(drop=True, level=0)
        except: pass
 # there are we fill in rest cells by GOST
        try:
            gost_30244_est = GOST30244(gost_30244_res)

            gost_30244_res = gost_30244_est.update_dataframe()
        except Exception as msg: print(f'30244 dataframe problems: {msg}')

        try:
            frame_30244_to_save = FrameOfData(data=gost_30244_res, source_of_titles=title_data).rename_df(key='val', val='val2')
            save_30244_to_word = saver.report_to_word(gost_30244_res, doc_templ_v, 'g')
            s_w_30244 = saver.get_path_to_word
            save_30244_to_excel = saver.report_to_excel(frame_30244_to_save, 'Горючесть')

        except Exception as msg:
            print(msg)
    else: pass
except Exception as msg: print(msg)

# second we will try to get a df of GOST30402 results
try:
    gost_30402_res = TakeRequest(filtered_work_data, ns[1], ['Группа воспламеняемости'])
    # now we will create new row in df and fill it in with basic info
    ptp_list = []
    if not gost_30402_res.empty:
        try:
            gost_30402_res = gost_30402_res.set_index(ns[0]).reset_index(drop=True, level=0)
            count = len(gost_30402_res)
            for item in column_list:
                count *= 1
                if isinstance(gost_30402_res.at[0, item], str):
                    gost_30402_res.at[count, item] = gost_30402_res.at[0, item]
                else:
                    gost_30402_res.at[count, item] = gost_30402_res[item].mean()
                    gost_30402_res.at[count, ns[9]] = 103
                    gost_30402_res.at[count, ns[7]] = np.nan
                    gost_30402_res.at[count, ns[81]] = np.nan
                    gost_30402_res.at[count, ns[82]] = np.nan
                    gost_30402_res.at[count, ns[83]] = np.nan
            for it_s in range(0, len(gost_30402_res)-1):
                if 'Да' in gost_30402_res.at[it_s, ns[82]]:
                    ptp_list.append(gost_30402_res.at[it_s, ns[81]])
            kptp = int(min(ptp_list))
            gost_30402_res.at[count, ns[81]] = kptp
        except: pass
        # there are we fill in rest cells by GOST
        try:
            gost_30402_est = GOST30402(gost_30402_res)
            gost_30402_res = gost_30402_est.update_dataframe()
        except: pass

        try:
            frame_30402_to_save = FrameOfData(data=gost_30402_res, source_of_titles=title_data).rename_df(key='val',
                                                                                                          val='val2')
            save_30402_to_word = saver.report_to_word(gost_30402_res, doc_templ_v, 'v')
            s_w_30402 = saver.get_path_to_word
            save_30402_to_excel = saver.report_to_excel(frame_30402_to_save, 'Воспламеняемость')
        except Exception as msg:
            print(msg)
    else: pass
except Exception as msg: print(msg)