"""
Author: Maxime Cauté
Created: 07.04.2021

This file is dedicated to the implementation of metrics for solutions.
"""
import numpy as np
import itertools


EUCLIDIAN_DISTANCE = lambda a,b : np.linalg.norm(a-b)

def remove_wrong_indices_in_tuple(tuple):
    valid_indices = []
    for i, element in enumerate(tuple):
        if element != -1:
            valid_indices.append(i)
    return [tuple[i] for i in valid_indices]

def remove_wrong_indices_in_tuple_pair(tuple1, tuple2):
    valid_indices = []
    for i, element in enumerate(tuple1):
        if element != -1 and tuple2[i] != -1:
            valid_indices.append(i)
    return [tuple1[i] for i in valid_indices], [tuple2[i] for i in valid_indices]


def compute_distance_from_tuples_and_group_indices(
                baseline_tuple,
                target_tuple,
                baseline_group_id,target_group_id,
                groups_dataframe,
                distance_metric = EUCLIDIAN_DISTANCE
    ):

    baseline_group_index = list(groups_dataframe.indices.keys()).index(baseline_group_id)
    target_group_index = list(groups_dataframe.indices.keys()).index(target_group_id)
    baseline_element_index = baseline_tuple[baseline_group_index]
    target_element_index = target_tuple[target_group_index]

    baseline_group = groups_dataframe.get_group(baseline_group_id)
    target_group = groups_dataframe.get_group(target_group_id)

    #Index is part of .values
    baseline_element_values = baseline_group.loc[baseline_element_index].values[1:]
    target_element_values = target_group.loc[target_element_index].values[1:]

    elements_distance = distance_metric(baseline_element_values, target_element_values)
    return elements_distance

def add_modified_distance_from_tuples_and_group_indices(
                current_distance,
                baseline_tuple,
                target_tuple,
                baseline_group_id,target_group_id,
                groups_dataframe,
                distance_metric = EUCLIDIAN_DISTANCE,
                distance_modifier = lambda x : x**2
    ):
    elements_distance = compute_distance_from_tuples_and_group_indices(
        baseline_tuple,
        target_tuple,
        baseline_group_id,target_group_id,
        groups_dataframe,
        distance_metric = distance_metric
    )
    return current_distance + distance_modifier(elements_distance)

def compute_distance_between_subgroups( element_indices_per_subgroup_per_tuple,
                                        groups_dataframe,
                                        distance_metric = EUCLIDIAN_DISTANCE
    ):
    subgroups_size = len(element_indices_per_subgroup_per_tuple)
    num_groups = len(element_indices_per_subgroup_per_tuple[0])

    distance = 0

    groups_ids = groups_dataframe.indices.keys()
    for baseline_group_id, target_group_id in itertools.combinations(groups_ids, 2):
        for baseline_tuple, target_tuple in itertools.combinations_with_replacement(element_indices_per_subgroup_per_tuple,2):
            distance = add_modified_distance_from_tuples_and_group_indices(
                distance,
                baseline_tuple, target_tuple,
                baseline_group_id,target_group_id,
                groups_dataframe,
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
        tuple =  remove_wrong_indices(element_indices_per_subgroup__tuple)
        distance = add_modified_distance_from_tuples_and_group_indices(
            distance,
            tuple, tuple,
            baseline_group_index,target_group_index,
            normalized_data_to_match,
            distance_metric = distance_metric
        )
    return distance
