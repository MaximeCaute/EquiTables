#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Maxime Cauté
Created: 05.05.2021

This file is dedicated to data preprocessing, for use in EquiTables.
"""
import numpy as np
global EQUITABLES_GROUP_INDEX
EQUITABLES_GROUP_INDEX = 0
EQUITABLES_BASE_GROUPNAME = "EquiTablesGroup"

def drop_non_relevant_columns(dataframe, relevant_parameters):
    """
    Removes non-relevant columns from a dataframe,
    based on a list of column names.
    --
    Input:
        - dataframe: pd.DataFrame. The dataframe to remove columns from.
        - relevant_parameters: string list. The list of the column names to keep.
    Output:
        - cleaned_dataframe: pd.DataFrame.
            The dataframe with only relevant columns.
    """
    return dataframe[relevant_parameters]

def normalize_dataframe(dataframe, columns_to_normalize):
    """
    Normalizes the values of a dataframe, for each relevant variable.
    Normalization process divides the values of a variable
    by the maximal value among themselves.
    Resulting normalized values are thus between 0 and 1.
    --
    Input:
        - dataframe: pd.DataFrame. The dataframe to normalize.
        - columns_to_normalize: string_list.
            The name of the columns to normalize over.
    Output:
        - dataframe: pd.DataFrame. The normalized_dataframe.
        - normalization_factors: int dict.
            The factors used for normalization,
            associated with the name of the column they were applied to.
    """
    normalization_factors = {}
    for column_to_normalize in columns_to_normalize:
        max_value = np.max(dataframe[column_to_normalize].values)
        dataframe = dataframe.apply(lambda x: x/max_value if x.name == column_to_normalize else x)
        normalization_factors[column_to_normalize] = max_value
    return dataframe, normalization_factors

def denormalize_dataframe(dataframe, normalization_factors):
    """
    Undoes the normalization of a dataframe done with given factors.
    --
    Input:
        - dataframe: pd.DataFrame. The normalized dataframe to denormalize.
        - normalization_factors: int dict.
            The factors used for normalization,
            associated with the name of the variable as a dataframe column.
    Output:
        - dataframe: pd.DataFrame. The denormalized dataframe.
    """
    for variable, factor in normalization_factors.items():
        dataframe = dataframe.apply(lambda x: x*factor if x.name == variable else x)
    return dataframe

def split_from_indicator(dataframe, group_indicator_function = lambda row: None):
    """
    Adds boolean group labels in a dataframe according to an assignmenent function.
    --
    Input:
        - dataframe: pd.DataFrame. The dataframe to add groups labels to.
    Parameters:
        - group_indicator_function: pd.Series -> string or int.
            The function that indicates groups by labels given a row.
            If the indication is not a label it creates a custom label
            by converting the indication to a string and prefixing "EquiTablesGroup".
                Defaults to a single None label for each row.
    Outputs:
        - dataframe: pd.DataFrame.
            The dataframe with added boolean columns to indicate groups.
    """
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
    """
    Drops custom groups from a dataframe.
    Customs groups include specified ones as well as EquiTableGroups.
    --
    Input:
        - dataframe: pd.DataFrame. The dataframe to drop groups from.
    Parameters:
        - custom_groups_names: string list.
            A list of specific custom groups names to remove.
            Defaults to an empty list.
    Output:
        - dataframe: pd.DataFrame. The dataframe with custom columns removed
    """
    for column_name in dataframe.copy():
        if (column_name in custom_groups_names) or column_name.startswith(EQUITABLES_BASE_GROUPNAME):
            dataframe = dataframe.drop(column_name,axis = 1)
    return dataframe
