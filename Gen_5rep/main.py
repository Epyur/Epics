
from func import *

# Поиск файлов, совпадающих с названием папки
current_directory = os.getcwd()
try:
    rep_file1 = os.path.join(current_directory, 'rep', 'reports.xlsx')
    old_df = pd.read_excel(rep_file1)
    old_df = old_df.set_index('Unnamed: 0')
except:
    pass


root_directory = r'C:\Users\epyur\YandexDisk-polishchuk@tn.ru\Техническая служба\Пожарная безопасностность\ЛПИ\ПК ЛПИ\out'  # Укажите путь к корневой папке
# путь к отчетному файлу

rep_file = os.path.join(current_directory, 'rep', 'report.xlsx')


text_to_remove = '-//-'

# перечень колонок, которые мы хотим сразу удалить из будущего датафрейма
column_to_remove = ['Телефон представителя']


# формируем список датафреймов из разных файлов
dataframes = DfList(root_directory)


# создаем объединенный датафрейм и записываем его в файл эксель
try:
    merged_df = MergDF(dataframes)
except:
    merged_df = old_df

# merged_df = merged_df.fillna(np.nan)

try:
    r_df = pd.concat([old_df, merged_df])
    r_df = r_df.reset_index(drop=True, level=0)
    m_df = r_df.drop_duplicates(keep='first')
    merged_df = m_df.copy()
except Exception as e:
    print(e)



# Создание директории, если не существует
Path(rep_file).parent.mkdir(parents=True, exist_ok=True)

# Экспорт в Excel
with pd.ExcelWriter(rep_file, engine='xlsxwriter') as writer:
    merged_df.to_excel(writer, index=True, sheet_name='Сводные данные')
# выделяем красным соответствия/не соответствия. функцию применять только на файле с одной вкладкой,
# в противном случае вкладки, к которым не применяется функция, будут удалены.
color_cell = ['Не соответствует', 'Соответствует']


all_columns_index = merged_df.columns
all_columns_list = all_columns_index.to_list()
# print(all_columns_list)
#
# сортировка №1 сведения о заявках на горючесть
colums_1 = ['Предмет исследования', 'Номер строки в СБД', 'Номер заявки', 'Номер испытания', 'e-mail заказчика',
            'ФИО заказчика', 'Наименование лаборатории', 'Идентификатор образца', 'ЕКН', 'Название материала',
            'СТО (ТУ) на материал', 'Описание', 'Производитель', 'Дополнительная информация', 'Толщина, мм',
            'Группа горючести (декларируемая)', 'Температура_ОС', 'Давление_ОС', 'Влажность_ОС', 'Дата протокола',
            'ФИО испытателя', 'Дата поступления образцов', 'Дата проведения испытания', 'Начальная температура в печи',
            'Температура газов на ТП1', 'Время достижения', 'Температура газов на ТП2', 'Время достижения.1',
            'Температура газов на ТП3', 'Время достижения.2', 'Температура газов на ТП4', 'Время достижения.3',
            'Средняя температура ДГ', 'Группа горючести по температуре ДГ', 'Соответствие',
            'Время достижения максимальной температуры газов', 'Длина повреждений, образец 1',
            'Длина повреждений, образец 2', 'Длина повреждений, образец 3', 'Длина повреждений, образец 4',
            'Среднее значение длины повреждений', 'Группа горючести по повреждениям', 'Соответствие.1',
            'Масса образца до испытания', 'Масса образца после испытания', 'Потеря массы',
            'Группа горючести по потере массы', 'Соответствие.2', 'Время самостоятельного горения, с',
            'Группа горючести по времени самостоятельного горения', 'Соответствие.3', 'Падение горящих капель расплава',
            'Группа горючести по падению капель', 'Соответствие декларируемой группе горючести по падению капель',
            'Итоговая оценка группы горючести', 'Общее соответствие', 'Тип основания под образец', 'Способ фиксации',
            'Время начала испытания', 'Фото образца до испытания', 'Фото образца после испытания',
            'Дополнительная информация и наблюдения', 'Ссылка на протокол внешней лаборатории']
df_comb = SelectAndFilter(merged_df, colums_1, mean_column='Масса образца до испытания', key_column='Название материала',
                          key_word='пвх', file_nam=rep_file, sheet_nam='Горючесть_ПВХ')
df_comb2 = SelectAndFilter(merged_df, colums_1, mean_column='Масса образца до испытания', key_column='Название материала',
                          key_word='LOGICPIR', file_nam=rep_file, sheet_nam='Горючесть_PIR')

# Сортировка №2, сведения о заявках на воспламеняемость
colums_2 = ['Предмет исследования', 'Номер строки в СБД', 'Номер заявки', 'Номер испытания', 'e-mail заказчика',
            'ФИО заказчика', 'Наименование лаборатории', 'Идентификатор образца', 'ЕКН', 'Название материала',
            'СТО (ТУ) на материал', 'Описание', 'Производитель', 'Дополнительная информация', 'Толщина, мм',
            'Группа воспламеняемости (декларируемая)', 'Температура_ОС', 'Давление_ОС', 'Влажность_ОС',
            'Дата регистрации результатов', 'Испытатель', 'Дата поступления образцов.1', 'Дата проведения испытания.1',
            'Ссылка на протокол внешней лаборатории.1', 'Тип основания под образец.1', 'Способ фиксации образца',
            'Плотность теплового потока', 'Факт воспламенения', 'Время воспламенения',
            'Установленная группа воспламеняемости', 'Соответствие.4', 'Дополнительная информация.1']
df_flam = SelectAndFilter(merged_df, colums_2, mean_column='Время воспламенения', key_column='Название материала',
                          key_word='пвх')
df_flam = SelectAndFilter(df_flam, colums_2, mean_column='ЕКН', file_nam=rep_file, sheet_nam='Воспламеняемость_ПВХ')
df_flam2 = SelectAndFilter(merged_df, colums_2, mean_column='Время воспламенения', key_column='Название материала',
                          key_word='LOGICPIR', file_nam=rep_file, sheet_nam='Воспламеняемость_PIR')

ColorMark(rep_file, 'Не соответствует', 'Соответствует')

# series_comparison = df_comb2['Общее соответствие']
# p1 = plot_pie_chart(series_comparison, title='LOGICPIR \n Общее соответствие по всем испытаниям',
#               new_file_name='PIR_gen')
# series_comparison2 = df_comb2['Соответствие.3']
# p2 = plot_pie_chart(series_comparison2, title='LOGICPIR \n Соответствие по показателю времени самостоятельного горения',
#                new_file_name='PIR_comb')
# series_comparison3 = df_comb2['Соответствие']
# p3 = plot_pie_chart(series_comparison3, title='LOGICPIR \n Соответствие по показателю длины повреждений',
#                new_file_name='PIR_lenth')
#
# series_comparison4 = df_comb2['Соответствие.1']
# p4 = plot_pie_chart(series_comparison4, title='LOGICPIR \n Соответствие по показателю температуры дымовых газов',
#                new_file_name='PIR_smog')
#
# series_comparison5 = df_comb2['Соответствие.2']
# p5 = plot_pie_chart(series_comparison5, title='LOGICPIR \n Соответствие по показателю потери массы',
#                new_file_name='PIR_mass')
# df_flam3 = SelectAndFilter(merged_df, ['Соответствие.4'], mean_column='Соответствие.4')
# print(df_flam3)
# series_comparison6 = df_flam3['Соответствие.4']
# p6 = plot_pie_chart(series_comparison6, title='LOGICROOF \n Общее соответствие (воспламеняемость)',
#                new_file_name='PVC_flam', colors=['green', 'red', 'gray'])

column_to_pic = ['Соответствие', 'Соответствие.1', 'Соответствие.2', 'Соответствие.3',
                 'Соответствие декларируемой группе горючести по падению капель', 'Общее соответствие']
column_to_pic_new = ['Температура дымовых газов', 'Длина повреждений',  'Потеря массы',
                         'Время самостоятельного горения', 'Падение горящих капель', 'Общая оценка']

column_to_pic_rename = dict(zip(column_to_pic, column_to_pic_new))
# print(column_to_pic_rename)
df_to_pic = df_comb2[column_to_pic]
df_to_pic = df_to_pic.rename(columns=column_to_pic_rename)
# print(df_to_pic)
PicatorVtoroy(df_to_pic, column_to_pic_new,  'LOGICPIR\n параметры соответствия', 'logicpir', 'Соответствует', 'Не соответствует')

# PicatorVtoroy(df_to_pic, column_to_pic_new,  'LOGICPIR\n параметры соответствия', 'logicpir', 'Соответствует', 'Не соответствует')

