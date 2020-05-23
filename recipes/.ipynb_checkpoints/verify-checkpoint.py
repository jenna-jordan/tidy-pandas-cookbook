import pandas as pd
import numpy as np

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