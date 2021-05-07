"""
Author: Maxime Cauté
Created: 05.05.2021

This file is dedicated to data preprocessing, for use in EquiTables.
"""
import numpy as np
global EQUITABLES_GROUP_INDEX
EQUITABLES_GROUP_INDEX = 0
EQUITABLES_BASE_GROUPNAME = "EquiTablesGroup"

def drop_irrelevant_columns(dataframe, relevant_parameters):
    return dataframe[relevant_parameters]

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
    old_dataframe = dataframe
    dataframe = dataframe.copy()
    function_indices_to_equitable_indices = {}
    for index, row in dataframe.iterrows():
        group_label = group_indicator_function(row)

        if group_label == None:
            continue
        if type(group_label) != str:
            global EQUITABLES_GROUP_INDEX
            print(f"WARNING! Non custom group label used: {group_label}!")
            if group_label not in function_indices_to_equitable_indices:
                function_indices_to_equitable_indices[group_label] = str(EQUITABLES_GROUP_INDEX)
                EQUITABLES_GROUP_INDEX+=1
            group_label = EQUITABLES_BASE_GROUPNAME+function_indices_to_equitable_indices[group_label]
            print(f"Using custom EquiTables label instead: {group_label}")

        if group_label in old_dataframe:
            raise Exception(f"Group label already used in original dataframe: {group_label}.")
        if group_label not in dataframe:
            dataframe[group_label] = False

        dataframe.at[index, group_label] = True
    return dataframe

def drop_custom_groups(dataframe, custom_groups_names = []):
    for column_name in dataframe.copy():
        if (column_name in custom_groups_names) or column_name.startswith(EQUITABLES_BASE_GROUPNAME):
            dataframe = dataframe.drop(column_name,axis = 1)
    return dataframe
