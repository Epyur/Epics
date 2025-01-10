import numpy as np
import os
from docxtpl import DocxTemplate
from Gen_3.internal.connector import *
from Gen_3.internal.calc import *

if __name__ == '__main__':

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

        if x == 0:
            exit()

        base_saver(x)
        print('Данные добавлены в базу данных')
        dict_g = calculator(x).to_dict()
        context_g = dict_g

        choice1 = int(input("Выберите метод, по которому хотите оформить протокол: \n1 - ГОСТ 30244, метод 2\n2 - ГОСТ 30402\n"))
        if choice1 == 1:
            choice2 = int(input('Выберите форму протокола: \n1 - Полный протокол; \n2 - Краткая справка по испытаниям\n'))
            if choice2 == 1:
                if x <= n:
                    doc = DocxTemplate(doc_templ_fg)
                    doc.render(context_g)
                    fg = str(out_file_name + '_Г_full' + '.docx')
                    out_report_fg = os.path.abspath(os.path.join('.', 'out', fg))
                    doc.save(out_report_fg)
                else:
                    print('Свяжитесь с Полищуком Евгением (polishchuk@tn.ru)')
            if choice2 == 2:
                if x <= n:
                    doc = DocxTemplate(doc_templ)
                    doc.render(context_g)
                    sg = str(out_file_name + '_Г_short' + '.docx')
                    out_report_sg = os.path.abspath(os.path.join('.', 'out', sg))
                    doc.save(out_report_sg)
                else:
                    print('Свяжитесь с Полищуком Евгением (polishchuk@tn.ru)')
        if  choice1 == 2:
            print('Формы протоколов по методу ГОСТ 30402 пока не готовы')
            continue


        print('©lab_2025 ver.1.2')
        continue