import docxtpl
from docx.shared import Mm

from .dictator import flatten_dict
from .photo import PhotoFinder
from .routes import *

def report_to_excel(dict1, out_file_name, out_num):
    df = dict1.copy()
    zf = pd.DataFrame(list(df.items()))
    dd = str(out_file_name + '.xlsx')
    out_book = os.path.abspath(os.path.join('.', 'out', str(out_num), dd))
    ds = zf.to_excel(out_book)
    return ds


def report_to_word(dict1, templ, out_file_name, suffix, out_num):
    fl = flatten_dict(dict1)

    try:
        fekn = int(fl['ekn'])
        fl.update({'ekn': fekn})
    except:
        pass


    doc = docxtpl.DocxTemplate(templ)
    try:
        context = {}
        before_1 = fl['photo_before_1']
        relative_path_1c = PhotoFinder(before_1)
        insert_image1c = docxtpl.InlineImage(doc, relative_path_1c, width=Mm(80))
        context.update({"img1c": insert_image1c})
    except:
        pass
        # print('Не введен номер фотографии "образец 1 до испытания"')
    try:
        before_2 = fl['photo_before_2']
        relative_path_2c = PhotoFinder(before_2)
        insert_image2c = docxtpl.InlineImage(doc, relative_path_2c, width=Mm(80))
        context.update({"img2c": insert_image2c})
    except:
        pass
        # print('Не введен номер фотографии "образец 2 до испытания"')
    try:
        before_3 = fl['photo_before_3']
        relative_path_3c = PhotoFinder(before_3)
        insert_image3c = docxtpl.InlineImage(doc, relative_path_3c, width=Mm(80))
        context.update({"img3c": insert_image3c})
    except:
        pass
        # print('Не введен номер фотографии "образец 3 до испытания"')
    try:
        after_1 = fl['photo_after_1']
        relative_path_4c = PhotoFinder(after_1)
        insert_image4c = docxtpl.InlineImage(doc, relative_path_4c, width=Mm(80))
        context.update({"img4c": insert_image4c})
    except:
        pass
        # print('Не введен номер фотографии "образец 1 после испытания"')
    try:
        after_2 = fl['photo_after_2']
        relative_path_5c = PhotoFinder(after_2)
        insert_image5c = docxtpl.InlineImage(doc, relative_path_5c, width=Mm(80))
        context.update({"img5c": insert_image5c})
    except:
        pass
        # print('Не введен номер фотографии "образец 2 после испытания"')
    try:
        after_3 = fl['photo_after_3']
        relative_path_6c = PhotoFinder(after_3)
        # print(relative_path_6c)
        insert_image6c = docxtpl.InlineImage(doc, relative_path_6c, width=Mm(80))
        context.update({"img6c": insert_image6c})
    except:
        pass
        # print('Не введен номер фотографии "образец 2 после испытания"')

    try:
        relative_path_1 = fl['temperature_graph_1']
        insert_image1 = docxtpl.InlineImage(doc, relative_path_1, width=Mm(160))
        context.update({"img1": insert_image1})
    except:
        pass
    try:
        relative_path_2 = fl['temperature_graph_2']
        insert_image2 = docxtpl.InlineImage(doc, relative_path_2, width=Mm(160))
        context.update({"img2": insert_image2})
    except:
        pass

    try:
        relative_path_3 = fl['temperature_graph_3']
        insert_image3 = docxtpl.InlineImage(doc, relative_path_3, width=Mm(160))
        context.update({"img3": insert_image3})
    except:
        pass
        # print(f'что-то здесь не так 3: {e}')
    try:
        d = fl | context
        # print(d)
        doc.render(d)
    except:
        doc.render(fl)


    sg = str(out_file_name + suffix + '.docx')
    out_report = os.path.abspath(os.path.join('.', 'out', str(out_num), sg))
    p = doc.save(out_report)
    return p