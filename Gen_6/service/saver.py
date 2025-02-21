import docxtpl
from docx.shared import Mm

from .dictator import flatten_dict
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
        relative_path_1 = fl['temperature_graph_1']
        insert_image1 = docxtpl.InlineImage(doc, relative_path_1, width=Mm(160))
        context.update({"img1": insert_image1})
    except:
        pass
    try:
        relative_path_2 = fl['temperature_graph_2']
        insert_image2 = docxtpl.InlineImage(doc, relative_path_2, width=Mm(160))
        context.update({"img2": insert_image2})
    except Exception as e:
        print(f'что-то здесь не так 2: {e}')

    try:
        relative_path_3 = fl['temperature_graph_3']
        insert_image3 = docxtpl.InlineImage(doc, relative_path_3, width=Mm(160))
        context.update({"img3": insert_image3})
    except Exception as e:
        print(f'что-то здесь не так 3: {e}')
    try:
        d = fl | context
        doc.render(d)
    except:
        doc.render(fl)


    sg = str(out_file_name + suffix + '.docx')
    out_report = os.path.abspath(os.path.join('.', 'out', str(out_num), sg))
    p = doc.save(out_report)
    return p