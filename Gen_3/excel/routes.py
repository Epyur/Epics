import os

directory_path = os.path.dirname(os.path.abspath(__file__))

bb = os.path.abspath(os.path.join('.', 'БИ4.xlsx')) # целевой файл
inc_book = os.path.abspath(os.path.join('.', 'excel', 'inc.xls')) # файл входящих заявок
comb_book = os.path.abspath(os.path.join('.', 'excel', '302442.xls')) # журнал результатов испытаний на горючесть
flam_book = os.path.abspath(os.path.join('.', 'excel', '30402.xls')) # журнал результатов испытаний на воспламеняемость
ekn_book = os.path.abspath(os.path.join('.', 'excel', 'EKN.xlsx')) # книга ЕКН
amb_book = os.path.abspath(os.path.join('.', 'excel', 'ambient.xls')) # журнал условий в лаборатории
cus_book = os.path.abspath(os.path.join('.', 'excel', 'custiomer.xls')) # журнал условий в лаборатории


doc_templ = os.path.abspath(os.path.join('.', 'docx', 'g_short.docx'))
