"""
Author: Maxime Cauté
Created: 07.04.2021

This file is dedicated to the implementation of metrics for solutions.
"""
import numpy as np
import itertools

EUCLIDIAN_DISTANCE = lambda a,b : np.linalg.norm(a-b)


def get_values_vector_from_dataframe_and_row_index(dataframe, row_index):
    return dataframe.iloc[row_index].values

def compute_distance_from_tuples_and_group_indices(
                baseline_tuple,
                target_tuple,
                baseline_group_index,target_group_index,
                normalized_data_to_match,
                distance_metric = EUCLIDIAN_DISTANCE
    ):
    baseline_element_index = baseline_tuple[baseline_group_index]
    target_element_index = target_tuple[target_group_index]

    baseline_element_values = normalized_data_to_match.iloc[baseline_element_index].values
    target_element_values = normalized_data_to_match.iloc[target_element_index].values

    elements_distance = distance_metric(baseline_element_values, target_element_values)
    return elements_distance

def add_modified_distance_from_tuples_and_group_indices(
                current_distance,
                baseline_tuple,
                target_tuple,
                baseline_group_index,target_group_index,
                normalized_data_to_match,
                distance_metric = EUCLIDIAN_DISTANCE,
                distance_modifier = lambda x : x**2
    ):
    elements_distance = compute_distance_from_tuples_and_group_indices(
        baseline_tuple,
        target_tuple,
        baseline_group_index,target_group_index,
        normalized_data_to_match,
        distance_metric = distance_metric
    )
    return current_distance + distance_modifier(elements_distance)

def compute_distance_between_subgroups( element_indices_per_subgroup_per_tuple,
                                        normalized_data_to_match,
                                        distance_metric = EUCLIDIAN_DISTANCE
    ):
    subgroups_size = len(element_indices_per_subgroup_per_tuple)
    num_groups = len(element_indices_per_subgroup_per_tuple[0])
    num_parameters = normalized_data_to_match.shape[1]

    distance = 0

    groups_indices = range(num_groups)
    for baseline_group_index, target_group_index in itertools.combinations(groups_indices, 2):
        for baseline_tuple, target_tuple in itertools.combinations_with_replacement(element_indices_per_subgroup_per_tuple,2):
            distance = add_modified_distance_from_tuples_and_group_indices(
                distance,
                baseline_tuple, target_tuple,
                baseline_group_index,target_group_index,
                normalized_data_to_match,
                distance_metric = distance_metric
            )
    return distance

def compute_distance_within_tuple(  element_indices_per_subgroup__tuple,
                                    normalized_data_to_match,
                                    distance_metric = EUCLIDIAN_DISTANCE):
    num_subgroups = len(element_indices_per_subgroup__tuple)
    subgroups_indices = range(num_subgroups)
    distance = 0

    for baseline_group_index, target_group_index in itertools.combinations(subgroups_indices, 2):
        tuple =  element_indices_per_subgroup__tuple,
        distance = add_modified_distance_from_tuples_and_group_indices(
            distance,
            tuple, tuple,
            baseline_group_index,target_group_index,
            normalized_data_to_match,
            distance_metric = distance_metric
        )
    return distance
