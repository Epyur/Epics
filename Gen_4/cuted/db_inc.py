import numpy as np
from Gen_4.service.routes import *
from .index_page import *

# ------------! РАЗБИРАЕМ книгу входящих заявок ! -----------------
inc_df_start = pd.read_excel(inc_book)
inc_df_columns = inc_df_start.columns.tolist()
inc_df = inc_df_start.rename(columns={'№ заявки': 'ID', 'ID заявки': 'Inc_ID', 'Дата поступления заявки': 'Date_in', 'e-mail заказчика': 'cust_mail', 'Цель испытания': 'inv_aim', 'Форма подтверждения соответствия': 'form', 'Приоритетность заявки': 'priority', 'Оцениваемая характеристика': 'cvality', 'Провести испытания во внешней лаборатории': 'ext_lab', 'Наименование внешней лаборатории': 'ext_lab_name', 'ЕКН материала (системы)': 'ekn', 'Наименование материала (при отсутствии ЕКН)': 'product_name', 'Идентификационные признаки образца': 'identity', 'Описание материала, для помещения в протокол': 'description', 'Тип материала (для отдельных групп методов)': 'product_type', 'Количество образцов передаваемых на испытания': 'number_of_prod', 'Фактическая толщина передаваемого образца': 'thickness', 'Целевой показатель (для НИОКР)': 'aim_cvality', 'Ссылки на приложенные файлы': 'link', 'Бюджет': 'budjet', 'Статья расходов': 'title_of_budget', 'ФИО согласующего': 'general_cast', 'Электронная почта согласующего': 'mail_of_general_cast'})
inc_df_columns_new = inc_df.columns.tolist()

# определяем колонку с ID
inc_df_id = inc_df.set_index('ID')

# выбираем из базы заявок строку соответствующую выбранному ID и создаем со

def inc_dict(x):
    if x in inc_df_id.index:
        inc_string = inc_df_id.loc[x].copy()
        inc_string_dict = inc_string.to_dict()
        #print(inc_string_dict)
    else:
        print('Такой записи нет, проверьте актуальность базы заявок')
        inc_string_dict = {}
    return inc_string_dict




