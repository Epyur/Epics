def group_compare(litera, aim_ind, real_indicator):
    try:
        if litera in aim_ind:
            if litera in real_indicator:
                if aim_ind >= real_indicator:
                    p = 'Соответствует'
                else:
                    p = 'Не соответствует'
            else:
                p = f'Невозможно сравнить {real_indicator} c {aim_ind}'
        else:
            p = 'Введенный показатель не соответствует указаной литере'
    except:
        p = 'н/у'
    return p

def FindeWorsest(litera, comb_list):
    l1 = []

    for i in comb_list:
        if litera in i:
            l1.append(i)
    if len(l1) == len(comb_list):
            p = max(l1)

    else:

        p = 'Не может быть проведена оценка на основании представленного набора показателей'

    return p

