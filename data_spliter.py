"""
Author(s): Maxime Cauté
Created: 17.03.2021

This file is dedicated to the seperation of data into appropriate groups
"""
from search_tree import SearchTree

def compute_groups_indices(data_to_differentiate):
    """
    This functions computes groups indices from boolean data to be differentiated.
    Groups are created only if they have representants.
    --
    Input:
        - data_to_differentiate: pandas DataFrame.
            The part of data that should be differentiated.
            The values should be boolean.
    Output:
        - groups_indices: int set list.
            The indices of the elements in each group.
            The i-th element contains the indices of the elements in group i.
    """
    groups_indices = [set(data_to_differentiate.index)]
    for differentiation_parameter in data_to_differentiate:
        parameter_dataframe = data_to_differentiate[differentiation_parameter]

        subgroups_indices = []
        for truth_value in [True,False]:
            differentiated_data_index = data_to_differentiate.index[
                                        parameter_dataframe == truth_value]

            for group_indices in groups_indices:
                subgroup_indices = group_indices.intersection(differentiated_data_index)

                if subgroup_indices != set():
                    subgroups_indices.append(subgroup_indices)
        groups_indices = subgroups_indices
    return groups_indices

def compute_subgroups_indices(data_to_match, data_to_differentiate,
                            groups_size = 2):
    """
    This function computes indices for groups based on data.

    WIP
    Note : does not check that differentiation columns have valid boolean values.
    Note: currently works for only 2 groups
    --
    Input:
        - data_to_match: pandas DataFrame.
            The part of data that should be matched.
        - data_to_differentiate: pandas DataFrame.
            The part of data that should be differentiated.
            The values should be boolean.
    Parameters:
        - groups_size: int. The sizes of the group to create.
            Defaults to groups of size 2 (TO BE CHANGED)
    Outputs:
        - subgroups_indices : int list list.
            The indices of the elements in each subgroup.
            The i-th element contains the indices of the selected elements in subgroup i.
    """
    NUM_GROUPS = 2
    HEURISTIC = lambda s: next(iter(s)) #gets an element of the set #perhaps not clean to use sets?

    ## NOTE : RETURN PDSERIES?
    #Ignore lines not in subgroup

    groups_indices = compute_groups_indices(data_to_differentiate)
    num_subgroups = len(groups_indices)

    ## HARD SELECTION FOR 2-Group match -> TODO
    #groups_indices = groups_indices[0:2]

    search_tree = SearchTree(groups_indices, groups_size)
    for tuple_index in range(groups_size):
        for subgroup_index in range(num_subgroups):
            chosen_element_index = search_tree.current_node.compute_index_in_subgroup_in_tuple_with_local_heuristic(
                    HEURISTIC,
                    subgroup_index,
                    tuple_index
            )
            search_tree.decide_index_for_subgroup_in_tuple_from_current_node(
                chosen_element_index, subgroup_index, tuple_index
            )
    subgroups_indices_tuples = search_tree.get_current_solution()

    subgroups_elements_indices = [[] for i in range(num_subgroups)]
    for subgroups_indices_tuple in subgroups_indices_tuples:
        for subgroup_index, subgroup_element_index in enumerate(subgroups_indices_tuple):
            subgroups_elements_indices[subgroup_index].append(subgroup_element_index)

    return subgroups_elements_indices
