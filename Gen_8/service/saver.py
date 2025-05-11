import pandas as pd
from .rout_map import *
from .photo import PhotoFinder
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os

def report_to_excel(df, out_num):

    dd = (str(out_num) + '.xlsx')
    out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
    ds = df.to_excel(out_book)
    return ds


def report_to_word(df, templ, out_num, ind):
    """
    Генерирует Word-документ из шаблона с данными и изображениями

    :param df: DataFrame с данными
    :param templ: Путь к шаблону Word
    :param out_num: Номер отчета
    :param ind: Суффикс для имени файла
    :return: Путь к сохраненному файлу
    """
    # Создаем базовый контекст из данных DataFrame
    suffix_column = 'series_num'
    dict1 = {
        f'{col}_{int(row[suffix_column])}': row[col]
        for col in df.columns
        for _, row in df.iterrows()
    }

    doc = DocxTemplate(templ)
    context = dict1.copy()  # Копируем базовый контекст

    # Определяем списки тегов для изображений
    before_tags = ["img1c", "img2c", "img3c"]
    after_tags = ["img4c", "img5c", "img6c"]
    graph_tags = ["img1", "img2", "img3"]

    for i in range(len(df)):
        # Обработка фото "до испытания"
        try:
            if i < len(before_tags) and 'photo_before' in df.columns:
                photo_path = df.at[i, 'photo_before']
                relative_path_1c = PhotoFinder(photo_path)
                if pd.notna(relative_path_1c) and os.path.exists(relative_path_1c):
                    img = InlineImage(doc, relative_path_1c, width=Mm(80))
                    context[before_tags[i]] = img
        except Exception as e:
            print(f'Ошибка вставки фото "до испытания" {i + 1}: {e}')

        # Обработка фото "после испытания"
        try:
            if i < len(after_tags) and 'photo_after' in df.columns:
                photo_path = df.at[i, 'photo_after']
                relative_path_2c = PhotoFinder(photo_path)
                if pd.notna(relative_path_2c) and os.path.exists(relative_path_2c):
                    img = InlineImage(doc, relative_path_2c, width=Mm(80))
                    context[after_tags[i]] = img
        except Exception as e:
            print(f'Ошибка вставки фото "после испытания" {i + 1}: {e}')

        # Обработка графиков
        try:
            if i < len(graph_tags) and 'series_num' in df.columns:
                ser_num = df.at[i, 'series_num']
                graph_path = os.path.abspath(os.path.join(
                    '.', 'out', str(out_num),
                    f'{out_num}_{ser_num}.jpg'
                ))

                if os.path.exists(graph_path):
                    img = InlineImage(doc, graph_path, width=Mm(160))
                    context[graph_tags[i]] = img
                else:
                    print(f'График не найден: {graph_path}')
        except Exception as e:
            print(f'Ошибка вставки графика {i + 1}: {e}')

    # Рендеринг документа
    try:
        doc.render(context)
    except Exception as e:
        print(f'Ошибка при рендеринге документа: {e}')
        return None

    # Сохранение результата
    output_filename = f"{out_num}{ind}.docx"
    output_path = os.path.abspath(os.path.join(
        '.', 'out', str(out_num), output_filename
    ))

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        return output_path
    except Exception as e:
        print(f'Ошибка при сохранении документа: {e}')
        return None