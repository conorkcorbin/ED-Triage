# Developed by Gautam Machiraju

import pandas as pd
import numpy as np
import collections
import math


def preprocess_and_filter(df, feat_type):
    if feat_type == "labs":
        time_col = "result_time_jittered_utc"
        feat_col = "lab_name"
        data_col = ["ord_value"]
        feat_map = {"Glucose by Meter":"glucose_by_meter",
                    "Sodium, Ser/Plas":"sodium_plas", "Sodium,Ser/Plas":"sodium_plas",
                    "Potassium, Ser/Plas":"potassium_plas", "Potassium,Ser/Plas":"potassium_plas",
                    "Magnesium, Ser/Plas":"magnesium_plas", "Magnesium,Ser/Plas":"magnesium_plas",
                    "Albumin, Ser/Plas":"albumin_plas", "Albumin,Ser/Plas":"albumin_plas",
                    "Creatinine, Ser/Plas":"creatinine_plas", "Creatinine,Ser/Plas":"creatinine_plas",
                    "BUN, Ser/Plas":"bun_plas", "BUN,Ser/Plas":"bun_plas",
                    "CO2, Ser/Plas":"co2_plas", "CO2,Ser/Plas":"co2_plas",
                    "Anion Gap":"anion_gap",
                    "Glucose, Ser/Plas":"glucose_plas", "Glucose,Ser/Plas":"glucose_plas",
                    "AST (SGOT), Ser/Plas":"ast_plas", "AST (SGOT),Ser/Plas":"ast_plas",
                    "ALT (SGPT), Ser/Plas":"alt_plas", "ALT (SGPT),Ser/Plas":"alt_plas",
                    "Total Bilirubin, Ser/Plas":"total_bilirubin_plas", "Total Bilirubin,Ser/Plas":"total_bilirubin_plas",
                    "Platelet count":"platelet_count",
                    "Hemoglobin":"hemoglobin",
                    "WBC":"wbc",
                    "Neutrophil, Absolute":"neutrophil_abs", "Neutrophil,Absolute":"neutrophil_abs"}
        df[feat_col].replace(feat_map, inplace=True)
        rows_keep = ["glucose_by_meter",
                    "sodium_plas",
                    "potassium_plas",
                    "magnesium_plas",
                    "albumin_plas",
                    "creatinine_plas",
                    "bun_plas",
                    "co2_plas",
                    "anion_gap",
                    "glucose_plas",
                    "ast_plas",
                    "alt_plas",
                    "total_bilirubin_plas",
                    "platelet_count",
                    "hemoglobin",
                    "wbc",
                    "neutrophil_abs"]
    
    elif feat_type == "flowsheet":
        time_col = "recorded_time" # "recorded_time_jittered_utc"
        feat_col = "features" # old: "row_disp_name"
        data_col = ["values"] # old: ["num_value1", "num_value2"]
        rows_keep = "all"
#         feat_map = {"BP":"blood_pressure", "NIBP":"blood_pressure", "Resting BP":"blood_pressure",
#                     "Pulse":"pulse", "Heart Rate":"pulse", "Resting HR":"pulse",
#                     "Resting RR":"respiratory_rate", "Resp Rate":"respiratory_rate", "Resp":"respiratory_rate",
#                     "SpO2":"o2_saturation", "Resting SpO2":"o2_saturation",
#                     "O2": "o2_used"}
        feat_map = {"Pulse":"pulse", "Heart Rate":"pulse", "Resting HR":"pulse",
                    "Resting RR":"respiratory_rate", "Resp Rate":"respiratory_rate", "Resp":"respiratory_rate",
                    "SpO2":"o2_saturation", "Resting SpO2":"o2_saturation",
                    "O2": "o2_used"}
        df[feat_col].replace(feat_map, inplace=True)
        
    # filter columns
    df["jc_csn"] = df["jc_uid"] + ":" + df["pat_enc_csn_id_coded"].astype(str) # merge the two
    cols_keep = ["jc_csn", time_col, feat_col] + data_col
    df = df[cols_keep]
    
    # filter rows for labs
    if rows_keep != "all":
        df = df[df[feat_col].isin(rows_keep)]
           
    # ensure data types for each col (clean the weird entries that can't be cast to float64)
    new_data_col = []
    for col in data_col:
        clean_col_data = []
        col_data = list(df[col].copy()) # deep copy
        for el in col_data:
            try:
                new_el = np.float64(el)
            except ValueError:
                new_el = np.nan
            clean_col_data.append(new_el)
        
        # set column
        df.loc[:, col] = clean_col_data
        
        # below is old code to make new column name and rename to old names...
        # turns out this also thew the warning on the notebook
        
#     new_data_col.append(col+"_clean")
#     cols_keep = ["jc_csn", time_col, feat_col] + new_data_col
#     df = df[cols_keep]
#     # rename back to old cols
#     col_map = {}
#     for key,val in zip(new_data_col, data_col):
#         col_map[key] = val 
#     print(col_map)
#     df.rename(columns=col_map, inplace=True)
    
    return df


def separate_multiple_values(df, feat_type):
    # really only meant for flowsheet

    if feat_type == "flowsheet":
        #df = pd.melt(df, id_vars=["row_disp_name", "jc_csn", "recorded_time_jittered_utc"], value_vars=['num_value1', 'num_value2'])
        df = pd.melt(df, id_vars=["features", "jc_csn", "recorded_time"], value_vars=['values'])
        df.set_index("jc_csn", inplace=True)
#         df["flowsheet_name"] = df["row_disp_name"] + ":" + df["variable"]
        df["flowsheet_name"] = df["features"]
#         df = df[["recorded_time_jittered_utc",'flowsheet_name','value']]
        df = df[["recorded_time",'flowsheet_name','value']]
    else:
        df.set_index("jc_csn", inplace=True)
        print("\nLabs detected. Skipping step. This function is really only meant for flowsheet... Have a nice day!")
    
    return df


def custom_pivot(df, feat_type):
    if feat_type == "labs":
        feat_col = "lab_name"
        data_col = "ord_value"
        time_col = "result_time_jittered_utc"
    elif feat_type == "flowsheet":
        feat_col = "flowsheet_name"
        data_col = "value"
        time_col = "recorded_time"  #"recorded_time_jittered_utc"
    
    # new id based on instances
    seen = []
    new_ids = []
    jc_csns = df.index
    for jc_csn in jc_csns:
        if jc_csn not in seen:
            inst = 0
            new_id = jc_csn + "_" + str(inst)
            seen.append(jc_csn)
            new_ids.append(new_id)
        else:
            inst += 1
            new_id = jc_csn + "_" + str(inst)
            new_ids.append(new_id)
    df["jc_csn_num"] = new_ids 
    
    # perform pivot
    df = df.pivot_table(values=data_col, index=["jc_csn_num", time_col], columns=feat_col)
    
    return df


def postprocess_cleanup(df, feat_type):
    # IF ANY IS NEEDED
    if feat_type == "labs":
        # remove height and weight rows_drop = [""]
        pass
    elif feat_type == "flowsheet":
        pass

    
def binnify(df, num_bins, feat_type):
    
    if feat_type == 'labs':
        time_col = "result_time_jittered_utc"
    elif feat_type == "flowsheet":
        time_col = "recorded_time" #"recorded_time_jittered_utc"
    
    feat_names = list(df.columns)
    ids = list(df.index)
    
    # only apply binning to pre-2018
    df_held_out = df.loc[df.index.get_level_values(time_col) >= '2018-01-01']
    df_to_use = df.loc[df.index.get_level_values(time_col) < '2018-01-01']
    
    # labels/bin names
    lab = list(range(1,num_bins+1))
        
    cols = []
    for fn in feat_names:    
        # retbins allows us to retreive the mapping to apply to other data
        nc, bin_fn = pd.qcut(df_to_use[fn].rank(method="first"), q=num_bins, retbins=True, labels=lab) # added the rank("first")
        cols.append(nc)
    pre_2018 = pd.concat(cols, axis=1)
    
    # now add 2018-onwards
    new_cols = []
    for fn in feat_names:  
        new_nc = pd.cut(df_held_out[fn].rank(method="first"), bins=bin_fn, labels=lab)
        new_cols.append(new_nc)
    post_2018 = pd.concat(new_cols, axis=1)
    
    # stack both pre and post 2018
    out_df = pd.concat([pre_2018,post_2018], ignore_index=False)
    return out_df


def map_multihot(col):
    counts = [np.array(list(collections.Counter(sorted(row)).values()))-1 for row in col]
    return counts  

def map_remove_nans(col):
    no_nans = []
    for row in col:
        row_els = []
        for el in row:
            if math.isnan(el) == False:
                row_els.append(el)
        no_nans.append(row_els)
    return no_nans


def countify(quantized_df, num_bins):
    # creates a multi-hot representation of each feature
    
    # save for later
    feat_names = list(quantized_df.columns)
    
    # add new column of just jc_uid - what we'll group by
    quantized_df["jc_uid"] = quantized_df.index.get_level_values(0).str.split(pat=":").str[0]
    
    # group by to get every csn's counts together in a list
    # need to "pad" to create columns for each bin
    gb_padded = quantized_df.groupby("jc_uid").agg(lambda x: list(x) + list(range(1,21)))
#     print(gb_padded.head())
    
    # remove nans
    gb_padded = gb_padded.apply(map_remove_nans)
#     print(gb_padded.head())
    
    # ensure string index
    index_new = list(gb_padded.index)
    index_new = [str(idx) for idx in index_new]
   
    # mapping features_bins to columns
    feat_names_new = []
    bin_nums = list(range(1, num_bins+1))
    for fn in feat_names:
        if fn != "jc_uid":
            to_add = [fn + "_" + str(bn) for bn in bin_nums]
            feat_names_new.extend(to_add)

    # create multi-hot representation
    mapped_df = gb_padded.apply(map_multihot)
#     print(mapped_df.head())
    lol = mapped_df.values.tolist() # list of list
#     print("LOL", lol[0:10])
    
    # not suuuuper efficient, but here we are...
    new_rows = []
    for row in lol:
        new_row = []
        for l in row:
            new_row.extend(list(l))
        new_rows.append(new_row)
        
#     print(len(new_rows))
#     print(len(new_rows[0]))
#     print(len(feat_names_new))
    
    binned_feats_df = pd.DataFrame(new_rows, columns=feat_names_new)
    binned_feats_df["jc_uid"] = index_new
    binned_feats_df.set_index("jc_uid", inplace=True)
    
    return binned_feats_df


################################################
# SIMULATION SCRIPTS (CAN IGNORE AT THIS POINT)
################################################


def create_synthetic_data(feat_class, n, a, b):
    
    if feat_class == "vitals":
        feat_names = ["BP_High_Systolic", 
                      "BP_Low_Diastolic", 
                      "FiO2", 
                      "Glasgow Coma Scale Score",
                      "Pulse",
                      "Resp", 
                      "Temp", 
                      "Urine"]
        
    elif feat_class == "labs":
        feat_names = ['WBC',  # White Blood Cell
                      'HCT',  # Hematocrit
                      'PLT',  # Platelet Count
                      'NA',   # Sodium, Whole Blood
                      'K',    # Potassium, Whole Blood
                      'CO2',  # CO2, Serum/Plasma
                      'BUN',  # Blood Urea Nitrogen
                      'CR',   # Creatinine
                      'TBIL', # Total Bilirubin
                      'ALB',  # Albumin
                      'CA',   # Calcium
                      'LAC',  # Lactic Acid
                      'ESR',  # Erythrocyte Sedimentation Rate
                      'CRP',  # C-Reactive Protein
                      'TNI',  # Troponin I
                      'PHA',  # Arterial pH
                      'PO2A', # Arterial pO2
                      'PCO2A',# Arterial pCO2
                      'PHV',  # Venous pH
                      'PO2V', # Venous pO2
                      'PCO2V'] # Venous pCO2
    
    feat_names = ["CSN"] + feat_names
    p = len(feat_names)
    df = pd.DataFrame(np.random.randint(a,b,size=(p, n)).T, columns=feat_names)
    return df


def fetch_relevant_columns(query_df, feat_names):
    df = query_df[feat_names]
    return df


def quantize_sim(df, num_bins, id_header):
    feat_names = list(df.columns)
    ids = list(df[id_header])
    new_cols = []
    new_cols.append(ids)
    
    for fn in feat_names:
        if fn != id_header:
            nc = pd.qcut(df[fn], q=num_bins, labels=list(range(1,num_bins+1)))
            new_cols.append(nc)
    
    array = np.array(new_cols).T.tolist()
    out_df = pd.DataFrame(array, columns=feat_names)
    return out_df


def map_multihot_sim(col):
    counts = [np.array(list(collections.Counter(sorted(row)).values()))-1 for row in col]
    return counts  


def count_quantized_per_pt_sim(quantized_df, num_bins, id_header):
    # creates a multi-hot representation of each feature
    feat_names = list(quantized_df.columns)
    
    # group by to get every csn's counts together in a list
    # gb = quantized_df.groupby(id_header).agg(lambda x: list(x))
    gb_padded = quantized_df.groupby(id_header).agg(lambda x: list(x) + list(range(1,21)))
    
    index_new = list(gb_padded.index)
    index_new = [str(idx) for idx in index_new]
   
    feat_names_new = []
    bin_nums = list(range(1, num_bins+1))
    for fn in feat_names:
        if fn != id_header:
            to_add = [fn + "_" + str(bn) for bn in bin_nums]
            feat_names_new.extend(to_add)
            
    mapped_df = gb_padded.apply(map_multihot)
    lol = mapped_df.values.tolist() # list of list
    
    new_rows = []
    for row in lol:
        new_row = []
        for l in row:
            new_row.extend(list(l))
        new_rows.append(new_row)
    
    n, _ = gb_padded.shape
    p_new = len(feat_names_new)

    binned_feats_df = pd.DataFrame(new_rows, columns=feat_names_new)
    binned_feats_df[id_header] = index_new
    binned_feats_df.set_index(id_header, inplace=True)
    
    return binned_feats_df
