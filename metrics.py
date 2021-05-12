#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Maxime Cauté
Created: 07.04.2021

This file is dedicated to the implementation of metrics for solutions.
"""
import numpy as np
import itertools


EUCLIDIAN_DISTANCE = lambda a,b : np.linalg.norm(a-b)

def remove_wrong_indices_in_tuple(tuple):
    """
    Removes invalid indices (e.g. -1) in a tuple.
    --
    Input:
        - tuple: int list dict. The tuple to remove indices from.
    Output:
        - cleaned_tuple: int list dict. The tuple with invalid indices removed.
    """
    return {group_id: index for group_id, index in tuple.items() if index!=-1}

def remove_wrong_indices_in_tuple_pair(tuple1, tuple2):
    """
    Removes invalid indices (e.g. -1) in a tuple pair.
    If an index is invalid in a tuple, it is removed in the second tuple as well.
    --
    Input:
        - tuple1: int list dict. The first tuple to remove indices from.
        - tuple2: int list dict. The second tuple to remove indices from.
    Output:
        - cleaned_tuple1: int list dict.
            The first tuple with invalid indices removed.
        - cleaned_tuple2: int list dict.
            The first tuple with invalid indices removed.
    """
    valid_indices = []
    for i, element in enumerate(tuple1):
        if element != -1 and tuple2[i] != -1:
            valid_indices.append(i)
    return [tuple1[i] for i in valid_indices], [tuple2[i] for i in valid_indices]


def compute_distance_from_tuples_and_group_indices(
                tuple1, tuple2,
                group1_id,group2_id,
                groups_dataframe,
                distance_metric = EUCLIDIAN_DISTANCE,
                distance_modifier = lambda x: x,

    ):
    """
    Computes a distance between two elements,
    taken from given respective tuple and groups, over values from a dataframe.
    --
    Input:
        - tuple1: int list dict. The tuple of the first element.
        - tuple2: int list dict. The tuple of the second element.
        - group1_id: string. The id of the group of the first element.
        - group2_id: string. The id of the group of the second element.
        - groups_dataframe: pd.DataFrameGroupBy. The dataframe grouped by groups.
    Parameters:
        - distance_metric: int array-like -> int array-like.
            The metric to compute distance with.
            Defaults to euclidian distance.
        - distance_modifier: int -> int. A modifier to apply to distances.
            Defaults to identity.
    Output:
        - modified_elements_distance: int.
            The (modified) distance computed between the elements.
    """
    element1_index = tuple1[group1_id]
    element2_index = tuple2[group2_id]

    group1_dataframe = groups_dataframe.get_group(group1_id)
    group2_dataframe = groups_dataframe.get_group(group2_id)

    #The first element of .values is the index
    element1_values = group1_dataframe.loc[element1_index].values[1:]
    element2_values = group2_dataframe.loc[element2_index].values[1:]

    elements_distance = distance_metric(element1_values, element2_values)
    return distance_modifier(elements_distance)

def compute_distance_between_subgroups( element_indices_by_subgroup_per_tuple,
                                        groups_dataframe,
                                        distance_metric = EUCLIDIAN_DISTANCE,
                                        distance_modifier = lambda x: x**2
    ):
    """
    Computes the distance between the elements of two subgroups of a dataframe.
    --
    Input:
        - elements_indices_by_subgroup_per_tuple: int dict list.
            The list of tuples for chosen element by subgroup,
            to compute distance from for a given subgroup
                Such a tuple is a dictionnary of groups associated (by id)
                with one of their element.
        - groups_dataframe: pd.DataFrameGroupBy. The grouped dataframe.
    Parameters:
        - distance_metric: int array-like -> int array-like.
            The metric to compute distance with.
            Defaults to euclidian distance.
        - distance_modifier: int -> int. A modifier to apply to distances.
            Defaults to square.
    Outputs:
        - distance: int. The distance between the subgroups
    """
    subgroups_size = len(element_indices_by_subgroup_per_tuple)
    num_groups = len(element_indices_by_subgroup_per_tuple[0])
    distance = 0

    groups_ids = groups_dataframe.indices.keys()
    for group1_id, group2_id in itertools.combinations(groups_ids, 2):
        for tuple1, tuple2 in itertools.combinations_with_replacement(element_indices_by_subgroup_per_tuple,2):
            #Can move modifier into distance
            distance+= compute_distance_from_tuples_and_group_indices(
                tuple1, tuple2,
                group1_id, group2_id,
                groups_dataframe,
                distance_metric = distance_metric,
                distance_modifier = distance_modifier
            )
    return distance

def compute_distance_within_tuple(  element_indices_by_subgroup__tuple,
                                    groups_dataframe,
                                    distance_metric = EUCLIDIAN_DISTANCE,
                                    distance_modifier = lambda x : x**2):
    """
    Computes the distance within all the valid the elements of a tuple
    in a dataframe.
    --
    Input:
        - elements_indices_by_subgroup_per_tuple: int dict list.
            The list of tuples for chosen element by subgroup,
            to compute distance from for a given subgroup
                Such a tuple is a dictionnary of groups associated (by id)
                with one of their element.
        - groups_dataframe: pd.DataFrameGroupBy. The grouped dataframe.
    Parameters:
        - distance_metric: int array-like -> int array-like.
            The metric to compute distance with.
            Defaults to euclidian distance.
        - distance_modifier: int -> int. A modifier to apply to distances.
            Defaults to square.
    Outputs:
        - distance: int. The distance between the subgroups
    """
    tuple =  remove_wrong_indices_in_tuple(element_indices_by_subgroup__tuple)
    group_ids = list(tuple.keys())
    distance = 0

    for group1_index, group2_index in itertools.combinations(group_ids, 2):
        distance+= compute_distance_from_tuples_and_group_indices(
            tuple, tuple,
            group1_index, group2_index,
            groups_dataframe,
            distance_metric = distance_metric,
            distance_modifier = distance_modifier
        )
    return distance
