import numpy as np
import os
from docxtpl import DocxTemplate
from Gen_3.internal.connector import *
from Gen_3.internal.calc import *


counter_x = 0
while counter_x <= 10:
    counter_x += 1
    x = int(input('Введите номер заявки: '))


    out_file_name = str(x)

    def base_saver(x):
        df = calculator(x).copy()
        dd = str(out_file_name + '.xlsx')
        out_book = os.path.abspath(os.path.join('.', 'out', dd))
        ds = df.to_excel(out_book)
        dict_x = inc_df_merged_comb_flam.loc[x].to_dict()
        return ds

    if x<=101:
        base_saver(x)
        print('Data were added to base')
        dict_x = calculator(x).to_dict()
        # print(dict_x)
        doc = DocxTemplate(doc_templ)
        context = dict_x
        doc.render(context)
        dw = str(out_file_name + '.docx')
        out_report = os.path.abspath(os.path.join('.', 'out', dw))
        doc.save(out_report)
    else:
        print('Свяжитесь с Полищуком Евгением (polishchuk@tn.ru)')


    print('©lab_2025 ver.1.2')
    continue