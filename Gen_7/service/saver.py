import docxtpl
from docx.shared import Mm
from .rout_map import *
from .photo import PhotoFinder

def report_to_excel(df, out_num):

    dd = (str(out_num) + '.xlsx')
    out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
    ds = df.to_excel(out_book)
    return ds


def report_to_word(df, templ, out_num):
    suffix_column = 'series_num'
    dict1 = {f'{col}_{int(row[suffix_column])}': row[col]
              for col in df.columns
              for _, row in df.iterrows()}

    doc = docxtpl.DocxTemplate(templ)

    before = ["img1c", "img2c", "img3c"]
    after = ["img4c", "img5c", "img6c"]
    grafs = ["img1", "img2", "img3"]
    context = {}
    for i in range(0, len(df)-1):

        try:
            before_1 = df.at[i, 'photo_before']
            ph_before = before[i]
            relative_path_1c = PhotoFinder(before_1)
            insert_image1c = docxtpl.InlineImage(doc, relative_path_1c, width=Mm(80))
            context.update({ph_before: insert_image1c})
        except Exception as e:
            print(e)

        try:
            after_1 = df.at[i, 'photo_after']
            ph_after = after[i]
            relative_path_4c = PhotoFinder(after_1)
            insert_image4c = docxtpl.InlineImage(doc, relative_path_4c, width=Mm(80))
            context.update({ph_after: insert_image4c})
        except:
            pass
            # print('Не введен номер фотографии "образец 1 после испытания"')

        try:
            ser_num = df.at[i, 'series_num']
            graf_pig = grafs[i]
            relative_path_1 = os.path.abspath(os.path.join('.', 'out', str(out_num), f'{str(out_num)}_{str(ser_num)}.jpg'))
            insert_image1 = docxtpl.InlineImage(doc, relative_path_1, width=Mm(160))
            context.update({graf_pig: insert_image1})
        except Exception as e:
            print(e)

    try:
        d = dict1 | context
        doc.render(d)
    except:
        doc.render(dict1)


    sg = (str(out_num) + '.docx')
    out_report = os.path.abspath(os.path.join('.', 'out', str(out_num), sg))
    p = doc.save(out_report)
    return p