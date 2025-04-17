import os



directory_path = os.path.dirname(os.path.abspath(__file__))
in_title = os.path.abspath(os.path.join('.', 'db', 'in_title.xlsx')) # файл входящих заявок
sbd = os.path.abspath(os.path.join('.', 'db', 'sbd.xls')) # файл сводной базы данных
ekn_book = os.path.abspath(os.path.join('.', 'db', 'EKN.xlsx')) # книга ЕКН
out_names = os.path.abspath(os.path.join('.', 'db', 'out_names.xlsx'))
cus_book = os.path.abspath(os.path.join('.', 'db', 'custiomer.xls'))

# файлы шаблонов отчетов
doc_templ = os.path.abspath(os.path.join('.', 'temple', 'g_short.docx'))
doc_templ_fg = os.path.abspath(os.path.join('.', 'temple', 'g_full.docx'))

# файлы термодата
def TdtFile(file_date):
    tdt = os.path.abspath(os.path.join('.', 'tdt', f'{file_date} 00_00.tdt'))
    return tdt


n = 101


book_bible = {in_title: 'IncomingTitle', sbd: 'UnitedBaseOfDatas', ekn_book: 'ProductInfo',
              cus_book: 'Customers', out_names: 'OutTitles'}