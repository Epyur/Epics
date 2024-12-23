from exp.outs.cheker import *

while int(len(new_writes())) > 0:

    print(shs)
    # записываем данные в строку таблицы
    for c in range(0, len(shs)):
        sheet_base.cell(row=er, column=c + 1).value = shs[c]
        base_book.save('../БИ4.xlsx')
    break
