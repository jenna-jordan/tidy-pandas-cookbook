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


# recipes to transform datasets


def split_lists(df, pk_columns:list, list_column:str, delim=","):
    new_df = df[pk_columns + [list_column]].copy()
    new_df[list_column] = df[list_column].str.split(pat=delim)
    new_df_exploded = new_df.explode(list_column).dropna().reset_index(drop=True)
    return new_df_exploded


def de_dummify(df, pk_columns:list, dummy_columns:list, col_name:str):
    new_df = df[pk_columns + dummy_columns].copy()
    # propogate the category/column name for rows where it is true
    for c in dummy_columns:
        new_df[c] = np.where(new_df[c]==1, c, None)
    # create a list out of the categories, and explode/melt the list
    new_df[col_name] = new_df[dummy_columns].values.tolist()
    new_df = new_df.drop(columns=dummy_columns).explode(col_name).dropna()
    return new_df


def decompose_table(df, primary_key:list):
    # find which columns belong in this table
    table_columns = set(find_dependent_columns(df, primary_key))
    if len(primary_key) > 1:
        for column in primary_key:
            dependent_cols = set(find_dependent_columns(df, [column]))
            table_columns -= dependent_cols
    # create the new table
    new_df = df[primary_key + list(table_columns)].copy().dropna(subset=primary_key).drop_duplicates().reset_index(drop=True)
    return new_df


# recipes to verify specified constraints in datasets


def check_ids_ref_integrity(primary_df, pdf_id:str, related_df, rdf_fk:list or str, verbose = False):
    if type(rdf_fk) == str:
        rdf_fk = [rdf_fk]
    
    ref_integrity = True
    missing_ids = set()
    
    p_ids = set(primary_df[pdf_id].dropna().unique())
    for c in rdf_fk:
        f_ids = set(related_df[c].dropna().unique())
        diff = f_ids - p_ids
        if len(diff):
            ref_integrity = False
            missing_ids.update(diff)
    
    if verbose:
        return missing_ids
    else:
        return ref_integrity

    
def check_key_uniqueness(df, key:list):
    orig_rows = len(df)
    mod_df = df.drop_duplicates(subset=key)
    mod_rows = len(mod_df)
    if orig_rows == mod_rows:
        return True
    else:
        return False