from ..service.dictator import *
from ..service.routes import *
from .indicators import *

def prop_indicator(krit):
    if krit < 11:
        p = "РП2"
    if krit <= 8:
        p = "РП3"
    if krit <= 5:
        p = "РП4"
    if krit >= 11:
        p = "РП1"
    return p

def propagator(x, dict2=None):
    dict_4 = dict_creator(flam_book, ['ID', 'sampels_num'], x)
    if dict_4 is False:
        False
    else:
        c = exp_counter(dict_4, 'exp_id')
        dict_4.update({'product_number': c})

        kptp = sorter_2(dict_4, 'ptp', 'ignition_fact')
        dict_4.update({'kptp': kptp})

        gr = prop_indicator(kptp)
        dict_4.update({'group': gr})

        compare = group_compare(dict2, 'flam_indicator', gr, ignition_group)
        dict_4.update({'compare': compare})

        d_3id1 = dict_4['exp_date'][1]
        d_3id2 = dict_4['place'][1]
        list1 = [d_3id1, d_3id2]
        dict_5 = dict_creator(amb_book, ['exp_date', 'place'], d_3id1)
        dict_5 = deleter(dict_5, d_3id2)
        dict_5 = flatten_simple(dict_5, ['amb_temp', 'amb_pres', 'amb_moist'])
        dict_4 = dict_unition(dict_5, dict_4)
    return dict_4