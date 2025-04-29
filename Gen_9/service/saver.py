import os
import docxtpl
import pandas as pd
from docx.shared import Mm

from Gen_9.service.core import PhotoFinder
from Gen_9.service.rout_map import ns



class ReportGenerator:
    def __init__(self, out_num):
        self.out_num = str(out_num)
        self.suffix_column = ns[9]
        self.before_keys = ["img1c", "img2c", "img3c"]
        self.after_keys = ["img4c", "img5c", "img6c"]
        self.graf_keys = ["img1", "img2", "img3"]
        self.sheet_name = None
        self.out_report = None
        if not os.path.exists(os.path.join('.', 'out', self.out_num)):
            # Если директория не существует, создаём её
            os.makedirs(os.path.join('.', 'out', self.out_num))

    def report_to_word(self, df, templ, ind):
        try:
            # Создаем словарь с данными для шаблона
            self.dict1 = {f'{col}_{int(row[self.suffix_column])}': row[col]
                          for col in df.columns
                          for _, row in df.iterrows()}

            # Инициализируем шаблон
            doc = docxtpl.DocxTemplate(templ)

            # Создаем контекст для шаблона
            context = {}
            finder = PhotoFinder(base_dir='DCIM')

            # Проходим по всем строкам датафрейма
            for i in range(0, len(df) - 1):

                # Добавляем изображения до испытания
                try:
                    before_1 = df.at[i, ns[70]]
                    ph_before = self.before_keys[i]
                    relative_path_1c = finder.get_file_path(before_1)
                    insert_image1c = docxtpl.InlineImage(doc, relative_path_1c, width=Mm(80))
                    context.update({ph_before: insert_image1c})
                except Exception as e:
                    print(f'{e} - это та самая ошибка')

                # Добавляем изображения после испытания
                try:
                    after_1 = df.at[i, ns[71]]
                    ph_after = self.after_keys[i]
                    relative_path_4c = finder.get_file_path(after_1)
                    insert_image4c = docxtpl.InlineImage(doc, relative_path_4c, width=Mm(80))
                    context.update({ph_after: insert_image4c})
                except:
                    pass

                # Добавляем графики
                try:
                    ser_num = df.at[i, ns[9]]
                    graf_pig = self.graf_keys[i]
                    relative_path_1 = os.path.abspath(
                        os.path.join('.', 'out', self.out_num, f'{self.out_num}_{str(ser_num)}.jpg'))
                    insert_image1 = docxtpl.InlineImage(doc, relative_path_1, width=Mm(160))
                    context.update({graf_pig: insert_image1})
                except Exception as e:
                    print(f'Ошибка внутри функции сохранения в ворд: {e}')

            # Объединяем данные и контекст
            try:
                d = self.dict1 | context
                doc.render(d)
            except:
                doc.render(self.dict1)

            # Формируем путь сохранения
            sg = (self.out_num + ind + '.docx')
            self.out_report = os.path.abspath(os.path.join('.', 'out', self.out_num, sg))

            # Сохраняем документ
            p = doc.save(self.out_report)
            return p

        except Exception as e:
            print(f"Произошла ошибка при генерации отчета: {e}")
            return None

    def report_to_excel(self, df, sheet_name):
        self.sheet_name = sheet_name
        # Удаляем пустые столбцы из датафрейма
        df = df.dropna(how='all', axis=1)

        # Создаем путь к файлу
        dd = (self.out_num + '.xlsx')
        out_book = os.path.abspath(os.path.join('.', 'out', self.out_num, dd))

        try:
            # Проверяем существование файла
            if os.path.exists(out_book):
                # Если файл существует, используем ExcelWriter с mode='a' (append)
                with pd.ExcelWriter(out_book, mode='a', engine='openpyxl') as writer:
                    # Удаляем существующий лист 'Результаты' если он есть
                    try:
                        book = writer.book
                        sheet = book[self.sheet_name]
                        book.remove(sheet)
                    except KeyError:
                        pass  # Листа не существует, продолжаем

                    # Записываем новый лист
                    df.to_excel(writer, sheet_name=self.sheet_name, index=False)
            else:
                # Если файла нет - создаем новый
                df.to_excel(out_book, sheet_name=self.sheet_name, index=False)

        except Exception as e:
            raise ValueError(f"Ошибка при сохранении Excel файла: {str(e)}")

        return out_book

    @property
    def get_path_to_word(self):
        path = self.out_report
        return path
