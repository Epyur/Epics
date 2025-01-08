import numpy as np
import os
from .connector import *
from .names import *

def calculator(x):
    df = inc_df_merged_comb_flam.loc[x].copy()
    def filler(donor, recepient):
        if df[recepient] is np.nan:
            func = df[donor]
            df[recepient] = func
            return df
    filler('product_name_y', 'product_name_x')
    filler('thickness_y', 'thickness_x')
    filler('description_y', 'description_x')
    filler('aim_cvality', 'comb_group')

    def srednee(start, finish, control, recepient):
        if df[control] is not np.nan:
            sery = df[start:finish].tolist()
            midl_len = sum(sery) / len(sery)
            midl_len_round = np.round(midl_len, decimals=2)
            df[recepient] = midl_len_round
        return df
    srednee('len_1_x', 'len_4_x', 'sery_x', 'middle_len_x')
    srednee('len_1_y', 'len_4_y', 'sery_y', 'middle_len_y')
    srednee('len_1', 'len_4', 'sery', 'middle_len')

    def mass_loss(start, finish, control, recepient):
        if df[control] is not np.nan:
            m_before = df[start]
            m_after = df[finish]
            m_loss = 100 - 100 * m_after / m_before
            m_loss_round = np.round(m_loss, decimals=2)
            df[recepient] = m_loss_round
        return df
    mass_loss('mass_before_x', 'mass_after_x', 'sery_x', 'mass_los_x')
    mass_loss('mass_before_y', 'mass_after_y', 'sery_y', 'mass_los_y')
    mass_loss('mass_before', 'mass_after', 'sery', 'mass_los')


    def gen_sr_znach(a, b, c, recepient):
        x = df[a]
        y = df[b]
        z = df[c]
        sr = (x + y + z) / 3
        sr_round = np.round(sr, decimals=2)
        df[recepient] = sr_round
        return df
    gen_sr_znach('middle_len_x', 'middle_len_y', 'middle_len', 'gen_middle_len')
    gen_sr_znach('temp_of_smog_x', 'temp_of_smog_y', 'temp_of_smog', 'gen_smog_temp')
    gen_sr_znach('combustion_time_x', 'combustion_time_y', 'combustion_time', 'gen_combustion_time')
    gen_sr_znach('mass_los_x', 'mass_los_y', 'mass_los', 'gen_middle_mass_los')

    def bubbles():
        if df['flame_bubles_x'] == 'Да':
            df['gen_babble'] = 'Да'
        if df['flame_bubles_y'] == 'Да':
            df['gen_babble'] = 'Да'
        if df['flame_bubles'] == 'Да':
            df['gen_babble'] = 'Да'
        else:
            df['gen_babble'] = 'Нет'
        return df
    bubbles()

    def smog_group(temp, recepient):
        if df[temp] <= 450:
            df[recepient] = 'Г3'
        if df[temp] <= 235:
            df[recepient] = 'Г2'
        if df[temp] <= 135:
            df[recepient] = 'Г1'
        if df[temp] > 450:
            df[recepient] = 'Г4'
        return df
    smog_group('temp_of_smog_x', 'group_by_smog_temp_x')
    smog_group('temp_of_smog_y', 'group_by_smog_temp_y')
    smog_group('temp_of_smog', 'group_by_smog_temp')
    smog_group('gen_smog_temp', 'gen_group_by_smog_temp')

    def len_group(lenth, recepient):
        if df[lenth] <= 85:
            df[recepient] = 'Г2'
        if df[lenth] <= 65:
            df[recepient] = 'Г1'
        if df[lenth] > 85:
            df[recepient] = 'Г3'
        return df
    len_group('middle_len_x', 'group_by_len_x')
    len_group('middle_len_y', 'group_by_len_y')
    len_group('middle_len', 'group_by_len')
    len_group('gen_middle_len', 'gen_group_by_len')

    def mass_group(mass, recepient):
        if df[mass] <= 50:
            df[recepient] = 'Г2'
        if df[mass] <= 20:
            df[recepient] = 'Г1'
        if df[mass] > 50:
            df[recepient] = 'Г3'
        return df
    mass_group('mass_los_x', 'group_by_mass_los_x')
    mass_group('mass_los_y', 'group_by_mass_los_y')
    mass_group('mass_los', 'group_by_mass_los')
    mass_group('gen_middle_mass_los', 'gen_group_by_mass_los')

    def time_group(time, recepient):
        if df[time] <= 300:
            df[recepient] = 'Г3'
        if df[time] <= 30:
            df[recepient] = 'Г2'
        if df[time] == 0:
            df[recepient] = 'Г1'
        if df[time] > 300:
            df[recepient] = 'Г4'
        return df
    time_group('combustion_time_x', 'group_by_combustion_x')
    time_group('combustion_time_y', 'group_by_combustion_y')
    time_group('combustion_time', 'group_by_combustion')
    time_group('gen_combustion_time', 'gen_group_by_combustion')

    def buble_group(buble, recepient):
        if df[buble] == 'Нет':
            df[recepient] = 'Г1'
        if df[buble] == 'Да':
            df[recepient] = 'Г4'
        return df
    buble_group('flame_bubles_x', 'group_by_buble_x')
    buble_group('flame_bubles_y', 'group_by_buble_y')
    buble_group('flame_bubles', 'group_by_buble')
    buble_group('gen_babble', 'gen_group_by_buble')

    def comb_group(start, finish, recepient):
        sery = df[start:finish].tolist()
        if 'Г2' in sery:
            df[recepient] = 'Г2'
        if 'Г3' in sery:
            df[recepient] = 'Г3'
        if 'Г4' in sery:
            df[recepient] = 'Г4'
        else:
            df[recepient] = 'Г1'
        return df
    comb_group('gen_group_by_smog_temp', 'gen_group_by_buble', 'gen_comb_group')

    def group_sootv(result, etalon, recepient):
        if df[result] <= df[etalon]:
            df[recepient] = 'Соответствует'
        else:
            df[recepient] = 'Не соответствует'
        return df
    group_sootv('gen_comb_group', 'comb_group', 'gen_match')

    return df
