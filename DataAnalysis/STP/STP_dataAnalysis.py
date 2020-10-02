
import numpy as np


def rescaleDataset(df, SCA):
    df['i_rer'] = df['i_rer'] / SCA
    df['i_ren'] = df['i_ren']
    df['i_rsg'] = df['i_rsg'] / SCA
    df['i_fic'] = df['i_fic'] / SCA
    df['i_gsv'] = df['i_gsv'] / SCA
    df['i_grp'] = df['i_grp']
    return df


def getBoolIxFromFeatKey(df, key, FEATS):
    matches = [list(np.isclose(df[feat], key[feat])) for feat in FEATS]
    ixBool = [all(row) for row in list(zip(*matches))]
    return ixBool
