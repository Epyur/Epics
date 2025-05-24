import os

import pandas as pd

directory_path = os.path.dirname(os.path.abspath(__file__))
in_title = os.path.abspath(os.path.join('.', 'db', 'in_title.xlsx')) # файл входящих заявок
sbd = os.path.abspath(os.path.join('.', 'db', 'sbd.xlsx')) # файл сводной базы данных
ekn_book = os.path.abspath(os.path.join('.', 'db', 'EKN.xlsx')) # книга ЕКН
out_names = os.path.abspath(os.path.join('.', 'db', 'out_names.xlsx'))
cus_book = os.path.abspath(os.path.join('.', 'db', 'custiomer.xls'))
alltascks = os.path.abspath(os.path.join('.', 'db', 'alltasks.xlsx'))
closedtasks = os.path.abspath(os.path.join('.', 'db', 'closedtasks.xlsx'))
calibration = os.path.abspath(os.path.join('.', 'db', 'calibration.xlsx'))
tg_users = os.path.abspath(os.path.join('.', 'db', 'tgusers.txt'))

# файлы шаблонов отчетов
doc_templ = os.path.abspath(os.path.join('.', 'db', 'g_short.docx'))
doc_templ_fg = os.path.abspath(os.path.join('.', 'db', 'g_full.docx'))
doc_templ_v = os.path.abspath(os.path.join('.', 'db', 'v_short.docx'))

# файлы термодата
def TdtFile(file_date):
    tdt = os.path.abspath(os.path.join('.', 'tdt', f'{file_date} 00_00.tdt'))
    return tdt


n = 101


book_bible = {in_title: 'IncomingTitle', sbd: 'UnitedBaseOfDatas', ekn_book: 'ProductInfo',
              cus_book: 'Customers', out_names: 'OutTitles'}

# Загрузка пространства имён
try:
    name_space_df = pd.read_excel(in_title)
    ns = name_space_df.set_index('col_num')['val'].to_dict()
except Exception as e:
    print(f"Ошибка загрузки пространства имён: {e}")
    ns = {}