from .dictator import *
from .routes import *
from ..methods.comb import *
from .saver import *
from ..methods.ignition import ignitor

counter_x = 0

while counter_x <= 100:
    counter_x += 1
    x = int(input('Введите номер заявки или 0, для завершения программы: '))
    dict_0 = {'ID': x} # словарь ID
    # print(dict_0)
    if x == 0:
        print("До свидания!")
        exit()
    else:
        dict_1 = dict_creator(inc_book, 'ID', x, ['place', 'ext_lab_name', 'number_of_samples', 'priority', 'budget', 'expense_item', 'matching_agent', 'matching_agent_mail']) # информация о входящей заявке
        # print(dict_1)
        # print(dict_1.get('ekn'))

        if dict_1 is False:
            print(f'ID {x} отсутствует в базе данных')
        else:
            if dict_1.get('ekn') is not np.nan:
                ekn = dict_1.get('ekn')
                # print(ekn)
                dict_2 = dict_creator(ekn_book, 'ekn', ekn, ['ki_indicator']) # получаем словарь информации о материале
                # print(dict_2)

            if dict_2 is False or dict_1['ekn'] == np.nan:
                print('В заявке не указан ЕКН или ЕКН указан не верно')
                ekn_new = int(input('Введите № ЕКН, либо введите 1 - НИОКР Техслужбы СБЕ; \n2 - НИОКР Завода ПИР; 3 - НИОКР завода ПВХ Мембран): '))
                dict_1.update({'екн': ekn_new})
                dict_2 = dict_creator(ekn_book, 'ekn', ekn_new)
                # print(dict_2)
            dict_united = dict_unition(dict_0, dict_1)
            # print(dict_0_1)

            dict_united = dict_unition(dict_united, dict_2)
            # print(dict_0_2)
            dict_3 = combustor(x, dict2=dict_united) # точка входа в модуль comb.py
            if dict_3 is False:
                print(f'В базе данных испытаний по методу 2 ГОСТ 30244 запись с ID {x} отсутствует')
            else:
                dict_united = dict_unition(dict_united, dict_3) # точка выхода из модуля comb,py
                choice_report_30244 = int(input('Данные по результатам испытаний по Метод 2 ГОСТ 30244 введены. Выберите '
                                               'форму отчета Word: \n1 - Полный протокол; \n2 - Краткая справка по испытаниям'
                                                '\n3 - продолжить без формирования протокола \n'))
                if choice_report_30244 == 1:
                    templ_30244 = doc_templ_fg
                    suffix = "_full"
                    report_to_word(dict_united, templ_30244, str(x), suffix=suffix)
                if choice_report_30244 == 2:
                    templ_30244 = doc_templ
                    suffix = '_short'
                    report_to_word(dict_united, templ_30244, str(x), suffix=suffix)
                if choice_report_30244 == 3:
                    pass

            dict_4 = ignitor(x, dict2=dict_united) #Точка входа в модуль ignition.py
            if dict_4 is False:
                print(f'В базе данных испытаний по методу ГОСТ 30402 запись с ID {x} отсутствует')
            else:
                dict_united = dict_unition(dict_united, dict_4, prefix2='ignition')
                # choice_report_30244 = int(
                #     input('Данные по результатам испытаний по Метод 2 ГОСТ 30244 введены. Выберите '
                #           'форму отчета Word: \n1 - Полный протокол; \n2 - Краткая справка по испытаниям'
                #           '\n3 - продолжить без формирования протокола \n'))
                # if choice_report_30244 == 1:
                #     templ_30244 = doc_templ_fg
                #     suffix = "_full"
                #     report_to_word(dict_united, templ_30244, str(x), suffix=suffix)
                # if choice_report_30244 == 2:
                #     templ_30244 = doc_templ
                #     suffix = '_short'
                #     report_to_word(dict_united, templ_30244, str(x), suffix=suffix)
                # if choice_report_30244 == 3:
                #     pass

            # формируем переименованный словарь и сохраняем его в excel
            dict_united_renamed = final_rename(dict_united)
            report_to_excel(dict_united_renamed, str(x))

