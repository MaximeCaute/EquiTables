"""
Author: Maxime Cauté
Created: 07.04.2021

This file is dedicated to the implementation of metrics for solutions.
"""
import numpy as np
import itertools

EUCLIDIAN_DISTANCE = lambda a,b : np.linalg.norm(a-b)

def compute_distance_between_subgroups( element_indices_per_subgroup_per_tuple,
                                        normalized_data_to_match,
                                        distance_metric = EUCLIDIAN_DISTANCE
    ):
    subgroups_size = len(element_indices_per_subgroup_per_tuple)
    num_subgroups = len(element_indices_per_subgroup_per_tuple[0])
    num_parameters = normalized_data_to_match.shape[1]

    distance = 0

    subgroups_indices = range(num_subgroups)
    for subgroup1_index, subgroup2_index in itertools.combinations(subgroups_indices, 2):
        for baseline_tuple, target_tuple in itertools.combinations_with_replacement(element_indices_per_subgroup_per_tuple,2):
            baseline_element_index = baseline_tuple[subgroup1_index]
            target_element_index = target_tuple[subgroup2_index]


            baseline_element_values = normalized_data_to_match.iloc[baseline_element_index].values
            target_element_values = normalized_data_to_match.iloc[target_element_index].values

            distance+= distance_metric(baseline_element_values, target_element_values)**2
    return distance
