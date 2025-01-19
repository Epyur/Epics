from .dictator import flatten_dict
from .routes import *

def report_to_excel(dict1, out_file_name):
    df = dict1.copy()
    zf = pd.DataFrame(list(df.items()))
    dd = str(out_file_name + '.xlsx')
    out_book = os.path.abspath(os.path.join('.', 'out', dd))
    ds = zf.to_excel(out_book)
    return ds


def report_to_word(dict1, templ, out_file_name, suffix):
    fl = flatten_dict(dict1)
    doc = DocxTemplate(templ)
    doc.render(fl)
    sg = str(out_file_name + suffix + '.docx')
    out_report = os.path.abspath(os.path.join('.', 'out', sg))
    p = doc.save(out_report)
    return p