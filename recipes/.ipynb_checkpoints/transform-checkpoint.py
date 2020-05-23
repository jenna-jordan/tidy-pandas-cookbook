import pandas as pd
import numpy as np

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