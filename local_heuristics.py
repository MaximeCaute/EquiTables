"""
Author: Maxime Cauté
Created: 31/03/2021

This file is dedicated to the implementation and selection of local heuristics.
Heuristics are functions that take a node and return, in this very order:
    - the chosen element;
    - the index of the subgroup it will be part of;
    - the index of the tuple it will be part of.
"""
def choose_first_possible(node):
    for tuple_index, possible_indices_for_subgroups_tuple in enumerate(node.subgroups_possible_indices_tuples):
        for subgroup_index, subgroup_possible_indices in enumerate(possible_indices_for_subgroups_tuple):
            if len(subgroup_possible_indices) > 0 :
                chosen_element = next(iter(subgroup_possible_indices))
                return chosen_element, subgroup_index, tuple_index

def get_local_heuristic_by_name(heuristic_name):
    """
    This function retrieves a given local heuristic by its name.
    If the name is not valid, returns "first possible" heuristic,
    and raises a warning.
    --
    Input:
        - heuristic_name: string. The name of the heuristic.
            Current possible options are:
                + "first possible".
    Outputs:
        - local_heuristic: local_heuristic. The chosen local heuristic.
            Is "first possible" heuristic by default for invalid names.

    """
    if heuristic_name == "first possible":
        return choose_first_possible
    print(f"WARNING: invalid name - {heuristic_name}!")
    return choose_first_possible
