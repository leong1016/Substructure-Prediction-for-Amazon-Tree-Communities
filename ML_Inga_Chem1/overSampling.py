__author__ = 'Yulong Liang'

import numpy as np
import pandas as pd


def duplicateMinority(df, labelStart, labelEnd, max_round=100):
    
    newdf = df.copy()
    t = 1
    
    while t < max_round:
        
        labels = newdf.iloc[:,labelStart:labelEnd]
        stats = labels.sum()
        ratio = stats.max() / stats.min()
        print('Round: {}; Max/Min: {}'.format(t, ratio))
        
        if (ratio < 10):
            break;
        
        stats = labels.sum(axis=0)
        minValue = np.min(stats)
        minIndex = np.where(stats==minValue)
        minName = stats.index[minIndex]

        dupeIndex = []
        for name in minName:
            firstRow = np.where(labels[name]==1)[0][0]
            dupeIndex.append(firstRow)
        print(dupeIndex)
        dupeMatrix = newdf.iloc[dupeIndex]

        newdf = newdf.append(dupeMatrix)
        
        t = t + 1

    return newdf


if __name__ == '__main__':
    
    raw = pd.read_csv('training_cleaned.csv')
    stats = raw.iloc[:,23403:-1].sum()
    ratio = stats.max() / stats.min()
    print('max/min ratio before: {}'.format(ratio))
    
    newraw = duplicateMinority(raw, 23403, -1)
    newstats = newraw.iloc[:,23403:-1].sum()
    newratio = newstats.max() / newstats.min()
    print('max/min ratio after : {}'.format(newratio))