import os
import pandas as pd
import numpy as np
from docxtpl import DocxTemplate


directory_path = os.path.dirname(os.path.abspath(__file__))
lpi_db = os.path.abspath(os.path.join('.', 'db', 'LPI.db'))
in_title = os.path.abspath(os.path.join('.', 'db', 'in_title.xlsx')) # файл входящих заявок
inc_book = os.path.abspath(os.path.join('.', 'db', 'inc.xls')) # файл входящих заявок
comb_book = os.path.abspath(os.path.join('.', 'db', '302442.xls')) # журнал результатов испытаний на горючесть
flam_book = os.path.abspath(os.path.join('.', 'db', '30402.xls')) # журнал результатов испытаний на воспламеняемость
ekn_book = os.path.abspath(os.path.join('.', 'db', 'EKN.xlsx')) # книга ЕКН
amb_book = os.path.abspath(os.path.join('.', 'db', 'ambient.xls')) # журнал условий в лаборатории
cus_book = os.path.abspath(os.path.join('.', 'db', 'custiomer.xls')) # журнал условий в лаборатории
out_names = os.path.abspath(os.path.join('.', 'db', 'out_names.xlsx'))

# файлы шаблонов отчетов
doc_templ = os.path.abspath(os.path.join('.', 'temple', 'g_short.docx'))
doc_templ_fg = os.path.abspath(os.path.join('.', 'temple', 'g_full.docx'))



n = 101


book_bible = {in_title: 'IncomingTitle', inc_book: 'IncomingApplication', comb_book: "CombustionBook",
              flam_book: 'FlamBook', ekn_book: 'ProductInfo', amb_book: 'AmbientConditions',
              cus_book: 'Customers', out_names: 'OutTitles'}