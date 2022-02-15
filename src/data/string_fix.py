
# encoding: windows-1254

from unidecode import unidecode
import numpy as np
import pandas as pd


def decoding_fix_dict(initial: np.ndarray, target: np.ndarray) -> dict: 
    """
    Return a dictionary object that will replace and fix a given list of strings. 
    WARNING: Strip like operations must be done beforehand.

    params: 
    initial: an array contains strings to be fixed
    target: an array contains strings that will be replaced with the array 'initial'

    """

    vfunc = np.vectorize(lambda x, y: unidecode(x) == unidecode(y))
    distance_matrix = vfunc(target, initial)
    df_distance = pd.DataFrame(distance_matrix, columns=target, index=initial.flatten())
    mtrx = df_distance.stack().reset_index().rename(columns={'level_0': 'initial', 'level_1': 'target', 0: 'match'})
    mtrx['dup_key'] = mtrx.apply(lambda x: ' - '.join(sorted([x['target'], x['initial']])), axis=1)
    mtrx.index = mtrx.index.astype('str')
    mtrx = mtrx.drop_duplicates(subset=['dup_key']).drop(columns=['dup_key'])
    mtrx = mtrx.query("initial != target")
    fix_dict = mtrx.query('match == True').drop(columns=['match'])
    fix_dict = fix_dict.set_index('initial')['target'].to_dict()
    return fix_dict


