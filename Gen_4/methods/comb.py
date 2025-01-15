from operator import length_hint
from ..service.dictator import *
from ..service.routes import *


class Combustion:
    __G1 = 'Г1'
    __G2 = 'Г2'
    __G3 = 'Г3'
    __G4 = 'Г4'
    indicator = {}

    def __init__(self, smog_temp, length):

        self.smog_temp = smog_temp
        self.length = length
        # self.mass_loss = mass_loss
        # self.comb_time = comb_time
        # self.drops = drops

    def smog_indicator(self):
        if self.smog_temp <= 450:
            self.indicator.update({'smog_indicator': self.__G3})
            return self.indicator
        if self.smog_temp <= 235:
            self.indicator.update({'smog_indicator': self.__G2})
            return self.indicator
        if self.smog_temp <= 135:
            self.indicator.update({'smog_indicator': self.__G1})
            return self.indicator
        if self.smog_temp > 450:
            self.indicator.update({'smog_indicator': self.__G4})
            return self.indicator

    def length_indicator(self):
        if self.length <= 85:
            self.indicator.update({'smog_indicator': self.__G2})
            return self.indicator
        if self.length <= 65:
            self.indicator.update({'smog_indicator': self.__G1})
            return self.indicator
        if self.length > 85:
            self.indicator.update({'smog_indicator': self.__G3})
            return self.indicator


def combustor(x):
    dict_3 = dict_creator(comb_book, ['ID', 'series_num'], x)
    # print(dict_3)
    dict_3 = average_exp(dict_3, ['len_1', 'len_2', 'len_3', 'len_4'], 'mean_len_exp')
    # print(dict_3)
    dict_3 = average_gen(dict_3, 'mean_len_exp', 'mean_len_gen')
    # print(dict_3)
    dict_3 = differences(dict_3, ['mass_before', 'mass_after'], 'mass_loss')
    # print(dict_3)
    dict_3 = average_gen(dict_3, 'mass_loss', 'mass_loss_gen')
    # print(dict_3)
    dict_3 = average_gen(dict_3, 'combustion_time', 'combustion_time_gen')
    # print(dict_3)
    dict_3 = search_value(dict_3, 'burning_drops', 'burning_drops_gen', 'Да', 'Да', 'Нет')
    # print(dict_3)
    d_3id1 = dict_3['exp_date'][1]
    d_3id2 = dict_3['place'][1]
    # print(d_3id1)
    # print(d_3id2)
    dict_4 = dict_creator(amb_book, ['exp_date', 'place'], d_3id1)
    # print(dict_4)
    dict_4 = flatten_simple(dict_4, ['amb_temp', 'amb_pres', 'amb_moist'])
    # print(dict_4)
    dict_3 = dict_unition(dict_4, dict_3, 'comb')
    # print(dict_3)
    return dict_3

