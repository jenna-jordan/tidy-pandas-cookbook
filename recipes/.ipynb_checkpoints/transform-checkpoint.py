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