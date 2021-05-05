"""
Author: Maxime Cauté
Created: 05.05.2021

This file is dedicated to data preprocessing, for use in EquiTables.
"""
import numpy as np

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
