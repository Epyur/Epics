import os

directory_path = os.path.dirname(os.path.abspath(__file__))

bb = os.path.abspath(os.path.join('..', 'Gen_2', 'БИ4.xlsx')) # целевой файл
inc_book = os.path.abspath(os.path.join('..', 'Gen_2', 'excel', 'inc.xls')) # файл входящих заявок
comb_book = os.path.abspath(os.path.join('..', 'Gen_2', 'excel', '302442.xls')) # журнал результатов испытаний на горючесть
flam_book = os.path.abspath(os.path.join('..', 'Gen_2', 'excel', '30402.xls')) # журнал результатов испытаний на воспламеняемость