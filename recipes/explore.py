import pandas as pd
import numpy as np
from itertools import combinations

# recipes for exploring datasets

def find_candidate_keys(df, max_columns=3):
    candidate_keys = []
    columns = df.columns.tolist()
    column_powerset = []
    # generate power set of columns
    for i in range(max_columns):
        combo = combinations(columns, i+1)
        column_powerset.extend(combo)
    # test elements in powerset
    for combo in column_powerset:
        ck = False
        if df[list(combo)].duplicated().sum() == 0:
            ck = True
            for k in candidate_keys:
                if set(combo).issuperset(set(k)):
                    ck = False
        if ck:
            candidate_keys.append(combo)
            
    return candidate_keys


def find_dependent_columns(df, key:list):
    dependent_columns = []
    columns = df.columns.tolist()
    # remove key columns from list of columns to check
    for k in key:
        columns.remove(k)
    # check if each column as 0 or 1 unique values per key value
    for c in columns:
        ue = df.groupby(key)[c].nunique().unique().tolist()
        if (ue == [1]) or (ue == [0]) or (ue == [0, 1]):
            dependent_columns.append(c)
    
    return dependent_columns


def find_no_variance_columns(df):
    no_var_columns = []
    columns = df.columns.tolist()
    for c in columns:
        if df[c].nunique() in [0, 1]:
            no_var_columns.append(c)
    
    return no_var_columns


def find_low_variance_columns(df, threshold:int):
    low_var_columns = []
    columns = df.columns.tolist()
    for c in columns:
        if 1 < df[c].nunique() <= threshold:
            low_var_columns.append((c, df[c].nunique()))
    
    return low_var_columns