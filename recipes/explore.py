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


def find_dependent_columns(df, key:list, drop_no_variance=True):
    dependent_columns = []
    columns = df.columns.tolist()
    if drop_no_variance:
        no_var_columns = find_no_variance_columns(df)
        if no_var_columns:
            for c in no_var_columns:
                columns.remove(c)
    for k in key:
        columns.remove(k)
    for c in columns:
        unique_elements = df.groupby(key)[c].nunique().unique().tolist()
        if (unique_elements == [1]) or (unique_elements == [0]) or (unique_elements == [0, 1]) or (unique_elements == [1, 0]):
            dependent_columns.append(c)
    
    return dependent_columns