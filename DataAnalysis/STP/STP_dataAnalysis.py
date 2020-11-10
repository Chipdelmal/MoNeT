
import numpy as np
import pandas as pd


def unifySexesDataframe(dfRC, EXPS, FEATS, LBLS):
    df = pd.DataFrame(columns=['i_sex']+FEATS+LBLS)
    for i in range(len(EXPS)):
        dfTemp = dfRC[EXPS[i]]
        for j in range(dfTemp.shape[0]):
            row = dict(dfTemp.iloc[j])
            row['i_sex'] = EXPS[i]
            df = df.append(row, ignore_index=True)
    return df


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


def zeroDivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def errorBetweenDataframes(dfB, dfP, FEATS, LABELS, error=True):
    dfO = dfB.copy()
    for i in range(dfB.shape[0]):
        sliceKey = dfB.iloc[i][FEATS]
        outB = dfB.iloc[i][LABELS].values
        boolFltr = getBoolIxFromFeatKey(dfP, sliceKey, FEATS)
        outP = dfP[boolFltr][LABELS].values
        if error:
            diff = zeroDivide(outP, outB)
        else:
            diff = zeroDivide(outP - outB, 1)
        dfO.iloc[boolFltr.index(True)] = list(sliceKey) + list(diff[0])
    return dfO
