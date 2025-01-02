import os

directory_path = os.path.dirname(os.path.abspath(__file__))

bb = os.path.abspath(os.path.join('..', 'Gen_3', 'БИ4.xlsx')) # целевой файл
inc_book = os.path.abspath(os.path.join('..', 'Gen_3', 'excel', 'inc.xls')) # файл входящих заявок
comb_book = os.path.abspath(os.path.join('..', 'Gen_3', 'excel', '302442.xls')) # журнал результатов испытаний на горючесть
flam_book = os.path.abspath(os.path.join('..', 'Gen_3', 'excel', '30402.xls')) # журнал результатов испытаний на воспламеняемость
ekn_book = os.path.abspath(os.path.join('..', 'Gen_3', 'excel', 'EKN.xlsx')) # книга ЕКН
amb_book = os.path.abspath(os.path.join('..', 'Gen_3', 'excel', 'ambient.xls')) # журнал условий в лаборатории
