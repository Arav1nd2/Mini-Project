#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 12:38:08 2020

@author: aravind
"""

import os
import sys
import pandas as pd


def extractor(op_type):
    output_directory = './Glottal/Output/'
    time_cols = ['OQ1', 'OQ2', 'NAQ', 'AQ', 'ClQ', 'OQa', 'QOQ', 'SQ1', 'SQ2']
    # freq_cols = ['DH12', 'HRF', 'PSP']

    output = pd.DataFrame()
    for filename in os.listdir(output_directory + '{}/'.format(op_type)):
        # time
        time_path = output_directory + \
            '/{}/'.format(op_type) + filename + '/time'
        freq_path = output_directory + \
            '/{}/'.format(op_type) + filename + '/freq'
        time_names = [time_path + '/' + i for i in os.listdir(time_path)]
        freq_names = [freq_path + '/' + i for i in os.listdir(freq_path)]
        time_params = {}
        freq_params = {}
        if len(time_names) > 0:
            time_df = pd.concat([pd.read_csv(f) for f in time_names])
            for c in time_cols:
                time_params[c + "_mean"] = time_df[c].mean()
                time_params[c + "_median"] = time_df[c].median()
                time_params[c + "_min"] = time_df[c].min()
                time_params[c + "_max"] = time_df[c].max()
                time_params[c + "_std"] = time_df[c].std()
                time_params[c + "_skew"] = time_df[c].skew()
                time_params[c + "_kurt"] = time_df[c].kurt()
        if len(freq_names) > 0:
            freq_df = pd.concat([pd.read_csv(f) for f in freq_names])
            _psp = [freq_df[c].mean()
                    for c in freq_df.columns if c != 'DH12' or c != 'HRF']
            psp = [x for x in _psp if str(x) != 'nan']
            if len(psp) > 0:
                freq_params['PSP'] = sum(psp) / len(psp)
            freq_params['HRF'] = freq_df['HRF'].mean()
            freq_params['DH12'] = freq_df['DH12'].mean()
        all_params = {**time_params, **freq_params}
        all_params['filename'] = op_type + filename
        all_params['label'] = 1 if op_type == 'D' else 0
        output = output.append(all_params, ignore_index=True)
    return output


def glottal_features(op_dir='.'):
    if os.path.isdir("./Glottal/Audio/D") and os.path.isdir("./Glottal/Audio/ND"):
        os.system(
            'matlab -nodisplay -nosplash -nodesktop -r "run(\'./Glottal/extracter.m\');exit;" | tail -n +11')

        D_df = extractor('D')
        nD_df = extractor('ND')

        op = pd.concat([D_df, nD_df])
        op.to_csv(op_dir + '/Glottal.csv')
        print('Glottal features saved to {}'.format(op_dir + '/Glottal.csv'))
        return op

    else:
        print("Error! Dataset not found!")
        sys.exit()
