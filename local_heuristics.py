"""
Author: Maxime Cauté
Created: 31/03/2021

This file is dedicated to the implementation and selection of local heuristics.
Heuristics are functions that take a node and return, in this very order:
    - the chosen element;
    - the index of the subgroup it will be part of;
    - the index of the tuple it will be part of;
    - a score for this choice.
Defined heuristics should be added to the ALLOWED_LOCAL_HEURISTIC_NAMES dictionnary with their name.
"""

import numpy as np
import metrics

def choose_first_possible(node):
    for (tuple_index, subgroup_id, element_index) in node.enumerate_possibilities():
        return element_index, subgroup_id, tuple_index, 0



def find_nearest(dataframe, chosen_indices, subgroup_index, subgroup_possible_indices):
    mindistance = np.Inf
    for candidate in subgroup_possible_indices:
        candidate_tuple = chosen_indices.copy()
        candidate_tuple[subgroup_index] = candidate
        dist = metrics.compute_distance_within_tuple(candidate_tuple, dataframe)
        if dist < mindistance:
            dist = mindistance
            best_candidate = candidate
    return best_candidate


def choose_nearest(node):
    for tuple_index, possible_indices_for_subgroups_tuple in enumerate(node.subgroups_possible_indices_tuples):
        for subgroup_index, subgroup_possible_indices in enumerate(possible_indices_for_subgroups_tuple):
            if len(subgroup_possible_indices) > 0 :
                chosen_indices = node.subgroups_chosen_indices_tuples[tuple_index]
                chosen_element = find_nearest(node.groups_dataframe,
                                              chosen_indices,
                                              subgroup_index,
                                              subgroup_possible_indices)
                return chosen_element, subgroup_index, tuple_index, 0


ALLOWED_LOCAL_HEURISTIC_NAMES = {
    'first_possible': choose_first_possible,
    'simple_nearest': choose_nearest
}

def get_local_heuristic_by_name(heuristic_name):
    """
    This function retrieves a given local heuristic by its name.
    If the name is not valid, returns "first_possible" heuristic,
    and raises a warning.
    --
    Input:
        - heuristic_name: string. The name of the heuristic.
            Current possible options are:
                + first_possible.
    Outputs:
        - local_heuristic: local_heuristic. The chosen local heuristic.
            Is "first_possible" heuristic by default for invalid names.

    """
    if heuristic_name in ALLOWED_LOCAL_HEURISTIC_NAMES:
        return ALLOWED_LOCAL_HEURISTIC_NAMES[heuristic_name]
    default_local_heuristic_name = list(ALLOWED_LOCAL_HEURISTIC_NAMES.keys())[0]
    print(  f"WARNING: invalid name - {heuristic_name}!\n"+
            f"Resolving to default heuristic '{default_local_heuristic_name}'.")
    return ALLOWED_LOCAL_HEURISTIC_NAMES[default_local_heuristic_name]
