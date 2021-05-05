"""
Author: Maxime Cauté
Created: 05.05.2021

This file is dedicated to data preprocessing, for use in EquiTables.
"""
import numpy as np
global EQUITABLE_GROUP_INDEX
EQUITABLE_GROUP_INDEX = 0

def normalize_dataframe(dataframe, variables_to_normalize):
    normalization_factors = {}
    for variable_to_normalize in variables_to_normalize:
        max_value = np.max(dataframe[variable_to_normalize].values)
        dataframe = dataframe.apply(lambda x: x/max_value if x.name == variable_to_normalize else x)
        normalization_factors[variable_to_normalize] = max_value
    return dataframe, normalization_factors

def denormalize_dataframe(dataframe, normalization_factors):
    for variable, factor in normalization_factors.items():
        dataframe = dataframe.apply(lambda x: x*factor if x.name == variable else x)
    return dataframe

def split_from_indicator(dataframe, group_indicator_function = lambda row: None):
    dataframe = dataframe.copy()
    function_indices_to_equitable_indices = {}
    for index, row in dataframe.iterrows():
        group_label = group_indicator_function(row)

        if group_label == None:
            continue
        if type(group_label) != str:
            global EQUITABLE_GROUP_INDEX
            print(f"WARNING! Non custom group label used: {group_label}!")
            if group_label not in function_indices_to_equitable_indices:
                function_indices_to_equitable_indices[group_label] = EQUITABLE_GROUP_INDEX
                EQUITABLE_GROUP_INDEX+=1
            group_label = f"EquiTableGroup{function_indices_to_equitable_indices[group_label]}"
            print(f"Using custom EquiTable label instead: {group_label}")

        if group_label not in dataframe:
            dataframe[group_label] = False

        dataframe.at[index, group_label] = True
    return dataframe
