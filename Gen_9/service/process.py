import os
import pandas as pd

from Gen_9.service.consumer import ConsumerInfo
from Gen_9.service.core import Materials, FrameOfData
from Gen_9.service.getmail import GetMail
from Gen_9.service.rout_map import closedtasks, exp_book, cus_book, ns, ekn_book, alltasks, sbd

def get_all():
    try:
        materials_data = FrameOfData().load_data(ekn_book)
        consumer_data = FrameOfData().load_data(cus_book)
        print('Загрузка информации о новых заявках....')
        try:
            new_tasks = GetMail()
            new_tasks.process_messages()
            new_tasks_df = new_tasks.GetDf
            new_tasks.save_to_excel(sbd)
        except Exception as e: print(e)
        for i in range(0, len(new_tasks_df)):
            cust_mail = new_tasks_df.at[i, ns[10]]
            cust_info = ConsumerInfo(consumer_data, cust_mail)
            new_tasks_df.at[i, ns[11]] = cust_info.cons_name
            new_tasks_df.at[i, ns[93]] = cust_info.cons_place_of_work
            new_tasks_df.at[i, ns[95]] = cust_info.cons_tel
            new_tasks_df.at[i, ns[94]] = cust_info.cons_co_requesits
            new_tasks_df.at[i, ns[96]] = cust_info.cons_sbe
            new_tasks_df.at[i, ns[97]] = cust_info.cons_ind

            try:
                mat_name_ekn = new_tasks_df.at[i, ns[14]].split(',')
                ekn = mat_name_ekn[-1]
                new_tasks_df.at[i, ns[14]] = ekn
            except Exception as e: print(f'Ошибка извлечения ekn: {e}')
            finally:
                ekn = new_tasks_df.at[i, ns[14]]
                if ekn:
                    ekn = int(ekn)
                    material_info = Materials(materials_data, ekn)
                    new_tasks_df.at[i, ns[15]] = material_info.get_name
                    # filtered_work_data.at[item, ns[16]] = material_info.get_color
                    new_tasks_df.at[i, ns[17]] = material_info.get_sto
                    new_tasks_df.at[i, ns[18]] = material_info.get_description
                    new_tasks_df.at[i, ns[19]] = material_info.get_producer_name
                    new_tasks_df.at[i, ns[22]] = material_info.get_thickness
                    new_tasks_df.at[i, ns[23]] = material_info.get_comb_group
                    new_tasks_df.at[i, ns[24]] = material_info.get_flam_group
                    new_tasks_df.at[i, ns[25]] = material_info.get_prop_group

        # Сохраняем в Excel
        if os.path.exists(alltasks):
            existing_df = pd.read_excel(alltasks)

            updated_df = pd.concat([existing_df, new_tasks_df], ignore_index=True)

        else:
            updated_df = new_tasks_df

        updated_df.to_excel(alltasks, index=False)
    except Exception as e: print(e)

    try:
        print('Загрузка информации о закрытых заявках....')
        closed_tasks = GetMail(folder='LPIFin')
        closed_tasks.process_messages()
        closed_tasks.save_to_excel(closedtasks)
    except: pass