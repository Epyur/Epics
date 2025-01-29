from ..service.dictator import *

group = {'Г1': 4, 'Г2': 3, 'Г3': 2, 'Г4': 1}
ignition_group = {'В1': 3, 'В2': 2, 'В3': 1}
propogation_group = {'РП1': 4, 'РП2': 3, 'РП3': 2, 'РП4': 1}

def group_compare(dict2, aim_ind, real_indicator, group_dict):
    a_i = dict2[aim_ind]
    if group_dict[a_i] <= group_dict[real_indicator]:
        p = 'Соответствует'
    else:
        p = 'Не соответствует'
    return p