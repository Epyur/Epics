import numpy as np

from ..service.dictator import *
from ..service.routes import *
from .indicators import *
from ..service.tdt import dataframe_tdt


def smog_indicator(krit):
    if krit <= 450:
        p = "Г3"
    if krit <= 235:
        p = "Г2"
    if krit <= 135:
        p = "Г1"
    if krit > 450:
        p = "Г4"
    return p

def length_indicator(krit):
    if krit <= 85:
       p = "Г2"
    if krit <= 65:
        p = "Г1"
    if krit > 85:
        p = "Г3"
    return p

def mass_indicator(krit):
    if krit <= 50:
       p = "Г2"
    if krit <= 20:
        p = "Г1"
    if krit > 50:
        p = "Г3"
    return p

def time_indicator(krit):
    if krit <= 300:
        p = "Г3"
    if krit <= 30:
        p = "Г2"
    if krit == 0:
        p = "Г1"
    if krit > 300:
        p = "Г4"
    return p

def drops_indicator(krit):
    if krit == 'Нет':
        p = "Г1"
    if krit == 'Да':
        p = 'Г4'
    return p


def combustor(x, dict2=None):
    dict_3 = dict_creator(comb_book, ['ID', 'series_num'], x)
    if dict_3 is False:
        False
    else:
        c = exp_counter(dict_3, 'exp_id') * 4
        dict_3.update({'product_number': c})
            # добавляем данные о дыме
        # print(dict_3['tp1_smog'][1])
        if np.isnan(dict_3['tp1_smog'][1]):
            g = 'temp_of_smog'
        else:
            g = ['tp1_smog', 'tp2_smog', 'tp3_smog', 'tp4_smog']
        dict_3 = average_exp(dict_3, g, 'temp_of_smog','comb_indicator',
                             dict2=dict2, func=smog_indicator, func2=group_compare, name2='temp_of_smog_group',
                             name3='temp_of_smog_compare', group_dict=group)
        # print(dict_3)
        dict_3 = average_gen(dict_3, 'temp_of_smog', 'mean_temp_of_smog_gen', 'comb_indicator', dict2=dict2,
                             func=smog_indicator, func2=group_compare, name2='mean_temp_of_smog_group',
                             name3='mean_temp_of_smog_compare', group_dict=group)
        # добавляем данные о длине повреждений
        # print(dict_3)
        dict_3 = average_exp(dict_3, ['len_1', 'len_2', 'len_3', 'len_4'], 'mean_len_exp', 'comb_indicator',
                             dict2=dict2, func=length_indicator, func2=group_compare, name2='mean_len_group', name3='mean_len_compare', group_dict=group)
        # print(dict_3)
        dict_3 = average_gen(dict_3, 'mean_len_exp', 'mean_len_gen','comb_indicator', dict2=dict2, func=length_indicator,
                             func2=group_compare, name2='mean_len_gen_group', name3='mean_len_gen_compare', group_dict=group)
        # print(dict_3)
        dict_3 = differences(dict_3, ['mass_before', 'mass_after'], 'mass_loss')
        # print(dict_3)
        dict_3 = average_gen(dict_3, 'mass_loss', 'mass_loss_gen','comb_indicator', dict2=dict2, func=mass_indicator,
                             func2=group_compare, name2='mass_loss_gen_group', name3='mass_loss_gen_compare', group_dict=group)
        dict_3 = estimation(dict_3, 'mass_loss', 'mass_loss_group', 'comb_indicator', dict2=dict2,
                            func=mass_indicator, func2=group_compare, name2='mass_loss_group_compare', group_dict=group)
        # print(dict_3)
        dict_3 = estimation(dict_3, 'combustion_time', 'combustion_time_group', 'comb_indicator', dict2=dict2,
                             func=time_indicator, func2=group_compare, name2='combustion_time_group_compare', group_dict=group)
        dict_3 = average_gen(dict_3, 'combustion_time', 'combustion_time_gen','comb_indicator', dict2=dict2, func=time_indicator,
                             func2=group_compare, name2='combustion_time_gen_group', name3='combustion_time_gen_compare', group_dict=group)
        # print(dict_3)
        dict_3 = search_value(dict_3, 'burning_drops', 'burning_drops_gen', 'Да', 'Да', 'Нет')
        # print(dict_3)
        dict_3 = estimation(dict_3, 'burning_drops', 'burning_drops_group', 'comb_indicator', dict2=dict2,
                            func=drops_indicator, func2=group_compare, name2='burning_drops_group_compare', group_dict=group)
        dict_3 = estimation_lite(dict_3, 'burning_drops_gen', 'burning_drops_gen_group', 'comb_indicator', dict2=dict2,
                            func=drops_indicator, func2=group_compare, name2='burning_drops_gen_compare', group_dict=group)
        dict_3 = compare_lite(dict_3, ['mean_temp_of_smog_group', 'mean_len_gen_group', 'mass_loss_gen_group',
                                       'combustion_time_gen_group', 'burning_drops_gen_group'], 'gen_comb_group',
                              'comb_indicator', dict2=group, dict3=dict2, func=group_compare, name2='gen_comb_compare', group_dict=group)
        d_3id1 = dict_3['exp_date'][1]
        d_3id2 = dict_3['place'][1]
        list1 = [d_3id1, d_3id2]
        dict_4 = dict_creator(amb_book, ['exp_date', 'place'], d_3id1)
        dict_4 = deleter(dict_4, d_3id2)
        dict_4 = flatten_simple(dict_4, ['amb_temp', 'amb_pres', 'amb_moist'])
        dict_3 = dict_unition(dict_4, dict_3, 'comb')

        """
        Обрабатываем данные термодата
        """
        # формируем Датафрейм из файла термодата
        df = dataframe_tdt(dict_3, 700, x)
        
        dict_3 = dict_3 | df

    return dict_3

